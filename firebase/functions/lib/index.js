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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.api = void 0;
const functions = __importStar(require("firebase-functions"));
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const api_1 = __importDefault(require("./routes/api"));
// Create Express app
const app = (0, express_1.default)();
// In Firebase Functions v2, environment variables are set directly in the Firebase console
// or via the firebase.json file, so we don't need to use functions.config() anymore
// Set SKIP_API_KEY_VALIDATION to true in development mode
if (process.env.NODE_ENV === 'development') {
    process.env.SKIP_API_KEY_VALIDATION = 'true';
    console.log('Development mode: API key validation is skipped');
}
// Optional: Configure IP restriction for additional security
// This can be enabled in production to restrict access to specific IP addresses
// const allowedIPs = functions.config().security?.allowed_ips?.split(',') || [];
// app.use((req, res, next) => {
//   const clientIP = req.ip || req.connection.remoteAddress;
//   if (allowedIPs.length === 0 || allowedIPs.includes(clientIP)) {
//     return next();
//   }
//   return res.status(403).json({ error: 'Forbidden', message: 'IP not allowed' });
// });
// Optional: Configure rate limiting for additional security
// This can be enabled in production to prevent abuse
// const rateLimit = require('express-rate-limit');
// const limiter = rateLimit({
//   windowMs: 15 * 60 * 1000, // 15 minutes
//   max: 100, // limit each IP to 100 requests per windowMs
//   message: { error: 'Too many requests', message: 'Please try again later' }
// });
// app.use(limiter);
// Middleware
app.use((0, cors_1.default)({ origin: true }));
app.use(express_1.default.json());
// Routes
app.use('/api', api_1.default);
// Error handling
app.use((err, req, res, next) => {
    console.error('Unhandled error:', err);
    res.status(500).json({
        success: false,
        error: 'Internal Server Error',
        message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
    });
});
// Export the Express app as a Firebase Cloud Function
exports.api = functions.https.onRequest(app);
// Start the server locally in development mode
if (process.env.NODE_ENV === 'development') {
    const PORT = process.env.PORT || 3000;
    // Set default values for environment variables if not already set
    if (!process.env.SERVICE_API_KEY) {
        process.env.SERVICE_API_KEY = 'dev-service-api-key';
        console.log('Using default SERVICE_API_KEY for development');
    }
    if (!process.env.CREW_AI_API_KEY) {
        process.env.CREW_AI_API_KEY = 'dev-crewai-api-key';
        console.log('Using default CREW_AI_API_KEY for development');
    }
    if (!process.env.CREW_AI_BASE_URL) {
        process.env.CREW_AI_BASE_URL = 'http://localhost:5000';
        console.log(`Using default CREW_AI_BASE_URL: ${process.env.CREW_AI_BASE_URL}`);
    }
    app.listen(PORT, () => {
        console.log(`Server running in development mode on port ${PORT}`);
        console.log(`API available at: http://localhost:${PORT}/api`);
    });
}
//# sourceMappingURL=index.js.map