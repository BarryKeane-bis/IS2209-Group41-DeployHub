# IS2209 Group41 DeployHub

A Flask-based gym plan web service integrating PostgreSQL and the API Ninjas Exercise API.

## Live Deployment
https://is2209-group41-deployhub-el8k.onrender.com
## GitHub Repository
https://github.com/BarryKeane-bis/IS2209_-Group41-_DeployHub

## Setup

### Prerequisites
- Python 3.12+
- pip
- Docker (optional for local container)

### Installation
```bash
git clone https://github.com/BarryKeane-bis/IS2209_-Group41-_DeployHub.git
cd IS2209_-Group41-_DeployHub
pip install -r requirements.txt
```

### Environment Variables
Copy `.env.example` to `.env` and fill in the values:
```
DATABASE_URL=your_supabase_connection_string
EXTERNAL_API_KEY=your_api_ninjas_key
FLASK_ENV=development
FLASK_APP=app/app.py
SECRET_KEY=your_secret_key
```

### Run Locally
```bash
python app/app.py
```

Then visit 👉 http://127.0.0.1:8080

## Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| / | GET | Frontend homepage |
| /health | GET | Returns service health status |
| /status | GET | Returns app and DB connectivity status |
| /exercises?muscle=chest | GET | Fetches exercises from API Ninjas |
| /plans | GET | Retrieves all workout plans from DB |
| /plans | POST | Creates a new workout plan |
| /data?muscle=chest | GET | Returns combined exercises and plans |

## CI/CD
- **CI:** GitHub Actions runs lint, tests, and Docker build on every PR
- **CD:** Auto-deploys to Render on every merge to main
- **Container:** Docker image published to GitHub Container Registry (GHCR)
- **Release:** v1.0.0 tagged on main

## Demo Steps
1. Visit `/health` — should return `{"status":"ok"}`
2. Visit `/status` — should return `{"db":"connected","status":"running"}`
3. Visit `/exercises?muscle=chest` — returns live exercise data from API Ninjas
4. Visit `/data?muscle=biceps` — returns combined exercises and workout plans
5. POST to `/plans` with `{"name": "My Chest Day", "user_id": "user1"}` — creates a workout plan

## Contributors
- Barry Keane
- Conor Dalton
- George Howard
- Darragh Lee