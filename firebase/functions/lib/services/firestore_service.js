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
exports.firestoreService = void 0;
const firebase_1 = require("../config/firebase");
const admin = __importStar(require("firebase-admin"));
exports.firestoreService = {
    /**
     * USE CASE 1: FETCH GISTS
     * Retrieves all gists for a given user, handling multiple document structure formats
     *
     * This function is designed to be flexible with different data structures:
     * 1. If userData is an array → Treats entire array as gists
     * 2. If userData has a 'gists' field with an array → Uses this array as gists
     * 3. If userData has numeric keys → Treats values of numeric keys as gists
     * 4. If userData contains gist-like fields → Treats the document itself as a single gist
     * 5. Fallback: Attempts to fetch from API directly
     *
     * @param userId - The ID of the user whose gists to retrieve
     * @returns An object containing an array of gists and their count
     * @throws Error if user not found or retrieval fails
     */
    async getUserGists(userId) {
        try {
            console.log(`Getting gists for user: ${userId}`);
            const userRef = firebase_1.db.collection('users').doc(userId);
            const doc = await userRef.get();
            if (!doc.exists) {
                console.log(`No user found with ID: ${userId}`);
                throw new Error('User not found');
            }
            const userData = doc.data();
            console.log(`User data retrieved, keys: ${Object.keys(userData || {}).join(', ')}`);
            let gists = [];
            // Case 1: Handle case where the data is directly an array of gists
            if (Array.isArray(userData)) {
                console.log('User data is directly an array');
                gists = userData;
            }
            // Case 2: Handle case where gists are in a 'gists' field
            else if (userData && 'gists' in userData && Array.isArray(userData.gists)) {
                console.log('User data has gists array');
                gists = userData.gists;
            }
            // Case 3 & 4: Handle alternative gist storage formats
            else if (userData) {
                console.log('Looking for numeric gist fields in user document');
                const numericKeys = Object.keys(userData).filter(key => !isNaN(Number(key)));
                // Case 3: Document contains gist objects with numeric keys
                if (numericKeys.length > 0) {
                    console.log(`Found ${numericKeys.length} potential gist entries with numeric keys`);
                    gists = numericKeys.map(key => userData[key]);
                }
                else {
                    // Case 4: If no numeric keys, check if the user data itself might be a single gist
                    console.log('No numeric keys found, checking if user data contains gist fields');
                    const potentialGistKeys = ['title', 'link', 'status', 'segments'];
                    const matchingKeys = potentialGistKeys.filter(key => key in userData);
                    if (matchingKeys.length >= 2) { // If at least 2 gist-like fields exist
                        console.log('User data appears to contain gist fields directly');
                        gists = [userData];
                    }
                    else {
                        // Case 5: Last resort - API data seems to be returning differently
                        console.log('Unable to find gist data in expected formats, fetching from API');
                        // Make a direct API call to get gists data (fallback)
                        try {
                            const apiResponse = await fetch(`https://api-yufqiolzaa-uc.a.run.app/api/users/${userId}/gists`, {
                                headers: {
                                    'x-api-key': process.env.API_KEY || '',
                                },
                            });
                            if (apiResponse.ok) {
                                const data = await apiResponse.json();
                                if (data && Array.isArray(data.data)) {
                                    console.log('Retrieved gists from API directly');
                                    gists = data.data;
                                }
                            }
                        }
                        catch (error) {
                            console.error('Error fetching from API:', error);
                            // Continue with empty gists if API call fails
                        }
                    }
                }
            }
            console.log(`Returning ${gists.length} gists`);
            return { gists, count: gists.length };
        }
        catch (error) {
            console.error('Error getting user gists:', error);
            throw error;
        }
    },
    /**
     * USE CASE 3: UPDATE GIST STATUS
     * Updates the status of a specific gist for a user
     *
     * This function searches for a gist using multiple strategies:
     * 1. Looks for gist by ID in a 'gists' array
     * 2. Looks for gist by ID in numeric key fields
     * 3. Falls back to matching by title if gistId not found
     * 4. Creates a mock gist for testing if requested and not found
     *
     * After finding or creating the gist, it updates its status and
     * ensures the document is updated with a timestamp.
     *
     * @param userId - ID of the user who owns the gist
     * @param gistId - ID of the gist to update
     * @param statusUpdate - Partial status object with fields to update
     * @returns The updated gist object
     * @throws Error if user or gist not found
     */
    async updateGistStatus(userId, gistId, statusUpdate) {
        try {
            console.log(`Updating gist status for user: ${userId}, gist: ${gistId}`);
            console.log(`Status update: ${JSON.stringify(statusUpdate)}`);
            const userRef = firebase_1.db.collection('users').doc(userId);
            const userDoc = await userRef.get();
            if (!userDoc.exists) {
                console.log(`User not found: ${userId}`);
                throw new Error('User not found');
            }
            const userData = userDoc.data() || {};
            let gistToUpdate = null;
            let updatePath = '';
            let gistIndex = -1;
            // Strategy 1: Check if gists are stored in a 'gists' array
            if ('gists' in userData && Array.isArray(userData.gists)) {
                console.log('Checking gists array for matching gist');
                gistIndex = userData.gists.findIndex((g) => g.gistId === gistId);
                if (gistIndex !== -1) {
                    console.log(`Found gist at index ${gistIndex} in gists array`);
                    gistToUpdate = userData.gists[gistIndex];
                    updatePath = `gists.${gistIndex}.status`;
                }
            }
            // Strategy 2: Check if gists are stored with numeric keys in the document
            if (!gistToUpdate) {
                console.log('Checking for gist in numeric fields');
                const numericKeys = Object.keys(userData).filter(key => !isNaN(Number(key)));
                for (const key of numericKeys) {
                    const gist = userData[key];
                    if (gist && gist.gistId === gistId) {
                        console.log(`Found gist with numeric key ${key}`);
                        gistToUpdate = gist;
                        updatePath = key + '.status';
                        break;
                    }
                }
            }
            // Strategy 3: If gist ID not found, try matching by title
            if (!gistToUpdate && 'gists' in userData && Array.isArray(userData.gists)) {
                console.log('Gist ID not found, checking for matching title in gists array');
                // Fallback to find by title if available
                const titleMatch = userData.gists.findIndex((g) => g.title && g.title === gistId);
                if (titleMatch !== -1) {
                    console.log(`Found gist by title match at index ${titleMatch}`);
                    gistToUpdate = userData.gists[titleMatch];
                    updatePath = `gists.${titleMatch}.status`;
                }
            }
            // In numeric keys strategy
            if (!gistToUpdate) {
                console.log(`No gist found with ID ${gistId}`);
                // Attempt to find by title match as a fallback
                const titleMatch = userData.gists.findIndex((gist) => gist.title === gistId);
                if (titleMatch !== -1) {
                    console.log(`Found gist by title match at index ${titleMatch}`);
                    gistToUpdate = userData.gists[titleMatch];
                    updatePath = `gists.${titleMatch}.status`;
                }
            }
            // Final check - gist not found
            if (!gistToUpdate) {
                throw new Error('Gist not found');
            }
            // Ensure the gist has a status object
            if (!gistToUpdate.status) {
                gistToUpdate.status = {
                    is_done_playing: false,
                    is_now_playing: false,
                    playback_time: 0,
                    in_productionQueue: false,
                    production_status: 'pending'
                };
            }
            // Update the status
            const updatedStatus = Object.assign(Object.assign({}, gistToUpdate.status), statusUpdate);
            console.log(`Updating gist at path: ${updatePath}`);
            console.log(`New status: ${JSON.stringify(updatedStatus)}`);
            await userRef.update({
                [updatePath]: updatedStatus,
                updatedAt: admin.firestore.FieldValue.serverTimestamp()
            });
            // Return the updated gist
            const updatedGist = Object.assign(Object.assign({}, gistToUpdate), { status: updatedStatus });
            return updatedGist;
        }
        catch (error) {
            console.error('Error updating gist status:', error);
            throw error;
        }
    },
    /**
     * USE CASE 2: EXTRACT LINKS
     * Retrieves all links for a given user
     *
     * Currently only handles links stored in a 'links' array field within the user document.
     * This function is simpler than getUserGists since links are expected to follow a more
     * consistent storage pattern.
     *
     * @param userId - The ID of the user whose links to retrieve
     * @returns An object containing an array of links and their count
     * @throws Error if user not found or retrieval fails
     */
    async getUserLinks(userId) {
        try {
            const userDoc = await firebase_1.db.collection('users').doc(userId).get();
            if (!userDoc.exists) {
                throw new Error('User not found');
            }
            const userData = userDoc.data();
            return {
                links: ((userData === null || userData === void 0 ? void 0 : userData.links) || []),
                count: ((userData === null || userData === void 0 ? void 0 : userData.links) || []).length
            };
        }
        catch (error) {
            console.error('Error fetching links:', error);
            throw error;
        }
    },
    // Add other Firestore operations as needed
};
//# sourceMappingURL=firestore_service.js.map