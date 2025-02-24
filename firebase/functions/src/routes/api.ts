import * as express from 'express';
import { contentApprovalController } from '../controllers/contentApproval';

const router = express.Router();

// Get all gists for a user
router.get('/gists/:userId', contentApprovalController.fetchUserGist);

// Get specific gist
router.get('/gists/:userId/:gistId', contentApprovalController.fetchUserGist);

// Update gist production status
router.post('/gists/:userId/:gistId/production', contentApprovalController.updateGistProductionStatus);

// Get specific link for content approval
router.get('/links/:userId/:linkId', contentApprovalController.fetchUserLink);

export default router;
