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
const auth_1 = require("./middleware/auth");
// Create Express app
const app = (0, express_1.default)();
// Make config available
process.env.FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY = process.env.FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY;
// IP restriction middleware - uncomment and configure if needed
// const ALLOWED_IPS = ['123.456.789.0']; // Replace with your actual allowed IPs
// app.use((req, res, next) => {
//   const clientIp = req.ip || req.headers['x-forwarded-for'] || req.connection.remoteAddress;
//   if (!ALLOWED_IPS.includes(clientIp)) {
//     console.warn(`Access denied for IP: ${clientIp}`);
//     return res.status(403).json({
//       success: false,
//       error: 'Access denied'
//     });
//   }
//   next();
// });
// Rate limiting - uncomment if needed
// const RATE_LIMIT_WINDOW_MS = 15 * 60 * 1000; // 15 minutes
// const MAX_REQUESTS_PER_WINDOW = 100; // 100 requests per 15 minutes
// 
// app.use((req, res, next) => {
//   // Simple in-memory rate limiter
//   // For production, use redis or a proper rate limiting library
//   const now = Date.now();
//   const key = req.ip || 'unknown';
//   
//   if (!global.rateLimiter) {
//     global.rateLimiter = {};
//   }
//   
//   if (!global.rateLimiter[key]) {
//     global.rateLimiter[key] = {
//       count: 0,
//       resetAt: now + RATE_LIMIT_WINDOW_MS
//     };
//   }
//   
//   if (now > global.rateLimiter[key].resetAt) {
//     global.rateLimiter[key] = {
//       count: 1,
//       resetAt: now + RATE_LIMIT_WINDOW_MS
//     };
//   } else {
//     global.rateLimiter[key].count++;
//   }
//   
//   if (global.rateLimiter[key].count > MAX_REQUESTS_PER_WINDOW) {
//     return res.status(429).json({
//       success: false,
//       error: 'Too many requests, please try again later'
//     });
//   }
//   
//   next();
// });
// Middleware
app.use((0, cors_1.default)({ origin: true }));
app.use(express_1.default.json());
// Authentication middleware for all routes
app.use(auth_1.authenticateUser);
// Routes
app.use('/api', api_1.default);
// Error handling
app.use((err, req, res, _next) => {
    console.error(err);
    res.status(500).json({
        success: false,
        error: 'Internal server error'
    });
});
// Export the Express app as a Firebase Cloud Function
exports.api = functions.https.onRequest(app);
// If running locally, start the server
if (process.env.NODE_ENV === 'development') {
    const PORT = process.env.PORT || 3000;
    app.listen(PORT, () => {
        console.log(`Server running on port ${PORT}`);
    });
}
//# sourceMappingURL=index.js.map