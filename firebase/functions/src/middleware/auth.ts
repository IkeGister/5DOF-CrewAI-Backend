import { Request, Response, NextFunction } from 'express';
import * as admin from 'firebase-admin';

/**
 * Firebase Authentication Middleware
 * 
 * This middleware verifies Firebase ID tokens in the Authorization header.
 * It sets req.user with the decoded token data if authentication is successful.
 * 
 * @param req - Express request object
 * @param res - Express response object
 * @param next - Express next function
 */
export const authenticateUser = async (
  req: Request, 
  res: Response, 
  next: NextFunction
) => {
  // Log request information in development environment only
  if (process.env.NODE_ENV === 'development') {
    console.log(`${req.method} ${req.path} - Authenticating request`);
    
    // Create a sanitized copy of headers to avoid logging sensitive information
    const sanitizedHeaders = { ...req.headers };
    
    // Redact sensitive information
    ['authorization', 'cookie', 'x-auth-token'].forEach(header => {
      if (sanitizedHeaders[header]) {
        sanitizedHeaders[header] = '[REDACTED]';
      }
    });
    
    console.log('Headers:', JSON.stringify(sanitizedHeaders));
  }

  // Check if the request has an authorization header
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    res.status(401).json({ 
      success: false,
      error: 'Unauthorized', 
      message: 'Authentication required' 
    });
    return;
  }

  // Extract the token
  const idToken = authHeader.split('Bearer ')[1];

  try {
    // Verify the ID token
    const decodedToken = await admin.auth().verifyIdToken(idToken);
    
    // Set the user information on the request object
    req.user = decodedToken;
    
    // Continue to the next middleware or route handler
    next();
  } catch (error) {
    console.error('Error verifying Firebase ID token:', error);
    res.status(401).json({ 
      success: false,
      error: 'Unauthorized', 
      message: 'Invalid authentication token' 
    });
  }
};

/**
 * Service-to-Service Authentication Middleware
 * 
 * This middleware verifies the API key in the X-API-Key header.
 * It allows requests to proceed only if the API key is valid.
 * 
 * @param req - Express request object
 * @param res - Express response object
 * @param next - Express next function
 */
export const authenticateService = (
  req: Request, 
  res: Response, 
  next: NextFunction
) => {
  // Log request information in development environment only
  if (process.env.NODE_ENV === 'development') {
    console.log(`${req.method} ${req.path} - Authenticating service request`);
    
    // Create a sanitized copy of headers to avoid logging sensitive information
    const sanitizedHeaders = { ...req.headers };
    
    // Redact sensitive information
    ['authorization', 'cookie', 'x-api-key'].forEach(header => {
      if (sanitizedHeaders[header]) {
        sanitizedHeaders[header] = '[REDACTED]';
      }
    });
    
    console.log('Headers:', JSON.stringify(sanitizedHeaders));
    
    // Always skip validation in development mode
    console.log('Development mode: Skipping API key validation');
    return next();
  }
  
  // Skip validation in development if configured - this is now redundant but kept for backward compatibility
  if (process.env.NODE_ENV === 'development' && process.env.SKIP_API_KEY_VALIDATION === 'true') {
    console.log('Skipping API key validation in development mode');
    return next();
  }
  
  // Get service API key from environment variables
  const expectedApiKey = process.env.SERVICE_API_KEY;
  
  // Get API key from request header
  const apiKey = req.headers['x-api-key'];
  
  if (!apiKey || apiKey !== expectedApiKey) {
    console.error('Invalid or missing API key');
    return res.status(401).json({
      success: false,
      error: 'Unauthorized',
      message: 'Valid API key required for service-to-service communication'
    });
  }
  
  next();
};

// Add a type definition for the user property on the Request object
declare global {
  namespace Express {
    interface Request {
      user?: admin.auth.DecodedIdToken;
    }
  }
}
