"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.crewAIService = void 0;
const axios_1 = __importDefault(require("axios"));
const CREW_AI_BASE_URL = process.env.CREW_AI_BASE_URL || 'http://localhost:5000';
exports.crewAIService = {
    async initiateContentApproval(gistData) {
        try {
            const response = await axios_1.default.post(`${CREW_AI_BASE_URL}/api/content/approve`, gistData);
            return response.data;
        }
        catch (error) {
            console.error('Error calling CrewAI service:', error);
            throw error;
        }
    }
};
//# sourceMappingURL=crewAIService.js.map