// Set up PostgreSQL connection
const pool = new Pool({
  user: 'postgres',
  host: 'localhost', // Change this to 'localhost' for local database
  database: 'fakereal-db',
  password: '05^O@8>E@[}YA~QS', // Replace with a secure password
  port: 5432, // Default Postgres port
});

// Handle image upload endpoint
app.post('/upload', upload.single('image'), async (req, res) => {
  if (!req.file) {
    return res.status(400).json({ message: 'No file uploaded' });
  }

  const imagePath = `/uploads/${req.file.filename}`; // Use relative path

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
app.use('/uploads', express.static(uploadDir));

// Set up server to listen on port 3000
const port = 3000;
app.listen(port, () => {
  console.log(`✅ Server running on http://localhost:${port}`);
});
