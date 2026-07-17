#!/usr/bin/env node
/**
 * A2A-Version Header Middleware — A2A Protocol v1.0.0
 * 
 * Validates A2A-Version header on every JSON-RPC request.
 * Per spec: all A2A requests MUST include A2A-Version header.
 * Rejects with 400 if header is missing or unsupported.
 * 
 * DITEMPA BUKAN DIBERI — Forged, Not Given
 */

const SUPPORTED_A2A_VERSIONS = new Set(['1.0', '1.0.0']);
const DEFAULT_A2A_VERSION = '1.0';

/**
 * Express middleware that validates A2A-Version header.
 * Configurable: can be set to required or optional.
 * 
 * @param {Object} options
 * @param {boolean} options.required - If true, reject requests without header (default: true for JSON-RPC routes)
 * @param {string|string[]} options.supportedVersions - Supported A2A versions
 */
function createA2AVersionMiddleware(options = {}) {
  const required = options.required !== false;
  const supported = new Set(
    Array.isArray(options.supportedVersions)
      ? options.supportedVersions
      : [options.supportedVersions || DEFAULT_A2A_VERSION]
  );

  return (req, res, next) => {
    // Public discovery GETs must not require A2A-Version (normative card is unauthenticated).
    const path = (req.path || req.url || '').split('?')[0];
    const isPublicDiscovery =
      req.method === 'GET' &&
      (/agent-card\.json$/.test(path) ||
        /\/agent\.json$/.test(path) ||
        /discovery-contract\.json$/.test(path) ||
        /routing-policy\.json$/.test(path) ||
        /a2a-discovery\.json$/.test(path) ||
        /peer-federation-contract\.json$/.test(path));
    if (isPublicDiscovery) {
      req.a2aVersion = DEFAULT_A2A_VERSION;
      res.setHeader('A2A-Version', DEFAULT_A2A_VERSION);
      return next();
    }

    const version = req.headers['a2a-version'] || req.headers['A2A-Version'];
    
    if (!version) {
      if (required) {
        return res.status(400).json({
          jsonrpc: '2.0',
          id: req.body?.id || null,
          error: {
            code: -32600,
            message: 'Invalid Request',
            data: {
              details: 'A2A-Version header is required. Set A2A-Version: 1.0',
              supportedVersions: [...supported],
            },
          },
        });
      }
      // Not required, skip validation but set default
      req.a2aVersion = DEFAULT_A2A_VERSION;
      return next();
    }

    // Normalise version string
    const normalizedVersion = version.trim();
    
    if (!supported.has(normalizedVersion)) {
      return res.status(400).json({
        jsonrpc: '2.0',
        id: req.body?.id || null,
        error: {
          code: -32600,
          message: 'Invalid Request',
          data: {
            details: `Unsupported A2A version: "${normalizedVersion}". Supported: ${[...supported].join(', ')}`,
            receivedVersion: normalizedVersion,
            supportedVersions: [...supported],
          },
        },
      });
    }

    // Set version on request for downstream use
    req.a2aVersion = normalizedVersion;
    
    // Set response header
    res.setHeader('A2A-Version', normalizedVersion);
    
    next();
  };
}

/**
 * A2A-Version response header middleware — sets A2A-Version on all responses
 * even if no middleware-level validation was required.
 */
function setA2AVersionResponseHeader(req, res, next) {
  res.setHeader('A2A-Version', req.a2aVersion || DEFAULT_A2A_VERSION);
  next();
}

module.exports = {
  createA2AVersionMiddleware,
  setA2AVersionResponseHeader,
  SUPPORTED_A2A_VERSIONS,
  DEFAULT_A2A_VERSION,
};
