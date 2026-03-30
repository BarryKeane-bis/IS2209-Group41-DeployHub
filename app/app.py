import os
import requests
import logging
import uuid
import time
from flask import Flask, jsonify, request
from dotenv import load_dotenv

from pathlib import Path
load_dotenv(Path(__file__).parent.parent / '.env')

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

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

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/status")
def status():
    return jsonify({"status": "running", "db": "not connected yet"})

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

if __name__ == "__main__":
    app.run(debug=True)