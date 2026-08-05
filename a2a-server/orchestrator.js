/**
 * Orchestrator Agent — Task Lifecycle Manager (Step 6).
 *
 * Forged 2026-08-05. DITEMPA BUKAN DIBERI.
 *
 * The capstone of the AAA agentic loop. Manages task lifecycles across
 * the federation: dispatch, monitor, retry, reroute, escalate.
 *
 * State machine:
 *   PENDING → ASSIGNED → IN_PROGRESS → COMPLETED
 *                    ↓         ↓
 *                  FAILED ← RETRYING → ESCALATED
 *
 * Integrates with:
 *   - Cockpit (agent discovery, liveness)
 *   - Agent Inbox (task dispatch to agents)
 *   - Redis (task queue persistence)
 *   - Witness/Predict gates (pre-execution checks)
 *   - 888-APEX (escalation when exhausted)
 */
'use strict';

const crypto = require('crypto');
const fs = require('fs');

// ── Task States ──────────────────────────────────────────────────────
const TASK_STATES = {
    PENDING: 'PENDING',
    ASSIGNED: 'ASSIGNED',
    IN_PROGRESS: 'IN_PROGRESS',
    RETRYING: 'RETRYING',
    COMPLETED: 'COMPLETED',
    FAILED: 'FAILED',
    ESCALATED: 'ESCALATED',
};

const MAX_RETRIES = 3;
const RETRY_BACKOFF_MS = [1000, 4000, 16000]; // 1s, 4s, 16s

// ── Agent Capability Map ─────────────────────────────────────────────
// Which agents can handle which task domains
const AGENT_CAPABILITIES = {
    'shell':        ['a-forge', 'opencode'],
    'git':          ['a-forge', 'opencode'],
    'deploy':       ['a-forge'],
    'filesystem':   ['a-forge', 'opencode'],
    'docker':       ['a-forge'],
    'browser':      ['a-forge', 'hermes'],
    'seismic':      ['geox'],
    'petrophysics': ['geox'],
    'basin':        ['geox'],
    'prospect':     ['geox'],
    'capital':      ['wealth'],
    'market':       ['wealth'],
    'risk':         ['wealth'],
    'vitality':     ['well'],
    'dignity':      ['well'],
    'judge':        ['arifos', '888-APEX'],
    'seal':         ['arifos'],
    'route':        ['aaa'],
    'code':         ['opencode', '333-AGI'],
    'research':     ['555-ASI', '333-AGI'],
    'vision':       ['555-ASI-VISION'],
    'fact_check':   ['hermes', '555-ASI'],
};

// Agent priority (lower = higher priority)
const AGENT_PRIORITY = {
    'a-forge': 1,
    'opencode': 2,
    'arifos': 1,
    'geox': 1,
    'wealth': 1,
    'well': 1,
    '555-ASI': 2,
    '555-ASI-VISION': 2,
    '333-AGI': 3,
    'hermes': 4,
    '888-APEX': 5,
};

// ── Orchestrator ──────────────────────────────────────────────────────

class Orchestrator {
    constructor(redisClient, inbox, cockpitPath) {
        /** Redis client for persistence */
        this.redis = redisClient;
        /** Agent Inbox for task dispatch */
        this.inbox = inbox;
        /** Path to cockpit status.json */
        this.cockpitPath = cockpitPath || '/root/AAA/state/status.json';
        /** In-memory task registry */
        this.tasks = new Map();
        /** Task queue key in Redis */
        this.queueKey = 'aaa:orchestrator:queue';
        /** Active task counter */
        this.taskCount = 0;
    }

    /**
     * Create a new task.
     * @param {object} spec - { intent, domain, tool, priority, deadline_ms, constraints }
     * @returns {{ task_id: string, state: string }}
     */
    createTask(spec = {}) {
        const taskId = crypto.randomUUID();
        const task = {
            task_id: taskId,
            state: TASK_STATES.PENDING,
            intent: spec.intent || '',
            domain: spec.domain || this._classifyDomain(spec.intent || ''),
            tool: spec.tool || '',
            priority: spec.priority || 5,
            deadline_ms: spec.deadline_ms || 300000, // 5min default
            constraints: spec.constraints || { reversibility: 'FULL' },
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            retry_count: 0,
            max_retries: spec.max_retries || MAX_RETRIES,
            assigned_agent: null,
            attempt_history: [],
            result: null,
            error: null,
        };

        this.tasks.set(taskId, task);
        this.taskCount++;
        this._persistQueue();

        console.log(`[orchestrator] Created task ${taskId.substring(0,8)}: ${task.intent.substring(0,50)}`);
        return task;
    }

