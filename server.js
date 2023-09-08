const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');

const app = express();
const port = process.env.PORT || 3000;

// Connect to MongoDB
mongoose.connect('mongodb://localhost/pantrycloud', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});
const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));
db.once('open', () => {
  console.log('Connected to MongoDB');
});

// Middleware
app.use(bodyParser.json());

// Define the PantryItem schema and model
const pantryItemSchema = new mongoose.Schema({
  name: String,
  quantity: Number,
  expirationDate: Date,
});
const PantryItem = mongoose.model('PantryItem', pantryItemSchema);

// CRUD Endpoints

// Create a new pantry item
app.post('/api/pantry-items', async (req, res) => {
  try {
    const newItem = new PantryItem(req.body);
    await newItem.save();
    res.status(201).json(newItem);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// Read all pantry items
app.get('/api/pantry-items', async (req, res) => {
  try {
    const items = await PantryItem.find();
    res.status(200).json(items);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Read a specific pantry item by ID
app.get('/api/pantry-items/:id', async (req, res) => {
  try {
    const item = await PantryItem.findById(req.params.id);
    if (!item) {
      return res.status(404).json({ error: 'Pantry item not found' });
    }
    res.status(200).json(item);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Update a pantry item by ID
app.put('/api/pantry-items/:id', async (req, res) => {
  try {
    const updatedItem = await PantryItem.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true }
    );
    if (!updatedItem) {
      return res.status(404).json({ error: 'Pantry item not found' });
    }
    res.status(200).json(updatedItem);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Delete a pantry item by ID
app.delete('/api/pantry-items/:id', async (req, res) => {
  try {
    const deletedItem = await PantryItem.findByIdAndDelete(req.params.id);
    if (!deletedItem) {
      return res.status(404).json({ error: 'Pantry item not found' });
    }
    res.status(204).send();
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});