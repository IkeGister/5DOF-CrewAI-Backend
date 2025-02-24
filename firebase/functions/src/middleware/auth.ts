import { Request, Response, NextFunction } from 'express';

export const authenticateUser = (
  req: Request, 
  res: Response, 
  next: NextFunction
): Response | void => {
  console.log('Headers:', req.headers);
  console.log('API Key from request:', req.headers['x-api-key']);
  console.log('Config API Key:', process.env.FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY);
  
  const apiKey = req.headers['x-api-key'];
  const configApiKey = process.env.FUNCTIONS_CONFIG_CREWAI_FUNCTIONS_API_KEY;

  if (!apiKey) {
    return res.status(401).json({ error: 'Unauthorized - No token provided' });
  }

  if (apiKey !== configApiKey) {
    return res.status(401).json({ error: 'Unauthorized - Invalid token' });
  }

  return next();
};
