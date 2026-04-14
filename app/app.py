import os
import requests
import logging
import uuid
import time
import psycopg2
from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / '.env')

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        return conn
    except Exception as e:
        logger.error(f"DB connection failed: {str(e)}")
        return None

@app.before_request
def before_request():
    request.request_id = str(uuid.uuid4())
    request.start_time = time.time()
    logger.info(f"request_id={request.request_id} method={request.method} path={request.path}")

@app.after_request
def after_request(response):
    duration = time.time() - request.start_time
    logger.info(f"request_id={request.request_id} status={response.status_code} duration={duration:.3f}s")
    return response

@app.route("/")
def index():
    if os.getenv("FLASK_ENV") == "production":
        return jsonify({
            "message": "Welcome to DeployHub!",
            "endpoints": ["/health", "/status", "/exercises", "/plans", "/data"]
        })
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/status")
def status():
    db_status = "connected"
    conn = get_db_connection()
    if conn is None:
        db_status = "unavailable"
    else:
        conn.close()
    return jsonify({"status": "running", "db": db_status})

@app.route("/exercises")
def exercises():
    muscle = request.args.get("muscle", "chest")
    api_key = os.getenv("EXTERNAL_API_KEY")
    try:
        response = requests.get(
            "https://api.api-ninjas.com/v1/exercises",
            headers={"X-Api-Key": api_key},
            params={"muscle": muscle},
            timeout=5
        )
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logger.error(f"request_id={request.request_id} error={str(e)}")
        return jsonify({"error": "Could not fetch exercises", "detail": str(e)}), 503

@app.route("/plans", methods=["GET"])
def get_plans():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database unavailable"}), 503
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, user_id, created_at FROM workout_plans;")
        rows = cur.fetchall()
        plans = [{"id": r[0], "name": r[1], "user_id": r[2], "created_at": str(r[3])} for r in rows]
        return jsonify(plans)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route("/plans", methods=["POST"])
def create_plan():
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database unavailable"}), 503
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO workout_plans (name, user_id) VALUES (%s, %s) RETURNING id;",
            (data.get("name"), data.get("user_id"))
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"id": new_id, "message": "Plan created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route("/data")
def data():
    muscle = request.args.get("muscle", "chest")
    api_key = os.getenv("EXTERNAL_API_KEY")

    exercises_data = []
    try:
        response = requests.get(
            "https://api.api-ninjas.com/v1/exercises",
            headers={"X-Api-Key": api_key},
            params={"muscle": muscle},
            timeout=5
        )
        response.raise_for_status()
        exercises_data = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"request_id={request.request_id} error={str(e)}")
        exercises_data = []

    plans_data = []
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, name, user_id, created_at FROM workout_plans;")
            rows = cur.fetchall()
            plans_data = [{"id": r[0], "name": r[1], "user_id": r[2], "created_at": str(r[3])} for r in rows]
        except Exception as e:
            logger.error(f"DB error: {str(e)}")
        finally:
            conn.close()

    return jsonify({
        "exercises": exercises_data,
        "plans": plans_data,
        "muscle_group": muscle
    })

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)