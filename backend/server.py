#!/usr/bin/env python3
"""
Smart Bookmark Manager - Backend API Server
Uses Python stdlib only: http.server + sqlite3
"""

import sqlite3
import json
import uuid
import re
from datetime import datetime, timezone

def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

DB_PATH = "bookmarks.db"
PORT = 5000

# ─── Database Setup ───────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bookmarks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print(f"✓ Database initialized at {DB_PATH}")

# ─── Request Handler ──────────────────────────────────────────────────────────

class BookmarkHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        print(f"  [{datetime.now().strftime('%H:%M:%S')}] {format % args}")

    def send_json(self, data, status=200):
        body = json.dumps(data, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def send_error_json(self, message, status=400):
        self.send_json({"error": message}, status)

    def read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        # GET /api/bookmarks
        if path == "/api/bookmarks":
            conn = get_db()
            rows = conn.execute(
                "SELECT * FROM bookmarks ORDER BY created_at DESC"
            ).fetchall()
            conn.close()
            bookmarks = [dict(r) for r in rows]
            self.send_json({"bookmarks": bookmarks, "count": len(bookmarks)})

        # GET /api/bookmarks/:id
        elif re.match(r"^/api/bookmarks/[\w-]+$", path):
            bid = path.split("/")[-1]
            conn = get_db()
            row = conn.execute(
                "SELECT * FROM bookmarks WHERE id = ?", (bid,)
            ).fetchone()
            conn.close()
            if row:
                self.send_json(dict(row))
            else:
                self.send_error_json("Bookmark not found", 404)

        # Serve static files (frontend)
        elif path == "" or path == "/" or path.startswith("/static"):
            self.serve_static(parsed.path)

        else:
            self.send_error_json("Not found", 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/api/bookmarks":
            data = self.read_body()
            title = (data.get("title") or "").strip()
            url = (data.get("url") or "").strip()

            if not title:
                return self.send_error_json("Title is required")
            if not url:
                return self.send_error_json("URL is required")
            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            now = utcnow()
            bid = str(uuid.uuid4())

            conn = get_db()
            conn.execute(
                "INSERT INTO bookmarks (id, title, url, created_at, updated_at) VALUES (?,?,?,?,?)",
                (bid, title, url, now, now)
            )
            conn.commit()
            row = conn.execute("SELECT * FROM bookmarks WHERE id = ?", (bid,)).fetchone()
            conn.close()

            self.send_json(dict(row), 201)
        else:
            self.send_error_json("Not found", 404)

    def do_PUT(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if re.match(r"^/api/bookmarks/[\w-]+$", path):
            bid = path.split("/")[-1]
            data = self.read_body()

            conn = get_db()
            row = conn.execute("SELECT * FROM bookmarks WHERE id = ?", (bid,)).fetchone()
            if not row:
                conn.close()
                return self.send_error_json("Bookmark not found", 404)

            title = (data.get("title") or row["title"]).strip()
            url = (data.get("url") or row["url"]).strip()

            if not title:
                conn.close()
                return self.send_error_json("Title cannot be empty")
            if not url:
                conn.close()
                return self.send_error_json("URL cannot be empty")
            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            now = utcnow()
            conn.execute(
                "UPDATE bookmarks SET title=?, url=?, updated_at=? WHERE id=?",
                (title, url, now, bid)
            )
            conn.commit()
            updated = conn.execute("SELECT * FROM bookmarks WHERE id = ?", (bid,)).fetchone()
            conn.close()

            self.send_json(dict(updated))
        else:
            self.send_error_json("Not found", 404)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if re.match(r"^/api/bookmarks/[\w-]+$", path):
            bid = path.split("/")[-1]
            conn = get_db()
            row = conn.execute("SELECT * FROM bookmarks WHERE id = ?", (bid,)).fetchone()
            if not row:
                conn.close()
                return self.send_error_json("Bookmark not found", 404)

            conn.execute("DELETE FROM bookmarks WHERE id = ?", (bid,))
            conn.commit()
            conn.close()

            self.send_json({"message": "Bookmark deleted", "id": bid})
        else:
            self.send_error_json("Not found", 404)

    def serve_static(self, path):
        """Serve the frontend index.html for all non-API routes."""
        import os
        # Try to serve from ../frontend/public/
        base = os.path.join(os.path.dirname(__file__), "..", "frontend", "public")
        
        if path == "/" or path == "":
            filepath = os.path.join(base, "index.html")
        else:
            filepath = os.path.join(base, path.lstrip("/"))

        if os.path.isfile(filepath):
            with open(filepath, "rb") as f:
                content = f.read()
            ext = filepath.rsplit(".", 1)[-1]
            mime = {
                "html": "text/html",
                "css": "text/css",
                "js": "application/javascript",
                "json": "application/json",
                "png": "image/png",
                "ico": "image/x-icon",
            }.get(ext, "application/octet-stream")
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            # Fallback to index.html (SPA routing)
            index = os.path.join(base, "index.html")
            if os.path.isfile(index):
                with open(index, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error_json("Not found", 404)


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    server = HTTPServer(("0.0.0.0", PORT), BookmarkHandler)
    print(f"🔖 Bookmark Manager API running at http://localhost:{PORT}")
    print(f"   Frontend: http://localhost:{PORT}/")
    print(f"   API Base: http://localhost:{PORT}/api/bookmarks")
    print("   Press Ctrl+C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
