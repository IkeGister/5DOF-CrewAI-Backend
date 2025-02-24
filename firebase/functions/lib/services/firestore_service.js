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
    async getUserGists(userId) {
        try {
            const userDoc = await firebase_1.db.collection('users').doc(userId).get();
            if (!userDoc.exists) {
                throw new Error('User not found');
            }
            const userData = userDoc.data();
            return {
                gists: (userData === null || userData === void 0 ? void 0 : userData.gists) || [],
                count: ((userData === null || userData === void 0 ? void 0 : userData.gists) || []).length
            };
        }
        catch (error) {
            console.error('Error fetching gists:', error);
            throw error;
        }
    },
    async updateGistStatus(userId, gistId, status) {
        try {
            const userRef = firebase_1.db.collection('users').doc(userId);
            const userDoc = await userRef.get();
            if (!userDoc.exists) {
                throw new Error('User not found');
            }
            const userData = userDoc.data();
            const gists = (userData === null || userData === void 0 ? void 0 : userData.gists) || [];
            const gistIndex = gists.findIndex((g) => g.gistId === gistId);
            if (gistIndex === -1) {
                throw new Error('Gist not found');
            }
            // Update the gist status
            gists[gistIndex].status = Object.assign(Object.assign({}, gists[gistIndex].status), status);
            // Update the document
            await userRef.update({
                gists: gists,
                updatedAt: admin.firestore.FieldValue.serverTimestamp()
            });
            return gists[gistIndex];
        }
        catch (error) {
            console.error('Firestore update error:', error);
            throw error;
        }
    },
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