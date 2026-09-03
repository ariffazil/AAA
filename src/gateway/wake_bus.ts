/**
 * Wake Bus — NATS-based agent wake signaling
 * 
 * Pattern distilled from paperclipai/paperclip heartbeat.ts (MIT)
 * Doctrine: DITEMPA BUKAN DIBERI
 * 
 * Provides:
 *   - publishWake(targetAgent, reason, payload, source) → NATS publish
 *   - subscribeWakes(agentId, handler) → durable JetStream consumer
 *   - getWakeStreamDepth(agentId?) → stream depth per agent
 * 
 * Wake reasons: assignment_created, comment_added, dependency_complete,
 *               budget_changed, held_release, sovereign_summons
 * 
 * Reuses cloudevents_bridge.ts connectNats() — zero new deps.
 * Stream: wake-bus, subjects wake.>, file storage, 7d retention.
 */

import { StringCodec, type NatsConnection } from 'nats';
import { connectNats } from './cloudevents_bridge.js';

const sc = StringCodec();
const WAKE_STREAM = 'wake-bus';
const WAKE_SUBJECT_PREFIX = 'wake';
const WAKE_RETENTION_DAYS = 7;

/** Allowed wake reason enum — mirrors Paperclip heartbeat wake events */
export const WakeReason = {
  ASSIGNMENT_CREATED: 'assignment_created',
  COMMENT_ADDED: 'comment_added',
  DEPENDENCY_COMPLETE: 'dependency_complete',
  BUDGET_CHANGED: 'budget_changed',
  HELD_RELEASE: 'held_release',
  SOVEREIGN_SUMMONS: 'sovereign_summons',
} as const;

export type WakeReasonType = typeof WakeReason[keyof typeof WakeReason];

export interface WakePayload {
  /** Target agent id (e.g. '333-AGI', 'FI-001') */
  target_agent: string;
  /** Why this wake was emitted */
  reason: WakeReasonType;
  /** Source of the wake (who emitted it) */
  source: string;
  /** Arbitrary payload data */
  payload?: Record<string, unknown>;
  /** ISO timestamp */
  timestamp: string;
  /** Unique wake id */
  wake_id: string;
}

export interface WakeHandler {
  (wake: WakePayload): void | Promise<void>;
}

/** Stream depth info for health reporting */
export interface WakeStreamDepth {
  agent_id?: string;
  message_count: number;
  byte_size: number;
  last_message_at: string | null;
}

// ── Stream setup ─────────────────────────────────────────────────────

let _streamEnsured = false;

async function ensureWakeStream(nc: NatsConnection): Promise<void> {
  if (_streamEnsured) return;

  const jsm = await nc.jetstreamManager();

  // Try to get stream info — if it exists, we're done
  try {
    const info = await jsm.streams.info(WAKE_STREAM);
    if (info) {
      _streamEnsured = true;
      return;
    }
  } catch {
    // Stream doesn't exist — create it
  }

  await jsm.streams.add({
    name: WAKE_STREAM,
    subjects: [`${WAKE_SUBJECT_PREFIX}.>`],
    storage: 'file',
    retention: 'limits',
    max_age: WAKE_RETENTION_DAYS * 24 * 60 * 60 * 1_000_000_000, // nanoseconds
    max_msgs: -1,
    max_bytes: -1,
    num_replicas: 1,
  });
  console.log(`[WakeBus] Created JetStream stream '${WAKE_STREAM}' (subjects: ${WAKE_SUBJECT_PREFIX}.>, retention: ${WAKE_RETENTION_DAYS}d)`);

  _streamEnsured = true;
}

// ── Publish ──────────────────────────────────────────────────────────

let _wakeCounter = 0;

/**
 * Publish a wake signal to a target agent via NATS.
 * Subject: wake.<target_agent>.<reason>
 * 
 * @param targetAgent — agent id to wake
 * @param reason — one of WakeReason enum values
 * @param payload — arbitrary data payload
 * @param source — who is emitting this wake
 */
export async function publishWake(
  targetAgent: string,
  reason: WakeReasonType,
  payload: Record<string, unknown> = {},
  source: string = '333-AGI',
): Promise<string> {
  const nc = await connectNats();
  await ensureWakeStream(nc);

  _wakeCounter++;
  const wakeId = `wake-${Date.now()}-${_wakeCounter.toString(36)}`;
  const subject = `${WAKE_SUBJECT_PREFIX}.${targetAgent}.${reason}`;

  const wake: WakePayload = {
    target_agent: targetAgent,
    reason,
    source,
    payload,
    timestamp: new Date().toISOString(),
    wake_id: wakeId,
  };

  nc.publish(subject, sc.encode(JSON.stringify(wake)));
  console.log(`[WakeBus] Published: ${subject} (wake_id=${wakeId})`);
  return wakeId;
}

// ── Subscribe ────────────────────────────────────────────────────────

/**
 * Subscribe to wake signals for a specific agent.
 * Uses plain NATS subscription (messages delivered in real-time).
 * For durable delivery, JetStream consumer can be wired later.
 * 
 * @param agentId — the agent to subscribe wakes for
 * @param handler — callback invoked for each wake
 * @returns unsubscribe function
 */
export async function subscribeWakes(
  agentId: string,
  handler: WakeHandler,
): Promise<() => void> {
  const nc = await connectNats();
  await ensureWakeStream(nc);

  const subject = `${WAKE_SUBJECT_PREFIX}.${agentId}.>`;
  const consumerName = `wake-${agentId}-${Date.now().toString(36)}`;

  // Use plain NATS subscription (synchronous subscriber)
  const sub = nc.subscribe(subject);
  console.log(`[WakeBus] Subscribed: ${subject} (consumer=${consumerName})`);

  // Process messages in background
  (async () => {
    for await (const msg of sub) {
      try {
        const wake: WakePayload = JSON.parse(sc.decode(msg.data));
        await handler(wake);
      } catch (err) {
        console.error(`[WakeBus] Handler error on ${subject}:`, err);
      }
    }
  })();

  // Return unsubscribe function
  return () => {
    sub.unsubscribe();
    console.log(`[WakeBus] Unsubscribed: ${consumerName}`);
  };
}

// ── Stream depth (for health output) ────────────────────────────────

/**
 * Get wake stream depth, optionally filtered by agent.
 * Used by gateway /health endpoint for observability.
 * 
 * @param agentId — optional filter by agent id
 * @returns stream depth info
 */
export async function getWakeStreamDepth(agentId?: string): Promise<WakeStreamDepth> {
  const nc = await connectNats();

  try {
    const jsm = await nc.jetstreamManager();
    const info = await jsm.streams.info(WAKE_STREAM);

    if (agentId) {
      return {
        agent_id: agentId,
        message_count: (info as any).state?.msgs ?? (info as any).state?.messages ?? 0,
        byte_size: (info as any).state?.bytes ?? 0,
        last_message_at: ((info as any).state?.last_seq ?? 0) > 0
          ? new Date((info as any).state?.last_ts ?? 0).toISOString()
          : null,
      };
    }

    return {
      message_count: (info as any).state?.msgs ?? (info as any).state?.messages ?? 0,
      byte_size: (info as any).state?.bytes ?? 0,
      last_message_at: ((info as any).state?.last_seq ?? 0) > 0
        ? new Date((info as any).state?.last_ts ?? 0).toISOString()
        : null,
    };
  } catch {
    // Stream doesn't exist yet — return empty
    return {
      agent_id: agentId,
      message_count: 0,
      byte_size: 0,
      last_message_at: null,
    };
  }
}
