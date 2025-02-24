"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.crewAIService = void 0;
const axios_1 = __importDefault(require("axios"));
const CREW_AI_BASE_URL = process.env.CREW_AI_BASE_URL || 'http://localhost:5000';
const API_KEY = process.env.FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY;
exports.crewAIService = {
    async initiateContentApproval(gistData) {
        try {
            const response = await axios_1.default.post(`${CREW_AI_BASE_URL}/api/content/approve`, gistData, {
                headers: {
                    'X-API-Key': API_KEY,
                    'Content-Type': 'application/json'
                }
            });
            return response.data;
        }
        catch (error) {
            console.error('Error calling CrewAI service:', error);
            throw error;
        }
    }
};
//# sourceMappingURL=crewAIService.js.map