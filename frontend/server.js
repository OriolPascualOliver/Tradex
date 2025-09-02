// server.js — minimal static server (no Express)
// Folders:
//   /pages  -> your HTML files
//   /public -> your static assets (css, js, img, ...)

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;

const rootDir   = __dirname;
const pagesDir  = path.join(rootDir, 'pages');
const publicDir = path.join(rootDir, 'public');

const mimeTypes = {
  '.html': 'text/html; charset=utf-8',
  '.css':  'text/css; charset=utf-8',
  '.js':   'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif':  'image/gif',
  '.svg':  'image/svg+xml',
  '.ico':  'image/x-icon',
  '.webp': 'image/webp'
};

function safeJoin(base, reqPath) {
  // remove any leading slashes and normalize
  const clean = reqPath.replace(/^\/+/, '');
  const full  = path.normalize(path.join(base, clean));
  if (!full.startsWith(base)) return null; // block traversal
  return full;
}

function resolveFilePath(pathname) {
  // decode and normalize the URL path
  let p = decodeURI(pathname);

  // Root → /pages/index.html
  if (p === '/') {
    return safeJoin(pagesDir, 'index.html');
  }

  // If path has no extension or ends with slash, treat as a page
  const hasExt = path.extname(p) !== '';
  if (!hasExt || p.endsWith('/')) {
    // drop trailing slash (if any)
    p = p.replace(/\/+$/, '');
    // remove leading slash for joining
    const basename = p.startsWith('/') ? p.slice(1) : p;
    const file = (basename === '' ? 'index' : basename) + '.html';
    return safeJoin(pagesDir, file);
  }

  // If the request explicitly asks for an .html file -> serve from /pages
  if (p.endsWith('.html')) {
    const basename = p.startsWith('/') ? p.slice(1) : p;
    return safeJoin(pagesDir, basename);
  }

  // Otherwise, treat as static asset from /public
  return safeJoin(publicDir, p);
}

function renderWithIncludes(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');
  const includeRegex = /<!--#include\s+"([^"]+)"\s*-->/g;
  content = content.replace(includeRegex, (m, includeFile) => {
    const full = safeJoin(pagesDir, includeFile);
    if (!full) return '';
    try {
      return fs.readFileSync(full, 'utf8');
    } catch {
      return '';
    }
  });
  return content;
}

const server = http.createServer(async (req, res) => {
  try {
    const { pathname } = new URL(req.url, 'http://localhost');
    const filePath = resolveFilePath(pathname);

    if (!filePath) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('404 Not Found');
      return;
    }

    await fs.promises.access(filePath);

    const ext = path.extname(filePath).toLowerCase();
    const contentType = mimeTypes[ext] || 'application/octet-stream';

    // Cache policy: strong for static assets in /public, no-cache for HTML
    const isStatic = filePath.startsWith(publicDir) && ext !== '.html';
    const headers = {
      'Content-Type': contentType,
      'Cache-Control': isStatic
        ? 'public, max-age=31536000, immutable'
        : 'no-cache'
    };
    if (ext === '.html' && filePath.startsWith(pagesDir)) {
      const html = renderWithIncludes(filePath);
      res.writeHead(200, headers);
      res.end(html);
      return;
    }

    const stream = fs.createReadStream(filePath);
    stream.on('error', () => {
      res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('500 Server Error');
    });
    res.writeHead(200, headers);
    stream.pipe(res);
  } catch (e) {
    if (e.code === 'ENOENT') {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('404 Not Found');
    } else {
      res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('500 Server Error');
    }
  }
});

server.listen(PORT, () => {
  console.log(`▶ Static site running at http://localhost:${PORT}`);
  console.log(`   Pages:  /, /pricing, /pricing.html, /contact ...`);
  console.log(`   Assets: /css/style.css, /js/app.js, /img/logo.png ...`);
});
