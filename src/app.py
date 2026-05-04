# PlexPrep Flask Application
# Provides a basic web interface for the media monitoring system

from flask import Flask, jsonify
from pathlib import Path
from main import scan_media_library

app = Flask(__name__)

log_file = Path("data/logs.csv")


@app.route("/")
def home():
    return """
    <h1>PlexPrep Media Monitor</h1>
    <p>System is running.</p>
    <ul>
        <li><a href="/status">System Status</a></li>
        <li><a href="/logs">View Logs</a></li>
        <li><a href="/scan">Run Media Scan</a></li>
    </ul>
    """


@app.route("/status")
def status():
    return jsonify({
        "system": "PlexPrep",
        "status": "running",
        "layer": "Application + Networking",
        "protocol": "HTTP (Flask)"
    })


@app.route("/logs")
def logs():
    if not log_file.exists():
        return "No logs found."

    with open(log_file, "r") as f:
        return f"<pre>{f.read()}</pre>"


@app.route("/scan")
def scan():
    results = scan_media_library()
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
