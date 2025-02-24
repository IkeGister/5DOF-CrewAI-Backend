"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.api = void 0;
const https_1 = require("firebase-functions/v2/https");
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const api_1 = __importDefault(require("./routes/api"));
const auth_1 = require("./middleware/auth");
const app = (0, express_1.default)();
// Make config available
process.env.FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY = process.env.FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY;
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
exports.api = (0, https_1.onRequest)({
    memory: '256MiB',
    timeoutSeconds: 60,
    minInstances: 0
}, app);
//# sourceMappingURL=index.js.map