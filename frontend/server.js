const http = require('http');
const fs = require('fs');
const path = require('path');

const port = process.env.PORT || 3000;

const rootDir   = __dirname;
const pagesDir  = path.join(rootDir, 'pages');
const publicDir = path.join(rootDir, 'public');

const mimeTypes = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.webp': 'image/webp'
};

function safeJoin(base, target) {
  const fp = path.normalize(path.join(base, target));
  if (!fp.startsWith(base)) return null;
  return fp;
}

const server = http.createServer((req, res) => {
  const urlPath = req.url === '/' ? '/index.html' : req.url;
  const isHtml  = urlPath.endsWith('.html') || urlPath === '/index.html';

  // 1) intenta /public para estáticos
  let filePath = safeJoin(publicDir, urlPath);

  // 2) si es página HTML o no existe en public, intenta /pages
  if (isHtml || !filePath || !fs.existsSync(filePath)) {
    filePath = safeJoin(pagesDir, urlPath);
  }

  if (!filePath || !fs.existsSync(filePath)) {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('404 Not Found');
    return;
  }

  const ext = path.extname(filePath).toLowerCase();
  const contentType = mimeTypes[ext] || 'application/octet-stream';

  // cache agresiva para estáticos; no para HTML
  const headers = { 'Content-Type': contentType };
  if (filePath.startsWith(publicDir) && ext !== '.html') {
    headers['Cache-Control'] = 'public, max-age=31536000, immutable';
  } else {
    headers['Cache-Control'] = 'no-cache';
  }

  fs.readFile(filePath, (err, content) => {
    if (err) {
      res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('500 Server Error');
      return;
    }
    res.writeHead(200, headers);
    res.end(content);
  });
});

server.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
