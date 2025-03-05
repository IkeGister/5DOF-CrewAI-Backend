import * as functions from 'firebase-functions';
import express from 'express';
import cors from 'cors';
import apiRoutes from './routes/api';

// Create Express app
const app = express();

// In Firebase Functions v2, environment variables are set directly in the Firebase console
// or via the firebase.json file, so we don't need to use functions.config() anymore

// Set SKIP_API_KEY_VALIDATION to true in development mode
if (process.env.NODE_ENV === 'development') {
  process.env.SKIP_API_KEY_VALIDATION = 'true';
  console.log('Development mode: API key validation is skipped');
}

// Optional: Configure IP restriction for additional security
// This can be enabled in production to restrict access to specific IP addresses
// const allowedIPs = functions.config().security?.allowed_ips?.split(',') || [];
// app.use((req, res, next) => {
//   const clientIP = req.ip || req.connection.remoteAddress;
//   if (allowedIPs.length === 0 || allowedIPs.includes(clientIP)) {
//     return next();
//   }
//   return res.status(403).json({ error: 'Forbidden', message: 'IP not allowed' });
// });





// Optional: Configure rate limiting for additional security
// This can be enabled in production to prevent abuse
// const rateLimit = require('express-rate-limit');
// const limiter = rateLimit({
//   windowMs: 15 * 60 * 1000, // 15 minutes
//   max: 100, // limit each IP to 100 requests per windowMs
//   message: { error: 'Too many requests', message: 'Please try again later' }
// });
// app.use(limiter);

// Middleware
app.use(cors({ origin: true }));
app.use(express.json());

// Routes
app.use('/api', apiRoutes);

// Error handling
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Unhandled error:', err);
  res.status(500).json({
    success: false,
    error: 'Internal Server Error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
  });
});

// Export the Express app as a Firebase Cloud Function
export const api = functions.https.onRequest(app);

// Start the server locally in development mode
if (process.env.NODE_ENV === 'development') {
  const PORT = process.env.PORT || 3000;
  
  // Set default values for environment variables if not already set
  if (!process.env.SERVICE_API_KEY) {
    process.env.SERVICE_API_KEY = 'dev-service-api-key';
    console.log('Using default SERVICE_API_KEY for development');
  }
  
  if (!process.env.CREW_AI_API_KEY) {
    process.env.CREW_AI_API_KEY = 'dev-crewai-api-key';
    console.log('Using default CREW_AI_API_KEY for development');
  }
  
  if (!process.env.CREW_AI_BASE_URL) {
    process.env.CREW_AI_BASE_URL = 'http://localhost:5000';
    console.log(`Using default CREW_AI_BASE_URL: ${process.env.CREW_AI_BASE_URL}`);
  }
  
  app.listen(PORT, () => {
    console.log(`Server running in development mode on port ${PORT}`);
    console.log(`API available at: http://localhost:${PORT}/api`);
  });
}
