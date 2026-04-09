# IS2209 Group41 DeployHub

A Flask-based gym plan web service integrating PostgreSQL and the API Ninjas Exercise API.

## Live Deployment
https://is2209-group41-deployhub.onrender.com

## Setup

### Prerequisites
- Python 3.13
- pip

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
```

### Run Locally
```bash
python app/app.py
```

## Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| /health | GET | Returns service health status |
| /status | GET | Returns app and DB connectivity status |
| /exercises?muscle=chest | GET | Fetches exercises from API Ninjas |
| /plans | GET | Retrieves all workout plans from DB |
| /plans | POST | Creates a new workout plan |

## CI/CD
- CI: GitHub Actions runs lint, tests, and Docker build on every PR
- CD: Auto-deploys to Render on every merge to main

## Demo
1. Visit /health — should return `{"status":"ok"}`
2. Visit /status — should return `{"db":"connected","status":"running"}`
3. Visit /exercises?muscle=chest — returns live exercise data
4. POST to /plans with `{"name": "My Chest Day", "user_id": "barry"}` — creates a workout plan
```
