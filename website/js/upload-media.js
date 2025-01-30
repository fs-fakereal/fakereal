const express = require('express');
const multer = require('multer');
const path = require('path');
const { Pool } = require('pg');
const cors = require('cors');
const fs = require('fs');

// Create Express app
const app = express();

// Enable CORS (for front-end access)
app.use(cors());

// Set up multer storage
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, './uploads'); // Store images in the 'uploads' directory
  },
  filename: (req, file, cb) => {
    const fileExt = path.extname(file.originalname); // Get file extension
    cb(null, Date.now() + fileExt); // Save file with a unique name (timestamp)
  }
});

// Initialize multer upload
const upload = multer({ storage: storage });

// Set up PostgreSQL connection
const pool = new Pool({
  user: 'postgres',
  host: '23.251.147.161', // Replace with your DB host/public IP
  database: 'fakereal-db', // Your database name
  password: '05^O@8>E@[}YA~QS', // Your DB password
  port: 5432, // Default Postgres port
});

// Handle image upload endpoint
app.post('/upload', upload.single('image'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ message: 'No file uploaded' });
  }

  const imagePath = req.file.path; // Get the uploaded file's path

  try {
    // Save image details to PostgreSQL (in the 'images' table)
    const query = 'INSERT INTO images (image_url) VALUES ($1) RETURNING *';
    const values = [imagePath];

    const result = await pool.query(query, values);

    if (result.rows.length > 0) {
      res.status(200).json({ message: 'File uploaded successfully', image: result.rows[0] });
    } else {
      res.status(500).json({ message: 'Error saving image to database' });
    }
  } catch (error) {
    console.error('Database Error:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// Serve uploaded images (static route)
app.use('/uploads', express.static('uploads'));

// Set up server to listen on port 3000
const port = 3000;
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
