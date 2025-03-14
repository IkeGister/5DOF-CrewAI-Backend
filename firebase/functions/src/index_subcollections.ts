import * as functions from 'firebase-functions';
import express from 'express';
import cors from 'cors';
import apiRoutes from './routes/api_subcollections';

// Create Express app
const app = express();

// In Firebase Functions v2, environment variables are set directly in the Firebase console
// or via the firebase.json file, so we don't need to use functions.config() anymore

// Set SKIP_API_KEY_VALIDATION to true in development mode
if (process.env.NODE_ENV === 'development') {
  process.env.SKIP_API_KEY_VALIDATION = 'true';
  console.log('Development mode: API key validation is skipped');
}

// Middleware
app.use(cors({ origin: true }));
app.use(express.json());

// Routes - Using the subcollection-based API routes
app.use('/api', apiRoutes);

// Error handling
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Unhandled API error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
  });
});

// 404 handler
app.use((req: express.Request, res: express.Response) => {
  res.status(404).json({
    error: 'Not found',
    message: `Endpoint ${req.method} ${req.path} not found`
  });
});

// Export the Express app as a Firebase Cloud Function
export const api = functions.https.onRequest(app);

// Add a note that this uses the subcollection-based structure
console.log('CrewAI Backend API loaded with subcollection-based structure'); 