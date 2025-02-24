import * as functions from 'firebase-functions';
import express from 'express';
import cors from 'cors';
import apiRoutes from './routes/api';
import { authenticateUser } from './middleware/auth';

const app = express();

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
export const api = functions.https.onRequest(app);

// Optional: Add Firestore triggers if needed
export const onUserContentUpdate = functions.firestore
  .document('users/{userId}/content/{contentId}')
  .onUpdate(async (change, context) => {
    const newData = change.after.data();
    const previousData = change.before.data();
    
    // Add logic for handling content updates
    // This could trigger CrewAI workflows based on status changes
    console.log('Content updated:', {
      userId: context.params.userId,
      contentId: context.params.contentId,
      previousStatus: previousData.status,
      newStatus: newData.status
    });
  });
