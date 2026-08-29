use anyhow::{Context, Result};
use ed25519_dalek::{VerifyingKey, Signature, Verifier};
use std::fs;
use std::path::Path;
use tracing::info;

pub struct KeyStore {
    sovereign_pubkey: Option<VerifyingKey>,
}

impl KeyStore {
    pub fn load(sov_path: Option<&Path>) -> Result<Self> {
        let pk = match sov_path {
            Some(p) => {
                let hex_str = fs::read_to_string(p).context("read sovereign pubkey")?;
                let bytes = hex::decode(hex_str.trim()).context("invalid hex")?;
                let arr: [u8; 32] = bytes.try_into().context("pubkey must be 32 bytes")?;
                Some(VerifyingKey::from_bytes(&arr)?)
            }
            None => None,
        };
        info!(loaded = pk.is_some(), "KeyStore init");
        Ok(Self { sovereign_pubkey: pk })
    }

    pub fn verify_sovereign(&self, message: &[u8], sig_bytes: &[u8; 64]) -> bool {
        let pk = match &self.sovereign_pubkey {
            Some(k) => k,
            None => return false,
        };
        let sig = Signature::from_bytes(sig_bytes);
        pk.verify(message, &sig).is_ok()
    }
}
