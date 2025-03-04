import express from 'express';
import { 
  fetchUserGists, 
  fetchUserGist, 
  updateGistProductionStatus, 
  fetchUserLinks,
  batchUpdateGists,
  updateGistAndLinks
} from '../controllers/contentApproval';
import { authenticateService } from '../middleware/auth';

const router = express.Router();

// Apply service authentication middleware to all routes
router.use(authenticateService);

// Health check endpoint
router.get('/health', (req, res) => {
  return res.status(200).json({ status: 'ok', message: 'API is running' });
});

// Gist routes with userId in URL parameters
router.get('/gists/:userId', fetchUserGists);
router.get('/gists/:userId/:gistId', fetchUserGist);
router.put('/gists/:userId/:gistId/status', updateGistProductionStatus);
router.put('/gists/:userId/batch/status', batchUpdateGists);
router.put('/gists/:userId/:gistId/with-links', updateGistAndLinks);

// Link routes with userId in URL parameters
router.get('/links/:userId', fetchUserLinks);

export default router;
