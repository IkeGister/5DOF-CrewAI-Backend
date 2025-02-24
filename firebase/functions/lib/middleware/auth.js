"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.authenticateUser = void 0;
const authenticateUser = (req, res, next) => {
    console.log('Headers:', req.headers);
    console.log('API Key from request:', req.headers['x-api-key']);
    console.log('Config API Key:', process.env.FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY);
    const apiKey = req.headers['x-api-key'];
    const configApiKey = process.env.FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY;
    if (!apiKey) {
        return res.status(401).json({ error: 'Unauthorized - No token provided' });
    }
    if (apiKey !== configApiKey) {
        return res.status(401).json({ error: 'Unauthorized - Invalid token' });
    }
    return next();
};
exports.authenticateUser = authenticateUser;
//# sourceMappingURL=auth.js.map