import * as functions from 'firebase-functions';
import express from 'express';
import cors from 'cors';
import apiRoutes from './routes/api';
import { authenticateUser } from './middleware/auth';

// Create Express app
const app = express();

// Make config available
process.env.FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY = process.env.FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY;

// IP restriction middleware - uncomment and configure if needed
// const ALLOWED_IPS = ['123.456.789.0']; // Replace with your actual allowed IPs
// app.use((req, res, next) => {
//   const clientIp = req.ip || req.headers['x-forwarded-for'] || req.connection.remoteAddress;
//   if (!ALLOWED_IPS.includes(clientIp)) {
//     console.warn(`Access denied for IP: ${clientIp}`);
//     return res.status(403).json({
//       success: false,
//       error: 'Access denied'
//     });
//   }
//   next();
// });

// Rate limiting - uncomment if needed
// const RATE_LIMIT_WINDOW_MS = 15 * 60 * 1000; // 15 minutes
// const MAX_REQUESTS_PER_WINDOW = 100; // 100 requests per 15 minutes
// 
// app.use((req, res, next) => {
//   // Simple in-memory rate limiter
//   // For production, use redis or a proper rate limiting library
//   const now = Date.now();
//   const key = req.ip || 'unknown';
//   
//   if (!global.rateLimiter) {
//     global.rateLimiter = {};
//   }
//   
//   if (!global.rateLimiter[key]) {
//     global.rateLimiter[key] = {
//       count: 0,
//       resetAt: now + RATE_LIMIT_WINDOW_MS
//     };
//   }
//   
//   if (now > global.rateLimiter[key].resetAt) {
//     global.rateLimiter[key] = {
//       count: 1,
//       resetAt: now + RATE_LIMIT_WINDOW_MS
//     };
//   } else {
//     global.rateLimiter[key].count++;
//   }
//   
//   if (global.rateLimiter[key].count > MAX_REQUESTS_PER_WINDOW) {
//     return res.status(429).json({
//       success: false,
//       error: 'Too many requests, please try again later'
//     });
//   }
//   
//   next();
// });

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

// If running locally, start the server
if (process.env.NODE_ENV === 'development') {
  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
}
