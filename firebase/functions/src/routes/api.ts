import express from 'express';
import { 
  fetchUserGists, 
  fetchUserGist, 
  updateGistProductionStatus, 
  fetchUserLinks,
  batchUpdateGists,
  updateGistAndLinks
} from '../controllers/contentApproval';
import { authenticateUser } from '../middleware/auth';

const router = express.Router();

// Apply authentication middleware to all routes
router.use(authenticateUser);

// Health check endpoint
router.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', message: 'API is running' });
});

// Gist routes
router.get('/gists/:userId', fetchUserGists);
router.get('/gists/:userId/:gistId', fetchUserGist);
router.put('/gists/:userId/:gistId/status', updateGistProductionStatus);
router.put('/gists/:userId/batch/status', batchUpdateGists);
router.put('/gists/:userId/:gistId/with-links', updateGistAndLinks);

// Link routes
router.get('/links/:userId', fetchUserLinks);

export default router;
