# 🔖 Markd — Smart Bookmark Manager

A full-stack **Bookmark Manager** application with a RESTful API and a sleek, modern dark-theme UI. Built with zero external dependencies — just Python 3 and a browser.

---

## ✨ Features

- **Add** bookmarks with a title and URL
- **View** all bookmarks with favicons, timestamps, and live search/filter
- **Edit** bookmarks inline — no page reload
- **Delete** bookmarks with confirmation
- Real-time filter/search across title and URL
- Persistent storage via SQLite
- Toast notifications for all actions
- Fully responsive UI

---

## 🛠 Tech Stack

| Layer    | Technology                                      |
|----------|-------------------------------------------------|
| Backend  | Python 3 (`http.server` + `sqlite3`) — no pip  |
| Database | SQLite 3 (auto-created on first run)            |
| Frontend | Vanilla HTML/CSS/JS (no frameworks needed)      |

---

## 🚀 Setup & Running

### Prerequisites

- **Python 3.7+** (check with `python3 --version`)
- No other dependencies required!

### Steps

```bash
# 1. Clone or download the project
git clone <your-repo-url>
cd bookmark-manager

# 2. Run the server
python3 run.py

# 3. Open your browser
# Visit: http://localhost:5000
```

The server will:
- Auto-create `backend/bookmarks.db` (SQLite database) on first run
- Serve the API at `http://localhost:5000/api/bookmarks`
- Serve the frontend at `http://localhost:5000/`

---

## 📡 API Reference

Base URL: `http://localhost:5000`

### Get All Bookmarks
```http
GET /api/bookmarks
```
**Response:**
```json
{
  "bookmarks": [
    {
      "id": "uuid",
      "title": "OpenAI",
      "url": "https://openai.com",
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T10:30:00"
    }
  ],
  "count": 1
}
```

---

### Get Single Bookmark
```http
GET /api/bookmarks/:id
```
**Response:** Single bookmark object or `{"error": "Bookmark not found"}` (404)

---

### Add a Bookmark
```http
POST /api/bookmarks
Content-Type: application/json

{
  "title": "GitHub",
  "url": "https://github.com"
}
```
**Response (201):** Created bookmark object

---

### Update a Bookmark
```http
PUT /api/bookmarks/:id
Content-Type: application/json

{
  "title": "GitHub — Updated",
  "url": "https://github.com/new"
}
```
**Response:** Updated bookmark object

---

### Delete a Bookmark
```http
DELETE /api/bookmarks/:id
```
**Response:**
```json
{
  "message": "Bookmark deleted",
  "id": "uuid"
}
```

---

## 📁 Project Structure

```
bookmark-manager/
├── run.py                    ← Entry point (run this)
├── README.md
├── backend/
│   ├── server.py             ← Python HTTP API server
│   ├── requirements.txt      ← (no deps — stdlib only)
│   └── bookmarks.db          ← SQLite DB (auto-created)
└── frontend/
    └── public/
        └── index.html        ← Single-page frontend app
```

---

## 🌐 Deployment Options

### Option A: Railway (Recommended — Free Tier)
1. Push code to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Set **Start Command**: `python3 run.py`
4. Railway auto-assigns a public URL

### Option B: Render
1. Push to GitHub
2. New Web Service → Connect repo
3. **Build Command**: *(leave empty)*
4. **Start Command**: `python3 run.py`
5. Free tier available

### Option C: Fly.io
```bash
# Install flyctl, then:
flyctl launch
flyctl deploy
```

### Option D: VPS / Any Server
```bash
# On your server:
git clone <repo>
cd bookmark-manager
nohup python3 run.py &
# Configure nginx/caddy to proxy port 5000
```

---

## 🧪 Quick API Test (curl)

```bash
# Add a bookmark
curl -X POST http://localhost:5000/api/bookmarks \
  -H "Content-Type: application/json" \
  -d '{"title":"Google","url":"https://google.com"}'

# View all bookmarks
curl http://localhost:5000/api/bookmarks

# Update (replace <id> with actual UUID)
curl -X PUT http://localhost:5000/api/bookmarks/<id> \
  -H "Content-Type: application/json" \
  -d '{"title":"Google Search","url":"https://google.com"}'

# Delete
curl -X DELETE http://localhost:5000/api/bookmarks/<id>
```

---

## 📸 Screenshot

The app features a dark brutalist-minimal design with:
- Lime-green accent (`#c8ff00`) for actions
- Cyan accent (`#00d4ff`) for edit states  
- Red accent (`#ff6b6b`) for destructive actions
- `Syne` display font + `DM Mono` for body text
- Subtle animated glow orbs and noise texture overlay


