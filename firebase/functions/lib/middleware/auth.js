"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.authenticateUser = void 0;
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
const authenticateUser = (req, res, next) => {
    // Log request information in development environment only
    if (process.env.NODE_ENV === 'development') {
        console.log(`${req.method} ${req.path} - Trusted backend request`);
        console.log('Headers:', JSON.stringify(req.headers));
    }
    // All requests are automatically trusted
    // No API key validation is performed
    return next();
};
exports.authenticateUser = authenticateUser;
//# sourceMappingURL=auth.js.map