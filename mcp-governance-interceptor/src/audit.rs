use std::fs::{self, OpenOptions};
use std::io::Write;
use std::path::Path;

use anyhow::{Context, Result};
use chrono::Utc;
use sha2::{Sha256, Digest};
use tracing::info;

use crate::types::{AuditEvent, InterceptorVerdict, PolicyReloadEvent};

pub struct AuditChain {
    chain_path: String,
    last_hash: String,
}

impl AuditChain {
    pub fn new(chain_path: &str) -> Self {
        let last_hash = Self::compute_tail_hash(chain_path);
        Self { chain_path: chain_path.to_string(), last_hash }
    }

    fn compute_tail_hash(chain_path: &str) -> String {
        match fs::read_to_string(chain_path) {
            Ok(content) => {
                if let Some(last) = content.lines().last() {
                    if !last.trim().is_empty() {
                        let mut h = Sha256::new();
                        h.update(last.as_bytes());
                        return format!("sha256:{}", hex::encode(h.finalize()));
                    }
                }
                "sha256:genesis".to_string()
            }
            Err(_) => "sha256:genesis".to_string(),
        }
    }

    pub fn log_verdict(
        &mut self,
        tool_name: &str,
        verdict: &InterceptorVerdict,
        role: Option<&str>,
        policy_version: &str,
    ) -> Result<()> {
        let ts = Utc::now().to_rfc3339();
        let etype = match verdict {
            InterceptorVerdict::Approved => "TOOL_CALL_APPROVED",
            InterceptorVerdict::Blocked { .. } => "TOOL_CALL_BLOCKED",
            InterceptorVerdict::RequiresHold { .. } => "TOOL_CALL_REQUIRES_HOLD",
        };
        let payload = format!("{}|{}|{}|{:?}|{}|{}", ts, etype, tool_name, verdict, role.unwrap_or("none"), policy_version);
        let mut h = Sha256::new();
        h.update(payload.as_bytes());
        let cur = format!("sha256:{}", hex::encode(h.finalize()));

        let event = AuditEvent {
            timestamp: ts,
            event_type: etype.to_string(),
            tool_name: Some(tool_name.to_string()),
            verdict: verdict.clone(),
            role: role.map(|r| r.to_string()),
            policy_version: policy_version.to_string(),
            chain_hash: cur.clone(),
            previous_hash: self.last_hash.clone(),
        };
        let json = serde_json::to_string(&event).context("serialize audit event")?;
        let mut f = OpenOptions::new().create(true).append(true).open(&self.chain_path)
            .with_context(|| format!("open audit chain: {}", self.chain_path))?;
        writeln!(f, "{}", json).context("write audit event")?;
        self.last_hash = cur;
        info!(tool = tool_name, "Audit logged");
        Ok(())
    }

    pub fn log_policy_reload(&mut self, pv: &str, ph: &str, signer: &str, added: u32, modified: u32, blocked: u32) -> Result<()> {
        let event = PolicyReloadEvent {
            timestamp: Utc::now().to_rfc3339(),
            event_type: "POLICY_RELOAD_SUCCESS".to_string(),
            policy_version: pv.to_string(),
            policy_hash: ph.to_string(),
            signature_algorithm: "ed25519".to_string(),
            signer: signer.to_string(),
            trigger: "hot-reload".to_string(),
            previous_hash: self.last_hash.clone(),
            delta_tools_added: added,
            delta_tools_modified: modified,
            delta_tools_blocked: blocked,
        };
        let json = serde_json::to_string(&event).context("serialize reload event")?;
        let mut h = Sha256::new();
        h.update(json.as_bytes());
        let cur = format!("sha256:{}", hex::encode(h.finalize()));
        let mut f = OpenOptions::new().create(true).append(true).open(&self.chain_path)
            .with_context(|| format!("open audit chain: {}", self.chain_path))?;
        writeln!(f, "{}", json).context("write reload event")?;
        self.last_hash = cur;
        Ok(())
    }

    pub fn verify_chain(path: &Path) -> Result<ChainIntegrity> {
        let content = fs::read_to_string(path).context("read audit chain")?;
        let lines: Vec<&str> = content.lines().filter(|l| !l.trim().is_empty()).collect();
        if lines.is_empty() {
            return Ok(ChainIntegrity::Valid { entries: 0 });
        }
        let mut prev = "sha256:genesis".to_string();
        for (i, line) in lines.iter().enumerate() {
            let ev: serde_json::Value = match serde_json::from_str(line) {
                Ok(v) => v,
                Err(e) => return Ok(ChainIntegrity::Broken { at_entry: i, reason: e.to_string() }),
            };
            let entry_prev = ev["previous_hash"].as_str().unwrap_or("");
            if entry_prev != prev {
                return Ok(ChainIntegrity::Broken { at_entry: i, reason: format!("chain break: expected {} got {}", prev, entry_prev) });
            }
            let mut h = Sha256::new();
            h.update(line.as_bytes());
            prev = format!("sha256:{}", hex::encode(h.finalize()));
        }
        Ok(ChainIntegrity::Valid { entries: lines.len() as u32 })
    }
}

#[derive(Debug)]
pub enum ChainIntegrity {
    Valid { entries: u32 },
    Broken { at_entry: usize, reason: String },
}
