import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    message: 'Drive Pulse Backend is running',
    timestamp: new Date().toISOString()
  });
});

app.get('/api/data', (req, res) => {
  res.json({
    message: 'Welcome to Drive Pulse API',
    version: '1.0.0'
  });
});

app.listen(PORT, () => {
  console.log(`🚗 Backend running on port ${PORT}`);
});