/**
 * A2A Client Demo
 * 
 * Examples of using the A2A client to dispatch tasks to external agents.
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

import { A2AClient, createA2AClient, dispatchToAgent, dispatchWithStreaming } from './client.js';

// Example 1: Basic message send
async function exampleBasicSend(): Promise<void> {
  console.log('\n📤 Example 1: Basic Message Send\n');

  const client = createA2AClient('http://localhost:3001');

  const task = await client.sendMessage({
    role: 'user',
    parts: [{ kind: 'text', text: 'Hello, what can you do?' }],
    messageId: crypto.randomUUID(),
  });

  console.log('Task created:', task.id);
  console.log('State:', task.status.state);
  console.log('Response:', task.status.message?.parts[0]?.text);
}

// Example 2: Using preset agents
async function examplePresetAgents(): Promise<void> {
  console.log('\n📤 Example 2: Preset Agent Dispatch\n');

  try {
    // Note: This will fail if the preset agents aren't running
    // In production, you would configure the environment variables
    const task = await dispatchToAgent('GEOX', 'Analyze the porosity data for Well A-1');
    console.log('Task dispatched to GEOX:', task.id);
  } catch (error) {
    console.log('Preset agent not available (expected if not running)');
  }
}

// Example 3: Streaming response
async function exampleStreaming(): Promise<void> {
  console.log('\n📤 Example 3: Streaming Response\n');

  const client = createA2AClient('http://localhost:3001');

  const stream = await client.sendMessageStream({
    role: 'user',
    parts: [{ kind: 'text', text: 'Generate a detailed report on reservoir quality' }],
    messageId: crypto.randomUUID(),
  });

  console.log('Streaming started...');

  for await (const response of stream) {
    console.log('Event received:', response.event.kind);
    
    if (response.event.kind === 'status-update') {
      console.log('State:', response.event.status?.state);
      if (response.event.status?.message?.parts[0]?.text) {
        console.log('Message:', response.event.status.message.parts[0].text);
      }
    }
    
    if (response.event.final) {
      console.log('Stream complete');
      break;
    }
  }
}

// Example 4: Subscribe to task updates
async function exampleSubscribe(): Promise<void> {
  console.log('\n📤 Example 4: Subscribe to Task Updates\n');

  const client = createA2AClient('http://localhost:3001');

  // First create a task
  const task = await client.sendMessage({
    role: 'user',
    parts: [{ kind: 'text', text: 'Start a long-running analysis' }],
    messageId: crypto.randomUUID(),
  });

  console.log('Task created:', task.id);

  // Then subscribe to updates
  const cancel = await client.subscribeToTask(task.id, (event) => {
    console.log('Update received:', event);
  });

  // After some time, cancel subscription
  setTimeout(() => {
    console.log('Unsubscribing...');
    cancel();
  }, 5000);
}

// Example 5: Task management
async function exampleTaskManagement(): Promise<void> {
  console.log('\n📤 Example 5: Task Management\n');

  const client = createA2AClient('http://localhost:3001');

  // Create a task
  const task = await client.sendMessage({
    role: 'user',
    parts: [{ kind: 'text', text: 'Perform some analysis' }],
    messageId: crypto.randomUUID(),
  });

  console.log('Created task:', task.id);

  // Get task status
  const retrieved = await client.getTask(task.id);
  if (retrieved) {
    console.log('Retrieved state:', retrieved.status.state);
  }

  // Cancel task
  const canceled = await client.cancelTask(task.id);
  console.log('Cancel successful:', canceled);

  // Try to get canceled task
  const afterCancel = await client.getTask(task.id);
  console.log('State after cancel:', afterCancel?.status.state);
}

// Example 6: Custom auth
async function exampleCustomAuth(): Promise<void> {
  console.log('\n📤 Example 6: Custom Authentication\n');

  const client = new A2AClient({
    baseUrl: 'http://localhost:3001',
    auth: {
      type: 'bearer',
      token: 'my-secret-token',
    },
  });

  const task = await client.sendMessage({
    role: 'user',
    parts: [{ kind: 'text', text: 'Hello with auth' }],
    messageId: crypto.randomUUID(),
  });

  console.log('Task with auth:', task.id);
}

// Run all examples
async function runAllExamples(): Promise<void> {
  console.log('🚀 A2A Client Demo');
  console.log('==================\n');

  console.log('Make sure the A2A server is running: npm run a2a:server');

  await exampleBasicSend().catch(console.error);
  await examplePresetAgents().catch(console.error);
  await exampleStreaming().catch(console.error);
  await exampleSubscribe().catch(console.error);
  await exampleTaskManagement().catch(console.error);
  await exampleCustomAuth().catch(console.error);

  console.log('\n✨ Demo complete\n');
}

// Run if executed directly
runAllExamples().catch(console.error);

export {
  exampleBasicSend,
  examplePresetAgents,
  exampleStreaming,
  exampleSubscribe,
  exampleTaskManagement,
  exampleCustomAuth,
};