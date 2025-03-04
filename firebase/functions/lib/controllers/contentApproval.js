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
exports.updateGistAndLinks = exports.batchUpdateGists = exports.fetchUserLinks = exports.updateGistProductionStatus = exports.fetchUserGist = exports.fetchUserGists = void 0;
const firebaseService = __importStar(require("../services/firebase_service"));
const crewAIService_1 = require("../services/crewAIService");
/**
 * Fetch user gists
 *
 * @param req Express request
 * @param res Express response
 */
const fetchUserGists = async (req, res) => {
    try {
        const { userId } = req.params;
        if (!userId) {
            return res.status(400).json({ error: 'User ID is required' });
        }
        // Use the Firebase service to get user gists
        const gists = await firebaseService.getUserGists(userId);
        return res.status(200).json({
            success: true,
            gists
        });
    }
    catch (error) {
        console.error('Error fetching user gists:', error);
        return res.status(500).json({
            error: 'Failed to fetch user gists',
            message: error.message
        });
    }
};
exports.fetchUserGists = fetchUserGists;
/**
 * Fetch a specific gist for a user
 *
 * @param req Express request
 * @param res Express response
 */
const fetchUserGist = async (req, res) => {
    try {
        const { userId, gistId } = req.params;
        if (!userId || !gistId) {
            return res.status(400).json({ error: 'User ID and Gist ID are required' });
        }
        // Use the Firebase service to get the gist
        const gist = await firebaseService.getGist(userId, gistId);
        if (!gist) {
            return res.status(404).json({ error: 'Gist not found' });
        }
        return res.status(200).json({
            success: true,
            data: gist
        });
    }
    catch (error) {
        console.error('Error fetching user gist:', error);
        return res.status(500).json({
            error: 'Failed to fetch user gist',
            message: error.message
        });
    }
};
exports.fetchUserGist = fetchUserGist;
/**
 * Update gist production status
 *
 * @param req Express request
 * @param res Express response
 */
const updateGistProductionStatus = async (req, res) => {
    try {
        const { userId, gistId } = req.params;
        const { inProduction, production_status } = req.body;
        if (!gistId) {
            return res.status(400).json({ error: 'Gist ID is required' });
        }
        if (!userId) {
            return res.status(400).json({ error: 'User ID is required' });
        }
        if (typeof inProduction !== 'boolean') {
            return res.status(400).json({ error: 'inProduction must be a boolean' });
        }
        if (!['draft', 'review', 'published'].includes(production_status)) {
            return res.status(400).json({ error: 'Invalid production_status' });
        }
        // Use the Firebase service to update the gist status
        await firebaseService.updateGistStatus(userId, gistId, inProduction, production_status);
        // If moving to production, initiate CrewAI workflow
        if (inProduction && production_status === 'review') {
            // Get the gist data
            const gist = await firebaseService.getGist(userId, gistId);
            if (gist) {
                // Initiate CrewAI workflow
                try {
                    await crewAIService_1.crewAIService.initiateContentApproval(gist);
                }
                catch (error) {
                    console.error('Error initiating CrewAI workflow:', error);
                }
            }
        }
        return res.status(200).json({
            success: true,
            message: 'Gist production status updated successfully'
        });
    }
    catch (error) {
        console.error('Error updating gist production status:', error);
        return res.status(500).json({
            error: 'Failed to update gist production status',
            message: error.message
        });
    }
};
exports.updateGistProductionStatus = updateGistProductionStatus;
/**
 * Fetch user links
 *
 * @param req Express request
 * @param res Express response
 */
const fetchUserLinks = async (req, res) => {
    try {
        const { userId } = req.params;
        if (!userId) {
            return res.status(400).json({ error: 'User ID is required' });
        }
        // Use the Firebase service to get user links
        const links = await firebaseService.getUserLinks(userId);
        return res.status(200).json({
            success: true,
            links
        });
    }
    catch (error) {
        console.error('Error fetching user links:', error);
        return res.status(500).json({
            error: 'Failed to fetch user links',
            message: error.message
        });
    }
};
exports.fetchUserLinks = fetchUserLinks;
/**
 * Update multiple gists and their links in a batch operation
 *
 * @param req Express request
 * @param res Express response
 */
const batchUpdateGists = async (req, res) => {
    try {
        const { userId } = req.params;
        const { gistIds, inProduction, production_status } = req.body;
        if (!userId) {
            return res.status(400).json({ error: 'User ID is required' });
        }
        if (!gistIds || !Array.isArray(gistIds) || gistIds.length === 0) {
            return res.status(400).json({ error: 'gistIds must be a non-empty array' });
        }
        if (typeof inProduction !== 'boolean') {
            return res.status(400).json({ error: 'inProduction must be a boolean' });
        }
        if (!['draft', 'review', 'published'].includes(production_status)) {
            return res.status(400).json({ error: 'Invalid production_status' });
        }
        // Use the Firebase service to batch update gists
        await firebaseService.batchUpdateGists(userId, gistIds, inProduction, production_status);
        return res.status(200).json({
            success: true,
            message: 'Gists updated successfully'
        });
    }
    catch (error) {
        console.error('Error batch updating gists:', error);
        return res.status(500).json({
            error: 'Failed to batch update gists',
            message: error.message
        });
    }
};
exports.batchUpdateGists = batchUpdateGists;
/**
 * Update a gist and all its related links atomically
 *
 * @param req Express request
 * @param res Express response
 */
const updateGistAndLinks = async (req, res) => {
    try {
        const { userId, gistId } = req.params;
        const { inProduction, production_status } = req.body;
        if (!gistId) {
            return res.status(400).json({ error: 'Gist ID is required' });
        }
        if (!userId) {
            return res.status(400).json({ error: 'User ID is required' });
        }
        if (typeof inProduction !== 'boolean') {
            return res.status(400).json({ error: 'inProduction must be a boolean' });
        }
        if (!['draft', 'review', 'published'].includes(production_status)) {
            return res.status(400).json({ error: 'Invalid production_status' });
        }
        // Use the Firebase service to update the gist and its links
        await firebaseService.updateGistAndLinks(userId, gistId, inProduction, production_status);
        return res.status(200).json({
            success: true,
            message: 'Gist and related links updated successfully'
        });
    }
    catch (error) {
        console.error('Error updating gist and links:', error);
        return res.status(500).json({
            error: 'Failed to update gist and links',
            message: error.message
        });
    }
};
exports.updateGistAndLinks = updateGistAndLinks;
//# sourceMappingURL=contentApproval.js.map