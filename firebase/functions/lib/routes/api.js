"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const contentApproval_1 = require("../controllers/contentApproval");
const auth_1 = require("../middleware/auth");
const router = express_1.default.Router();
// Apply authentication middleware to all routes
router.use(auth_1.authenticateUser);
// Health check endpoint
router.get('/health', (req, res) => {
    res.status(200).json({ status: 'ok', message: 'API is running' });
});
// Gist routes
router.get('/gists/:userId', contentApproval_1.fetchUserGists);
router.get('/gists/:userId/:gistId', contentApproval_1.fetchUserGist);
router.put('/gists/:userId/:gistId/status', contentApproval_1.updateGistProductionStatus);
router.put('/gists/:userId/batch/status', contentApproval_1.batchUpdateGists);
router.put('/gists/:userId/:gistId/with-links', contentApproval_1.updateGistAndLinks);
// Link routes
router.get('/links/:userId', contentApproval_1.fetchUserLinks);
exports.default = router;
//# sourceMappingURL=api.js.map