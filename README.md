# plexprep-media-monitor
# Smart Connected Media Server Monitoring and Automated Plex File Organisation System
## Project Overview
PlexPrep is a connected IoT-style media server monitoring and automation system designed to improve the management of home media libraries.

The system monitors designated media folders, analyses file naming structures, tracks server health metrics such as storage usage, and automates file organisation for Plex-compatible naming conventions.

 PlexPrep aims to provide users with a practical tool for:

- Monitoring media server health
- Tracking storage space usage
- Detecting newly added media files
- Identifying incorrectly named or misplaced files
- Suggesting or applying Plex-friendly renaming conventions
- Logging system activity and file events
- Providing alerts and dashboard visualisation

# Project Objectives
- Build a connected application that demonstrates data source, processing, networking, and application layers
- Simulate or monitor a media library environment
- Automate file organisation tasks
- Provide real-time monitoring and alerts
- Develop a professional GitHub-based project with clear documentation and regular version control

 # Core Features (Planned)
# Release 1:
- Media folder scanning
- Storage monitoring
- Basic logging
- File naming analysis
- Console output
# Release 2:
- Flask web dashboard
- HTTP networking/API
- Structured JSON messaging
- Historical logs
- Dashboard visualisation
# Release 3:
- Automated file renaming suggestions
- Duplicate file detection
- Live updates
- Improved UI
- Alerts and notifications
# Stretch Goals:
- Metadata integration (TMDB/OMDb)
- Remote deployment
- Configurable settings dashboard
- Advanced analytics

# Technologies Used
# Programming Languages:
- Python
- HTML
- CSS
- JavaScript
# Frameworks / Libraries:
- Flask
- watchdog
- pathlib / os / shutil
- regex
- JSON
- SQLite / CSV
# Tools:
- GitHub
- Git
- VS Code
- Raspberry Pi (optional deployment)
- Local PC development environment
# System Architecture
``` text
Media Folder / Server Storage
        ↓
Data Collection & File Monitoring
        ↓
Processing Engine (Analysis / Renaming / Alerts)
        ↓
Networking Layer (HTTP API / Flask)
        ↓
Dashboard / Logs / User Alerts
```
# Repository Structure
``` text
 plexprep-media-monitor/
├── README.md
├── proposal.md
├── .gitignore
├── src/
│   └── main.py
├── data/
│   └── logs.csv
└── test_media/
    ├── movies/
    └── tv/
```
# Current Development Stage
# Week 1:
- Project proposal
- GitHub setup
- Documentation
- Folder structure
- Initial media scanner prototype
- Future Development Roadmap
# Week 2:
- Media scanning engine
- File analysis system
- Storage monitoring
# Week 3:
- Networking implementation
- Flask backend
- JSON messaging
# Week 4:
- Dashboard UI
- Alerts
- Historical data
# Week 5:
- Final testing
- GitHub cleanup
- Demo video
- Documentation refinement
- Assignment Context

# This project is being developed as part of Assignment 2 for Computer Systems and Networks, focusing on connected devices, networking, IoT architecture, and practical system integration.

# Author

Student Name: Patrick O'Neill
Student ID: 20119129

# Status
 In Development – Week 1 Proposal & Initial Setup
