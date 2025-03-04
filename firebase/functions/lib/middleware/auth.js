"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.authenticateService = exports.authenticateUser = void 0;
const admin = __importStar(require("firebase-admin"));
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
const authenticateUser = async (req, res, next) => {
    // Log request information in development environment only
    if (process.env.NODE_ENV === 'development') {
        console.log(`${req.method} ${req.path} - Authenticating request`);
        // Create a sanitized copy of headers to avoid logging sensitive information
        const sanitizedHeaders = Object.assign({}, req.headers);
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
    }
    catch (error) {
        console.error('Error verifying Firebase ID token:', error);
        res.status(401).json({
            success: false,
            error: 'Unauthorized',
            message: 'Invalid authentication token'
        });
    }
};
exports.authenticateUser = authenticateUser;
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
const authenticateService = (req, res, next) => {
    // Log request information in development environment only
    if (process.env.NODE_ENV === 'development') {
        console.log(`${req.method} ${req.path} - Authenticating service request`);
        // Create a sanitized copy of headers to avoid logging sensitive information
        const sanitizedHeaders = Object.assign({}, req.headers);
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
exports.authenticateService = authenticateService;
//# sourceMappingURL=auth.js.map