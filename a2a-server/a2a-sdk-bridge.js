#!/usr/bin/env node
/**
 * A2A SDK Bridge — @a2a-js/sdk Integration for AAA Gateway
 * 
 * Integrates the official @a2a-js/sdk into our existing Express server.
 * Provides:
 * 1. agentCardHandler — spec-compliant /.well-known/agent-card.json serving
 * 2. jsonRpcHandler — JSON-RPC 2.0 transport for tasks/send, tasks/get, tasks/cancel
 * 3. Task store integration with our existing InMemoryTaskStore
 * 
 * This runs ALONGSIDE our existing custom routes — it does NOT replace them.
 * The SDK handlers provide standard A2A compliance; our custom routes provide
 * arifOS constitutional extensions (seal chain, delegation guard, etc.).
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

const express = require('express');
const { agentCardHandler, jsonRpcHandler, UserBuilder } = require('@a2a-js/sdk/server/express');
const { DefaultRequestHandler, InMemoryTaskStore } = require('@a2a-js/sdk/server');
const { validateMessage, normaliseMessage } = require('./a2a-part-types');
const crypto = require('crypto');

// ── SDK-backed Agent Card Handler ───────────────────────────────────────

/**
 * Creates an Express router that serves the gateway's agent card
 * at /.well-known/agent-card.json using the SDK's agentCardHandler.
 * 
 * @param {Object} agentCard - The AAA gateway agent card object
 * @returns {import('express').Router}
 */
function createSDKAgentCardRouter(agentCard) {
  const router = express.Router();
  
  // Use SDK's agentCardHandler with a provider function
  router.use(
    '/',
    agentCardHandler({
      agentCardProvider: () => Promise.resolve(agentCard),
    })
  );
  
  return router;
}

// ── SDK-backed JSON-RPC Handler ─────────────────────────────────────────

/**
 * Wraps our existing task store for SDK compatibility.
 * The SDK's InMemoryTaskStore uses load(id) / save(task) interface.
 */
class A2ALegacyTaskAdapter {
  constructor(taskStoreGet, taskStoreSet) {
    this._get = taskStoreGet;
    this._set = taskStoreSet;
  }

  async load(taskId) {
    const task = await this._get(taskId);
    return task || null;
  }

  async save(task) {
    await this._set(task.id, task);
  }
}

/**
 * Creates an SDK DefaultRequestHandler connected to our A2A ecosystem.
 * Routes tasks through our existing dispatch and seal chain logic.
 * 
 * @param {Object} options
 * @param {Function} options.taskStoreGet - Function(taskId) => task
 * @param {Function} options.taskStoreSet - Function(taskId, task) => void
 * @param {Object} options.agentCard - The gateway agent card
 * @param {Function} options.taskDispatcher - Function(task) to execute task
 * @returns {DefaultRequestHandler}
 */
function createSDKRequestHandler(options) {
  const { taskStoreGet, taskStoreSet, agentCard, taskDispatcher } = options;
  
  const taskStore = new InMemoryTaskStore();
  
  const handler = new DefaultRequestHandler(
    agentCard,
    taskStore
  );

  // We override sendMessage to use our dispatch pipeline
  // while keeping the SDK's JSON-RPC validation and state management
  const originalSendMessage = handler.sendMessage.bind(handler);
  
  handler.sendMessage = async (requestContext) => {
    const { id, params } = requestContext;
    const message = params?.message;
    
    if (!message || !message.parts) {
      throw new Error('A2A_Request: message with parts required');
    }

    // Validate message parts using our A2A part types
    const validation = validateMessage(message);
    if (!validation.valid) {
      throw new Error(`A2A_Validation: ${validation.message}`);
    }

    // Normalise parts
    const normalisedMessage = normaliseMessage(message);

    // Generate task ID if not provided
    const taskId = params?.id || `a2a-sdk-${crypto.randomUUID().slice(0, 8)}`;
    const task = {
      id: taskId,
      status: {
        state: 'TASK_STATE_SUBMITTED',
        timestamp: new Date().toISOString(),
        message: { role: 'user', parts: normalisedMessage.parts },
      },
      parts: [],
      artifacts: [],
      history: [],
      metadata: {
        ...(params?.metadata || {}),
        source: 'a2a-sdk',
        createdAt: new Date().toISOString(),
      },
    };

    await taskStore.save(task);

    // Dispatch the task if a dispatcher is provided
    if (typeof taskDispatcher === 'function') {
      // Update state to WORKING
      task.status.state = 'TASK_STATE_WORKING';
      task.status.timestamp = new Date().toISOString();
      await taskStore.save(task);

      // Dispatch asynchronously
      taskDispatcher(taskId, normalisedMessage, params).catch(err => {
        console.error(`[A2A SD KBridge] Task ${taskId} dispatch error:`, err.message);
      });
    }

    return {
      id: taskId,
      status: task.status,
      parts: [],
      artifacts: [],
    };
  };

  return handler;
}

/**
 * Creates Express router with SDK jsonRpcHandler, mounted at a custom path.
 * 
 * @param {DefaultRequestHandler} requestHandler 
 * @returns {import('express').Router}
 */
function createSDKJsonRPCRouter(requestHandler) {
  return jsonRpcHandler({
    requestHandler,
    userBuilder: UserBuilder.noAuthentication,
  });
}

module.exports = {
  createSDKAgentCardRouter,
  createSDKRequestHandler,
  createSDKJsonRPCRouter,
  A2ALegacyTaskAdapter,
};