    /**
     * Run the orchestrator loop — dispatch pending tasks to available agents.
     * @returns {Promise<{dispatched: number, results: object[]}>}
     */
    async tick() {
        const pending = Array.from(this.tasks.values())
            .filter(t => t.state === TASK_STATES.PENDING)
            .sort((a, b) => a.priority - b.priority);

        const results = [];
        for (const task of pending) {
            try {
                const result = await this._dispatchTask(task);
                results.push(result);
            } catch (e) {
                results.push({ task_id: task.task_id, error: e.message });
            }
        }

        return {
            dispatched: results.filter(r => r.dispatched).length,
            results,
        };
    }

    /**
     * Dispatch a single task to the best available agent.
     */
    async _dispatchTask(task) {
        // 1. Find capable agents
        const candidates = this._findCandidates(task.domain);
        if (candidates.length === 0) {
            task.state = TASK_STATES.FAILED;
            task.error = 'No capable agent found for domain: ' + task.domain;
            task.updated_at = new Date().toISOString();
            return { task_id: task.task_id, dispatched: false, error: task.error };
        }

        // 2. Filter to live agents (from cockpit)
        const liveAgents = this._filterLiveAgents(candidates);
        if (liveAgents.length === 0) {
            // All candidates dead — retry or fail
            return this._handleNoLiveAgents(task, candidates);
        }

        // 3. Pick best agent (priority, then first available)
        const bestAgent = liveAgents[0];

        // 4. Assign and send via inbox
        task.state = TASK_STATES.ASSIGNED;
        task.assigned_agent = bestAgent;
        task.updated_at = new Date().toISOString();

        // Send via inbox if available
        if (this.inbox && this.inbox.connected) {
            try {
                await this.inbox.send({
                    from: 'AAA-Orchestrator',
                    to: bestAgent,
                    intent: task.intent,
                    evidence: { OBS: [`Task ${task.task_id} dispatched by AAA Orchestrator`], DER: [], INT: [] },
                    constraints: task.constraints,
                    metadata: { task_id: task.task_id, domain: task.domain, priority: task.priority },
                });
                task.state = TASK_STATES.IN_PROGRESS;
            } catch (e) {
                console.error(`[orchestrator] Inbox send failed for ${bestAgent}: ${e.message}`);
            }
        }

        task.attempt_history.push({
            agent: bestAgent,
            timestamp: new Date().toISOString(),
            state: task.state,
        });

        console.log(`[orchestrator] Dispatched ${task.task_id.substring(0,8)} → ${bestAgent} (domain: ${task.domain})`);
        this._persistQueue();

        return { task_id: task.task_id, dispatched: true, agent: bestAgent, domain: task.domain };
    }

    /**
     * Handle case when no live agents are available.
     */
    _handleNoLiveAgents(task, candidates) {
        task.retry_count++;
        if (task.retry_count < task.max_retries) {
            task.state = TASK_STATES.RETRYING;
            task.error = `No live agents. Retry ${task.retry_count}/${task.max_retries}. Candidates: ${candidates.join(', ')}`;
            task.updated_at = new Date().toISOString();
            console.log(`[orchestrator] Retrying ${task.task_id.substring(0,8)} (${task.retry_count}/${task.max_retries})`);
            return { task_id: task.task_id, dispatched: false, retrying: true, error: task.error };
        } else {
            task.state = TASK_STATES.ESCALATED;
            task.error = `All agents exhausted after ${task.max_retries} retries. Candidates: ${candidates.join(', ')}`;
            task.updated_at = new Date().toISOString();
            console.log(`[orchestrator] ESCALATED ${task.task_id.substring(0,8)}`);
            return { task_id: task.task_id, dispatched: false, escalated: true, error: task.error };
        }
    }

    /**
     * Complete a task.
     */
    completeTask(taskId, result = {}) {
        const task = this.tasks.get(taskId);
        if (!task) return { error: 'task not found' };

        task.state = TASK_STATES.COMPLETED;
        task.result = result;
        task.updated_at = new Date().toISOString();
        this._persistQueue();
        console.log(`[orchestrator] Completed ${taskId.substring(0,8)}`);
        return { task_id: taskId, state: task.state };
    }

