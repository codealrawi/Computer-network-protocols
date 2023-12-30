const http = require('http');
const url = require('url');

function generateRandomArray(n) {
  const result = [];
  for (let i = 0; i < n; i++) {
    result.push(Math.floor(Math.random() * n) + 1);
  }
  return result;
}

const server = http.createServer((req, res) => {
  const urlParts = url.parse(req.url, true);
  const n = parseInt(urlParts.query.n);
  
  if (isNaN(n) || n < 1) {
    res.statusCode = 400;
    res.end('Invalid parameter "n".');
    return;
  }
  
  const randomArray = generateRandomArray(n);
  res.setHeader('Content-Type', 'application/json');
  res.end(JSON.stringify(randomArray));
});

const port = 3000;
server.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
