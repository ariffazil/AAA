#!/usr/bin/env node
/**
 * A2A Part Types — A2A Protocol v1.0.0
 * 
 * Implements the A2A protobuf oneof discriminator pattern for parts:
 * - TextPart: { type: "text", text: string }
 * - FilePart: { type: "file", mimeType: string, fileUri?: string, fileData?: { bytes: string, mimeType?: string } }
 * - DataPart: { type: "data", data: object }
 * 
 * Per A2A spec §3.3: Parts use protobuf oneof with the field name as type discriminator.
 * The SDK uses "TextPart", "FilePart", "DataPart" as type markers, but for HTTP JSON
 * transport the wire format uses "type" field for backward compatibility.
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

// ── Constants ────────────────────────────────────────────────────────────

const PART_TYPES = {
  TEXT: 'text',
  FILE: 'file',
  DATA: 'data',
};

const VALID_PART_TYPES = new Set(Object.values(PART_TYPES));
const MAX_TEXT_LENGTH = 50000;
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB for base64 file data
const MAX_PARTS = 50;

// ── Part Validators ──────────────────────────────────────────────────────

function validateTextPart(part) {
  if (typeof part.text !== 'string') {
    return { valid: false, message: 'TextPart requires string text field' };
  }
  if (part.text.length > MAX_TEXT_LENGTH) {
    return { valid: false, message: `TextPart text exceeds ${MAX_TEXT_LENGTH} characters` };
  }
  return { valid: true };
}

function validateFilePart(part) {
  if (typeof part.mimeType !== 'string' || !part.mimeType) {
    return { valid: false, message: 'FilePart requires string mimeType field' };
  }
  // Must have either fileUri or fileData (or both per spec)
  if (!part.fileUri && !part.fileData) {
    return { valid: false, message: 'FilePart requires fileUri or fileData' };
  }
  if (part.fileUri && typeof part.fileUri !== 'string') {
    return { valid: false, message: 'FilePart fileUri must be a string' };
  }
  if (part.fileData) {
    if (typeof part.fileData !== 'object') {
      return { valid: false, message: 'FilePart fileData must be an object' };
    }
    if (typeof part.fileData.bytes !== 'string') {
      return { valid: false, message: 'FilePart fileData.bytes must be a base64 string' };
    }
    // Size check
    if (part.fileData.bytes.length > MAX_FILE_SIZE) {
      return { valid: false, message: `FilePart fileData.bytes exceeds ${MAX_FILE_SIZE} bytes` };
    }
  }
  return { valid: true };
}

function validateDataPart(part) {
  if (part.data === undefined || part.data === null) {
    return { valid: false, message: 'DataPart requires data field' };
  }
  if (typeof part.data !== 'object') {
    return { valid: false, message: 'DataPart data must be an object (JSON)' };
  }
  return { valid: true };
}

// ── Main Validator ───────────────────────────────────────────────────────

/**
 * Validate a single message part according to A2A v1.0.0 Part types.
 * Accepts both "type" (canonical) and "kind" (legacy compatibility).
 * 
 * @param {Object} part
 * @returns {{ valid: boolean, message?: string }}
 */
function validatePart(part) {
  if (!part || typeof part !== 'object') {
    return { valid: false, message: 'Each part must be an object' };
  }

  // Determine discriminator — A2A uses field name as type marker
  // "type" is the canonical field (HTTP JSON transport)
  // "kind" is legacy backward compat
  const discriminator = part.type || part.kind;
  
  if (!discriminator || typeof discriminator !== 'string') {
    return { valid: false, message: 'Each message part must have a string type field' };
  }

  const normalizedType = discriminator.toLowerCase();
  
  if (!VALID_PART_TYPES.has(normalizedType)) {
    return { 
      valid: false, 
      message: `Unknown part type: "${discriminator}". Allowed: ${[...VALID_PART_TYPES].join(', ')}` 
    };
  }

  // Set normalised type back for downstream consumers
  part._normalizedType = normalizedType;

  switch (normalizedType) {
    case PART_TYPES.TEXT:
      return validateTextPart(part);
    case PART_TYPES.FILE:
      return validateFilePart(part);
    case PART_TYPES.DATA:
      return validateDataPart(part);
    default:
      return { valid: false, message: `Unknown part type: ${normalizedType}` };
  }
}

/**
 * Validate an A2A Message containing parts.
 * 
 * @param {Object} message - The message object with parts array
 * @returns {{ valid: boolean, message?: string }}
 */
function validateMessage(message) {
  if (!message || typeof message !== 'object') {
    return { valid: false, message: 'message must be an object' };
  }
  if (!message.parts || !Array.isArray(message.parts)) {
    return { valid: false, message: 'message.parts must be an array' };
  }
  if (message.parts.length > MAX_PARTS) {
    return { valid: false, message: `message.parts exceeds maximum of ${MAX_PARTS}` };
  }
  if (message.parts.length === 0) {
    return { valid: false, message: 'message.parts must not be empty' };
  }

  for (let i = 0; i < message.parts.length; i++) {
    const result = validatePart(message.parts[i]);
    if (!result.valid) {
      return { valid: false, message: `parts[${i}]: ${result.message}` };
    }
  }

  return { valid: true };
}

/**
 * Extract plain text from a message's parts.
 * Concatenates all TextPart text fields.
 * 
 * @param {Object} message 
 * @param {Object} options - { maxLength, maxParts }
 * @returns {string}
 */
function extractText(message, options = {}) {
  if (!message || !message.parts) return '';
  const maxLength = options.maxLength || MAX_TEXT_LENGTH;
  const parts = Array.isArray(message.parts) ? message.parts : [];
  
  return parts
    .filter(p => p && (p.type === 'text' || p.kind === 'text') && typeof p.text === 'string')
    .map(p => p.text.replace(/\x00/g, ''))
    .join(' ')
    .slice(0, maxLength);
}

/**
 * Normalise a part to canonical A2A format.
 * Handles legacy "kind" → "type" migration.
 * 
 * @param {Object} part
 * @returns {Object} Normalised part
 */
function normalisePart(part) {
  if (!part || typeof part !== 'object') return part;
  
  const normalised = { ...part };
  
  // If using legacy "kind", promote to "type"
  if (part.kind && !part.type) {
    normalised.type = part.kind;
  }
  
  // Ensure type is canonical lowercase (except protobuf names like "TextPart")
  // A2A wire format uses lowercase types for HTTP JSON transport
  if (normalised.type && !normalised.type.startsWith('Text') && !normalised.type.startsWith('File') && !normalised.type.startsWith('Data')) {
    normalised.type = normalised.type.toLowerCase();
  }
  
  // Set _discriminator for internal routing
  normalised._discriminator = normalised.type;
  
  return normalised;
}

/**
 * Normalise all parts in a message.
 * 
 * @param {Object} message
 * @returns {Object} Message with normalised parts
 */
function normaliseMessage(message) {
  if (!message || !message.parts) return message;
  return {
    ...message,
    parts: message.parts.map(normalisePart),
  };
}

module.exports = {
  PART_TYPES,
  VALID_PART_TYPES,
  validatePart,
  validateMessage,
  extractText,
  normalisePart,
  normaliseMessage,
  MAX_TEXT_LENGTH,
  MAX_PARTS,
};
