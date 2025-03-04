import { Request, Response, NextFunction } from 'express';

/**
 * Trusted Backend Middleware
 * 
 * This middleware assumes all requests are coming from trusted backend services
 * and doesn't require an API key. For additional security, consider implementing:
 * 1. IP whitelisting
 * 2. VPC/network security
 * 3. Rate limiting
 * 
 * @param req - Express request object
 * @param res - Express response object
 * @param next - Express next function
 */
export const authenticateUser = (
  req: Request, 
  res: Response, 
  next: NextFunction
): void => {
  // Log request information in development environment only
  if (process.env.NODE_ENV === 'development') {
    console.log(`${req.method} ${req.path} - Trusted backend request`);
    
    // Create a sanitized copy of headers to avoid logging sensitive information
    const sanitizedHeaders = { ...req.headers };
    
    // Redact sensitive information
    if (sanitizedHeaders['x-api-key']) {
      sanitizedHeaders['x-api-key'] = '[REDACTED]';
    }
    
    // Redact other potential sensitive headers
    ['authorization', 'cookie', 'x-auth-token'].forEach(header => {
      if (sanitizedHeaders[header]) {
        sanitizedHeaders[header] = '[REDACTED]';
      }
    });
    
    console.log('Headers:', JSON.stringify(sanitizedHeaders));
  }

  // All requests are automatically trusted
  // No API key validation is performed
  return next();
};
