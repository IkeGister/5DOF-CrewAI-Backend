import express from 'express';
import { updateGistProductionStatus } from '../controllers/contentApproval_subcollections';
import { authenticateService } from '../middleware/auth';

const router = express.Router();

// Apply service authentication middleware to all routes
router.use(authenticateService);

// Health check endpoint
router.get('/health', (req, res) => {
  return res.status(200).json({ 
    status: 'ok', 
    message: 'API is running with subcollection-based structure',
    version: 'subcollections-v1' 
  });
});

// Currently active endpoint - notifies when a gist has been created (subcollection version)
router.put('/gists/:userId/:gistId/status', updateGistProductionStatus);

export default router; 