use tracing::{debug, info};
use crate::policy::PolicyConfig;

pub struct IntentRouter<'a> {
    config: &'a PolicyConfig,
}

impl<'a> IntentRouter<'a> {
    pub fn new(config: &'a PolicyConfig) -> Self {
        Self { config }
    }

    pub fn classify(&self, user_message: &str) -> Vec<String> {
        let lower = user_message.to_lowercase();
        let mut scores: Vec<(String, u32, u8)> = Vec::new();
        for (name, domain) in &self.config.intent_router.domains {
            let score: u32 = domain.keywords.iter()
                .filter(|kw| lower.contains(&kw.to_lowercase()))
                .count() as u32;
            if score > 0 {
                debug!(domain = name.as_str(), score = score, "matched");
                scores.push((name.clone(), score, domain.priority));
            }
        }
        scores.sort_by(|a, b| b.1.cmp(&a.1).then_with(|| a.2.cmp(&b.2)));
        let mut tools: Vec<String> = Vec::new();
        for (name, _, _) in &scores {
            if let Some(d) = self.config.intent_router.domains.get(name) {
                for t in &d.tools {
                    if !tools.contains(t) { tools.push(t.clone()); }
                }
            }
        }
        let max = self.config.global.max_tools_per_turn;
        let result: Vec<String> = tools.into_iter().take(max).collect();
        info!(count = result.len(), "Intent classified");
        result
    }
}
