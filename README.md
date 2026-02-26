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

## 🚀 Setup & Running Locally

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

## 🌐 Deployment

### ⭐ Option A: Replit (Recommended — Easiest & Free)

Replit requires **no git, no CLI, no Docker** — just upload and run.

#### Steps

1. **Create a free account** at [replit.com](https://replit.com)

2. **Create a new Repl**
   - Click **+ Create Repl**
   - Choose template: **Python**
   - Name it: `bookmark-manager`
   - Click **Create Repl**

3. **Upload your project files**
   - In the left sidebar, click the **three dots (⋮)** next to Files
   - Click **Upload folder** and select your project folder  
   *(or upload files one by one into the correct folders)*

4. **Set the run command**
   - Click the `.replit` file in the sidebar
   - Set the `run` field to:
     ```
     python3 run.py
     ```

5. **Click the Run ▶ button**
   - Your app starts and a live preview appears on the right
   - The SQLite database is auto-created and **persists across restarts** — no setup needed

6. **Get your public URL**
   - Click the **open in new tab ↗** icon at the top of the preview pane
   - Your URL looks like: `https://bookmark-manager.YOUR-USERNAME.repl.co`
   - Share this URL with anyone!

7. **Keep it awake for free (optional)**
   - Replit free tier sleeps after ~30 mins of inactivity
   - Go to [uptimerobot.com](https://uptimerobot.com) → free account
   - Add a new **HTTP monitor** with your Replit URL, ping every **5 minutes**
   - Your app will never sleep again ✅

> 💡 **Why Replit?** SQLite works out of the box with no volume configuration, there's no CLI or git required, and you get a live public URL in under 5 minutes.

---

### Option B: Railway

1. Push code to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Set **Start Command**: `python3 run.py`
4. Add a **Volume** mounted at `/data` for persistent database storage
5. Set environment variable: `DB_PATH=/data/bookmarks.db`
6. Railway auto-assigns a public URL

---

### Option C: Render

1. Push to GitHub
2. New Web Service → Connect repo
3. **Build Command**: *(leave empty)*
4. **Start Command**: `python3 run.py`
5. Add a **Disk** mounted at `/data` (1 GB)
6. Set environment variable: `DB_PATH=/data/bookmarks.db`

> ⚠️ Free tier spins down after 15 min of inactivity — first request after sleep takes ~30s.

---

### Option D: Fly.io

```bash
# Install flyctl, then:
flyctl auth login
flyctl launch
flyctl volumes create markd_data --size 1 --region sin
flyctl secrets set DB_PATH=/data/bookmarks.db
flyctl deploy
```

---

### Option E: VPS / Any Server

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
Live URL : https://bookmark-manager--vishalaryadeshp.replit.app/
