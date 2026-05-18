# PlexPrep Flask Application
# Provides a basic dashboard and API endpoints for the media monitoring system
from turtle import color

from flask import Flask, jsonify
from pathlib import Path
from main import scan_media_library ,get_storage_stats, apply_safe_renames

app = Flask(__name__)

log_file = Path("data/logs.csv")
def render_page(title, content, top_button=False):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #0f0f0f;
                color: #ffffff;
                margin: 0;
                padding: 30px;
            }}

            .box {{
                background-color: #1f1f1f;
                border-left: 5px solid #e5a00d;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.35);
            }}

            h1 {{
                color: #e5a00d;
                margin-top: 0;
            }}

            pre, table {{
                background-color: #111111;
                padding: 15px;
                border-radius: 8px;
                overflow-x: auto;
                color: #f3f4f6;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
            }}

            th, td {{
                padding: 12px;
                border-bottom: 1px solid #333333;
                text-align: left;
            }}

            th {{
                color: #e5a00d;
            }}

            a {{
                display: inline-block;
                margin-right: 10px;
                margin-top: 20px;
                margin-bottom: 20px;
                color: #0f0f0f;
                background-color: #e5a00d;
                padding: 10px 16px;
                border-radius: 6px;
                text-decoration: none;
                font-weight: bold;
            }}

            a:hover {{
                background-color: #ffffff;
            }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>{title}</h1>
          {"<a href='/'>Return to Dashboard</a>" if top_button else ""}
            {content}
            <a href="/">Return to Dashboard</a>
        </div>
    </body>
    </html>
    """

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

        metadata = item.get("metadata")

        if isinstance(metadata, dict):

            # Movie metadata message
            if "message" in metadata:
                metadata_display = f"""
                <div class="metadata-card">
                    <strong>{metadata.get("message")}</strong>
                </div>
                """

            # TV metadata
            else:
                metadata_display = f"""
                <div class="metadata-card">
                    <strong>{metadata.get("title", "Unknown Title")}</strong><br>
                    {metadata.get("airdate", "Unknown airdate")}<br>
                    {metadata.get("runtime", "Unknown runtime")} mins
                </div>
                """

        elif metadata:
            metadata_display = metadata

        else:
            metadata_display = "N/A"

        table_rows += f"""
        <tr>
            <td>{item["file"]}</td>
            <td>{item["type"]}</td>
            <td class="{status_class}">{item["status"]}</td>
            <td>{item["suggested_name"]}</td>
            <td>{metadata_display}</td>
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

            .metadata-card {{
                 background-color: #181818;
                 border-left: 3px solid #e5a00d;
                 padding: 10px;
                 border-radius: 6px;
                 line-height: 1.6;
                min-width: 180px;}}

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
                <th>Metadata</th>
            </tr>
            {table_rows}
        </table>

        <p>
            <a href="/scan">Media Scan Results</a> |
            <a href="/rename-preview">Rename Preview</a> |
            <a href="/rename">Apply Safe Rename</a> |
            <a href="/logs">Activity Logs</a> |
            <a href="/status">Server Status</a>
        </p>
    </body>
    </html>
    """

@app.route("/status")
def status():
    content = """
    <table>
        <tr><th>Item</th><th>Status</th></tr>
        <tr><td>System</td><td>PlexPrep</td></tr>
        <tr><td>Application Status</td><td>Running</td></tr>
        <tr><td>Layer</td><td>Application + Networking</td></tr>
        <tr><td>Protocol</td><td>HTTP Flask</td></tr>
    </table>
    """

    return render_page("System Status", content)

@app.route("/logs")
def logs():
    if not log_file.exists():
        return render_page("Logs", "<p>No logs found.</p>")

    rows = ""

    with open(log_file, "r") as f:
        lines = f.readlines()

    # Skip the header row
    for line in lines[1:]:
        columns = line.strip().split(",")

        if len(columns) >= 5:
            rows += f"""
            <tr>
                <td>{columns[0]}</td>
                <td>{columns[1]}</td>
                <td>{columns[2]}</td>
                <td>{columns[3]}</td>
                <td>{columns[4]}</td>
            </tr>
            """

    content = f"""
    <table>
        <tr>
            <th>Timestamp</th>
            <th>File Path</th>
            <th>Media Type</th>
            <th>Status</th>
            <th>Action</th>
        </tr>
        {rows}
    </table>
    """

    return render_page("System Logs", content, top_button=True)

@app.route("/scan")
def scan():
    results = scan_media_library()

    rows = ""

    for item in results:

        metadata = item.get("metadata")

        if isinstance(metadata, dict):
            metadata_display = f"""
            <div class="metadata-card">
                <strong>{metadata.get("title", "Unknown Title")}</strong><br>
                {metadata.get("airdate", "Unknown airdate")}<br>
                {metadata.get("runtime", "Unknown runtime")} mins
            </div>
            """
        elif metadata:
            metadata_display = metadata
        else:
            metadata_display = "N/A"

        rows += f"""
        <tr>
            <td>{item["file"]}</td>
            <td>{item["type"]}</td>
            <td>{item["status"]}</td>
            <td>{item["suggested_name"]}</td>
            <td>{metadata_display}</td>
        </tr>
        """

    content = f"""
    <table>
        <tr>
            <th>File</th>
            <th>Type</th>
            <th>Status</th>
            <th>Rename Suggestion</th>
            <th>Metadata</th>
        </tr>
        {rows}
    </table>
    """

    return render_page("Media Scan Results", content, top_button=True)

@app.route("/rename-preview")
def rename_preview():
    results = scan_media_library()

    rename_items = [
        item for item in results
        if item["status"] == "needs_rename"
        and item["suggested_name"]
    ]

    if not rename_items:
        return render_page(
            "Rename Preview",
            "<p>No files currently need renaming.</p>"
        )

    rows = ""

    for item in rename_items:
        rows += f"""
        <tr>
            <td>{item["file"]}</td>
            <td>{item["suggested_name"]}</td>
        </tr>
        """

    content = f"""
    <table>
        <tr>
            <th>Current File</th>
            <th>Suggested Rename</th>
        </tr>
        {rows}
    </table>
    """

    return render_page("Rename Preview", content, top_button=True)

@app.route("/rename")
def rename_files():
    renamed_files = apply_safe_renames()

    if not renamed_files:
        return render_page(
            "No Files Needed Renaming",
            "<p>Your media library is already organised correctly.</p>"
        )

    rows = ""

    for item in renamed_files:
        rows += f"""
        <tr>
            <td>{item["old_file"]}</td>
            <td>{item["new_file"]}</td>
            <td>{item["status"]}</td>
        </tr>
        """

    content = f"""
    <p>The following files were safely renamed:</p>
    <table>
        <tr>
            <th>Old File</th>
            <th>New File</th>
            <th>Status</th>
        </tr>
        {rows}
    </table>
    """

    return render_page("Files Renamed Successfully", content)

if __name__ == "__main__":
    app.run(debug=True)