const express = require('express');
const mongoose = require('mongoose');

const app = express();
app.use(express.json());

mongoose.connect('mongodb://localhost/books', { useNewUrlParser: true });
const db = mongoose.connection;

db.on('error', (error) => console.error(error));
db.once('open', () => console.log('Connected to MongoDB'));

const bookSchema = new mongoose.Schema({
  name: String
});

const Book = mongoose.model('Book', bookSchema);

app.post('/books', (req, res) => {
  const book = new Book({
    name: req.body.name
  });

  book.save((error, book) => {
    if (error) {
      console.error(error);
      res.status(500).send('Error saving book');
    } else {
      console.log(`Book saved: ${book.name}`);
      res.send(book);
    }
  });
});

app.get('/books', (req, res) => {
  Book.find({}, (error, books) => {
    if (error) {
      console.error(error);
      res.status(500).send('Error fetching books');
    } else {
      console.log(`Books fetched: ${books.map(book => book.name).join(', ')}`);
      res.send(books);
    }
  });
});

app.listen(3000, () => {
  console.log('Server started on port 3000');
});
