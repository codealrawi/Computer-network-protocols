const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const menu = () => {
  console.log(`\n1. Add Book\n2. View Books\n3. Exit`);
  rl.question('Enter your choice: ', (choice) => {
    switch (choice) {
      case '1':
        rl.question('Enter book name: ', (bookName) => {
          addBook(bookName);
          menu();
        });
        break;
      case '2':
        viewBooks();
        menu();
        break;
      case '3':
        console.log('Exiting...');
        process.exit(0);
        break;
      default:
        console.log('Invalid choice. Try again.');
        menu();
    }
  });
}

const addBook = (bookName) => {
  console.log(`Adding book: ${bookName}`);
  // Send a request to the server to add the book
}

const viewBooks = () => {
  console.log('Fetching books...');
  // Send a request to the server to get the list of books
}

menu();
