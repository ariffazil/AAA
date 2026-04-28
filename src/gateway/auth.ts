import { Request, Response, NextFunction } from 'express';
import { ERROR_CODES } from './schema';

export interface AuthContext {
  authenticated: boolean;
  authScheme?: string;
  clientId?: string;
  scopes?: string[];
}

export function createAuthMiddleware() {
  return (req: Request, res: Response, next: () => void): void => {
    const authHeader = req.headers.authorization;
    const apiKeyHeader = req.headers['x-api-key'];
    
    // Skip auth for public endpoints
    const publicPaths = [
      '/.well-known/agent.json',
      '/agent.json',
      '/health',
    ];
    
    if (publicPaths.includes(req.path)) {
      (req as any).authContext = { authenticated: false };
      return next();
    }

    // Critical Trust Boundary: Validate Bearer/API Key
    if (authHeader?.startsWith('Bearer ')) {
      const token = authHeader.slice(7);
      if (token === process.env.A2A_TOKEN || process.env.NODE_ENV === 'development') {
        (req as any).authContext = {
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
        (req as any).authContext = {
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
    (req as any).authContext = { authenticated: false };
    next();
  };
}
