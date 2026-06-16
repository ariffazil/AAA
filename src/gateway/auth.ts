import { Request, Response, NextFunction, RequestHandler } from 'express';
import { ERROR_CODES } from './schema';

export interface AuthContext {
  authenticated: boolean;
  authScheme?: string;
  clientId?: string;
  scopes?: string[];
}

export type AuthenticatedRequest = Request & {
  authContext?: AuthContext;
};

export function createAuthMiddleware(): RequestHandler {
  return (req: Request, res: Response, next: NextFunction): void => {
    const authReq = req as AuthenticatedRequest;
    const authHeader = req.headers.authorization;
    const apiKeyHeader = req.headers['x-api-key'];
    
    // Skip auth for public endpoints
    const publicPaths = [
      '/.well-known/a2a-discovery.json',
      '/.well-known/agent-card.json',
      '/.well-known/agent.json',
      '/.well-known/a2a-routing-policy.json',
      '/a2a/discovery-contract.json',
      '/a2a/agent-card.json',
      '/a2a/agent.json',
      '/a2a/routing-policy.json',
      '/agent-card.json',
      '/agent.json',
      '/health',
    ];
    
    if (publicPaths.includes(req.path)) {
      authReq.authContext = { authenticated: false };
      return next();
    }

    // Critical Trust Boundary: Validate Bearer/API Key
    if (authHeader?.startsWith('Bearer ')) {
      const token = authHeader.slice(7);
      if (token === process.env.A2A_TOKEN || process.env.NODE_ENV === 'development') {
        authReq.authContext = {
          authenticated: true,
          authScheme: 'bearer',
          clientId: 'authenticated-client',
          scopes: ['read', 'write', 'delegate'],
        };
        return next();
      }
    }

    if (apiKeyHeader) {
      if (apiKeyHeader === process.env.A2A_API_KEY || process.env.NODE_ENV === 'development') {
        authReq.authContext = {
          authenticated: true,
          authScheme: 'apiKey',
          clientId: 'api-client',
          scopes: ['read', 'write'],
        };
        return next();
      }
    }

    // Reject in production if no valid auth
    if (process.env.NODE_ENV === 'production') {
      res.status(401).json({
        jsonrpc: '2.0',
        id: 0,
        error: { 
          code: ERROR_CODES.AUTHENTICATED_EXTENDED_CARD_NOT_CONFIGURED, 
          message: 'Authentication required' 
        }
      });
      return;
    }

    // Allow in development
    authReq.authContext = { authenticated: false };
    next();
  };
}
