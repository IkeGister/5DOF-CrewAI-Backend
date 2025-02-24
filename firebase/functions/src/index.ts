import { onRequest } from 'firebase-functions/v2/https';
import express from 'express';
import cors from 'cors';
import apiRoutes from './routes/api';
import { authenticateUser } from './middleware/auth';

const app = express();

// Make config available
process.env.FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY = process.env.FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY;

// Middleware
app.use(cors({ origin: true }));
app.use(express.json());

// Authentication middleware for all routes
app.use(authenticateUser);

// Routes
app.use('/api', apiRoutes);

// Error handling
app.use((err: Error, req: express.Request, res: express.Response, _next: express.NextFunction) => {
  console.error(err);
  res.status(500).json({
    success: false,
    error: 'Internal server error'
  });
});

// Export the Express app as a Firebase Cloud Function
export const api = onRequest(
  {
    memory: '256MiB',
    timeoutSeconds: 60,
    minInstances: 0
  },
  app
);
