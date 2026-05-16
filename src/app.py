# PlexPrep Flask Application
# Provides a basic dashboard and API endpoints for the media monitoring system
from flask import Flask, jsonify
from pathlib import Path
from main import scan_media_library ,get_storage_stats

app = Flask(__name__)

log_file = Path("data/logs.csv")

@app.route("/")
def home():
    results = scan_media_library()
    storage = get_storage_stats()
    if storage["usage_percent"] < 70:
        disk_class = "healthy"
    elif storage["usage_percent"] < 90:
        disk_class = "warning"
    else:
        disk_class = "critical"

    total_files = len(results)
    movie_count = sum(1 for item in results if item["type"] == "Movie")
    tv_count = sum(1 for item in results if item["type"] == "TV Show")
    valid_count = sum(1 for item in results if item["status"] == "valid")
    needs_rename_count = sum(1 for item in results if item["status"] == "needs_rename")

    table_rows = ""

    for item in results:
        status_class = "valid" if item["status"] == "valid" else "warning"

        table_rows += f"""
        <tr>
            <td>{item["file"]}</td>
            <td>{item["type"]}</td>
            <td class="{status_class}">{item["status"]}</td>
            <td>{item["suggested_name"]}</td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>PlexPrep Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #0f0f0f;
                color: #ffffff;
                margin: 0;
                padding: 30px;
            }}

            h1 {{
                color: #e5a00d;
                margin-bottom: 5px;
            }}

            h2 {{
                color: #ffffff;
                margin-top: 30px;
            }}

            p {{
                color: #d1d5db;
            }}

            .cards {{
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
                margin: 30px 0;
            }}

            .card {{
                background-color: #1f1f1f;
                border-left: 5px solid #e5a00d;
                padding: 20px;
                border-radius: 10px;
                min-width: 150px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
            }}

            .card h2 {{
                margin: 0;
                font-size: 30px;
                color: #e5a00d;
            }}

            .card p {{
                margin: 5px 0 0;
                color: #f3f4f6;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                background-color: #1a1a1a;
                border-radius: 10px;
                overflow: hidden;
            }}

            th, td {{
                padding: 12px;
                border-bottom: 1px solid #333333;
                text-align: left;
            }}

            th {{
                background-color: #262626;
                color: #e5a00d;
            }}

            tr:hover {{
                background-color: #242424;
            }}

            .valid {{
                color: #ffffff;
                font-weight: bold;
            }}

            .warning {{
                color: #e5a00d;
                font-weight: bold;
            }}

           .card h2.healthy {{
               color: #22c55e;
            }}

           .card h2.warning {{
               color: #e5a00d;
            }}

           .card h2.critical {{
               color: #ef4444;
   }}

            a {{
                color: #e5a00d;
                text-decoration: none;
                font-weight: bold;
            }}

            a:hover {{
                color: #ffffff;
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <h1>PlexPrep Media Monitor</h1>
        <p>Smart connected media server monitoring and Plex file organisation dashboard.</p>
<div class="cards">

    <div class="card">
        <h2>{total_files}</h2>
        <p>Total Files</p>
    </div>

    <div class="card">
        <h2>{movie_count}</h2>
        <p>Movies</p>
    </div>

    <div class="card">
        <h2>{tv_count}</h2>
        <p>TV Episodes</p>
    </div>

    <div class="card">
        <h2>{valid_count}</h2>
        <p>Valid Files</p>
    </div>

    <div class="card">
        <h2>{needs_rename_count}</h2>
        <p>Needs Rename</p>
    </div>

</div>

<div class="cards">

   <div class="card">
    <h2 class="{disk_class}">{storage["usage_percent"]}%</h2>
    <p>Disk Usage</p>
</div>

    <div class="card">
        <h2>{storage["total_gb"]} GB</h2>
        <p>Total Capacity</p>
    </div>

    <div class="card">
        <h2>{storage["used_gb"]} GB</h2>
        <p>Used Capacity</p>
    </div>

    <div class="card">
        <h2>{storage["free_gb"]} GB</h2>
        <p>Free Capacity</p>
    </div>
    

</div>
   
        <h2>Scan Results</h2>

        <table>
            <tr>
                <th>File</th>
                <th>Type</th>
                <th>Status</th>
                <th>Rename Suggestions</th>
            </tr>
            {table_rows}
        </table>

        <p>
            <a href="/scan">View JSON Scan</a> |
            <a href="/logs">View Logs</a> |
            <a href="/status">System Status</a>
        </p>
    </body>
    </html>
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