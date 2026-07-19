/**
 * CloudEvents NATS Bridge — AAA → A-FORGE event propagation
 * 
 * Forged: 2026-07-19 by FORGE (000Ω)
 * Doctrine: DITEMPA BUKAN DIBERI
 * 
 * Reads CloudEvents from arifOS kernel, publishes to NATS subjects.
 * A-FORGE consumes via forge_* event listeners.
 * 
 * Event types (18 federation events):
 *   arifos.session.init, arifos.session.expire
 *   arifos.judge.seal, arifos.judge.hold, arifos.judge.sabar, arifos.judge.void
 *   arifos.vault.append
 *   arifos.cooling.drift, arifos.cooling.pattern
 *   aforge.execute.start, aforge.execute.complete, aforge.execute.abort
 *   geox.claim.create, geox.claim.seal
 *   wealth.capital.compute
 *   well.vitality.assess
 *   federation.organ.health, federation.888.hold
 */

import { connect, StringCodec, type NatsConnection } from 'nats';

const NATS_URL = process.env.NATS_URL || 'nats://localhost:4222';
const sc = StringCodec();

interface CloudEvent {
  specversion: string;
  type: string;
  source: string;
  id: string;
  time: string;
  subject?: string;
  data?: Record<string, unknown>;
  datacontenttype?: string;
}

let nc: NatsConnection | null = null;

export async function connectNats(): Promise<NatsConnection> {
  if (!nc) {
    nc = await connect({ servers: NATS_URL });
    console.log(`[CloudEventsBridge] Connected to NATS at ${NATS_URL}`);
  }
  return nc;
}

export async function publishCloudEvent(event: CloudEvent): Promise<void> {
  const nats = await connectNats();
  const subject = `federation.events.${event.type.replace(/\./g, '.')}`;
  const payload = JSON.stringify(event);
  nats.publish(subject, sc.encode(payload));
  console.log(`[CloudEventsBridge] Published: ${event.type} → ${subject}`);
}

export async function subscribeToEvents(
  eventType: string,
  handler: (event: CloudEvent) => void
): Promise<void> {
  const nats = await connectNats();
  const subject = `federation.events.${eventType.replace(/\./g, '.')}`;
  const sub = nats.subscribe(subject);
  console.log(`[CloudEventsBridge] Subscribed to: ${subject}`);
  
  (async () => {
    for await (const msg of sub) {
      try {
        const event: CloudEvent = JSON.parse(sc.decode(msg.data));
        handler(event);
      } catch (err) {
        console.error(`[CloudEventsBridge] Parse error on ${subject}:`, err);
      }
    }
  })();
}

/**
 * Forward arifOS kernel events to federation NATS bus.
 * Called by arifOS after each kernel operation.
 */
export async function bridgeKernelEvent(
  eventType: string,
  source: string,
  data?: Record<string, unknown>
): Promise<void> {
  const event: CloudEvent = {
    specversion: '1.0.2',
    type: eventType,
    source: source,
    id: `${eventType}-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`,
    time: new Date().toISOString(),
    datacontenttype: 'application/json',
    data,
  };
  await publishCloudEvent(event);
}

export async function closeNats(): Promise<void> {
  if (nc) {
    await nc.drain();
    nc = null;
  }
}