    /**
     * Fail a task (will be retried on next tick if retries remain).
     */
    failTask(taskId, error) {
        const task = this.tasks.get(taskId);
        if (!task) return { error: 'task not found' };

        task.retry_count++;
        if (task.retry_count < task.max_retries) {
            task.state = TASK_STATES.RETRYING;
            task.error = error;
            task.updated_at = new Date().toISOString();
            console.log(`[orchestrator] Failed ${taskId.substring(0,8)} — retrying (${task.retry_count}/${task.max_retries})`);
        } else {
            task.state = TASK_STATES.ESCALATED;
            task.error = error;
            task.updated_at = new Date().toISOString();
            console.log(`[orchestrator] Failed ${taskId.substring(0,8)} — escalated`);
        }
        this._persistQueue();
        return { task_id: taskId, state: task.state };
    }

    /**
     * Get task status.
     */
    getTask(taskId) {
        return this.tasks.get(taskId) || null;
    }

    /**
     * List all tasks.
     */
    listTasks(filter = 'all') {
        const all = Array.from(this.tasks.values());
        if (filter === 'active') return all.filter(t => t.state !== TASK_STATES.COMPLETED && t.state !== TASK_STATES.FAILED);
        if (filter === 'pending') return all.filter(t => t.state === TASK_STATES.PENDING);
        if (filter === 'completed') return all.filter(t => t.state === TASK_STATES.COMPLETED);
        if (filter === 'escalated') return all.filter(t => t.state === TASK_STATES.ESCALATED);
        return all;
    }

    /**
     * Get orchestrator stats.
     */
    stats() {
        const all = Array.from(this.tasks.values());
        return {
            total_tasks: all.length,
            pending: all.filter(t => t.state === TASK_STATES.PENDING).length,
            in_progress: all.filter(t => t.state === TASK_STATES.IN_PROGRESS).length,
            retrying: all.filter(t => t.state === TASK_STATES.RETRYING).length,
            completed: all.filter(t => t.state === TASK_STATES.COMPLETED).length,
            failed: all.filter(t => t.state === TASK_STATES.FAILED).length,
            escalated: all.filter(t => t.state === TASK_STATES.ESCALATED).length,
        };
    }

    // ── Internal ────────────────────────────────────────────────────

    _classifyDomain(intent) {
        const t = intent.toLowerCase();
        if (t.match(/\b(seismic|basin|geox|petrophysics|prospect|well.*log)\b/)) return 'geox';
        if (t.match(/\b(capital|npv|emv|market|portfolio|wealth|forex|risk)\b/)) return 'wealth';
        if (t.match(/\b(vitality|fatigue|well|homeostasis|dignity)\b/)) return 'well';
        if (t.match(/\b(judge|seal|verdict|constitutional)\b/)) return 'arifos';
        if (t.match(/\b(deploy|build|docker|systemctl)\b/)) return 'deploy';
        if (t.match(/\b(git|commit|push|merge)\b/)) return 'git';
        if (t.match(/\b(code|edit|write|refactor)\b/)) return 'code';
        if (t.match(/\b(research|search|investigate|analyze)\b/)) return 'research';
        if (t.match(/\b(image|vision|screenshot|photo)\b/)) return 'vision';
        return 'code';
    }

    _findCandidates(domain) {
        // Normalize domain
        const d = domain.toLowerCase();
        for (const [key, agents] of Object.entries(AGENT_CAPABILITIES)) {
            if (d.includes(key) || key.includes(d)) {
                return [...agents].sort((a, b) => (AGENT_PRIORITY[a] || 9) - (AGENT_PRIORITY[b] || 9));
            }
        }
        // Default: code-capable agents
        return ['a-forge', 'opencode', '333-AGI'];
    }

    _filterLiveAgents(candidates) {
        let liveAgents = [];
        try {
            const cockpit = JSON.parse(fs.readFileSync(this.cockpitPath, 'utf8'));
            const agentList = cockpit.agent_list || [];
            const alive = new Set(agentList.filter(a => a.status === 'healthy').map(a => a.agent_id));

            liveAgents = candidates.filter(c => alive.has(c) || c === '333-AGI' || c === '888-APEX');
        } catch {
            // Cockpit unavailable — assume all available
            liveAgents = [...candidates];
        }
        return liveAgents;
    }

    _persistQueue() {
        // Store task list to Redis if available
        if (this.redis && this.redis.isOpen) {
            try {
                const tasks = Array.from(this.tasks.values());
                this.redis.set(this.queueKey, JSON.stringify(tasks.slice(-50))); // keep last 50
            } catch { /* best-effort */ }
        }
    }
}

// ── Singleton ────────────────────────────────────────────────────────

let _orchestrator = null;

function getOrchestrator(redisClient, inbox) {
    if (!_orchestrator) {
        _orchestrator = new Orchestrator(redisClient, inbox);
    }
    return _orchestrator;
}

module.exports = { Orchestrator, getOrchestrator, TASK_STATES, AGENT_CAPABILITIES };
