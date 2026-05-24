# plexprep-media-monitor

# Smart Connected Media Server Monitoring and Automated Plex File Organisation System

## Project Overview

PlexPrep is a connected media server monitoring and automation system designed to improve the management, validation, and organisation of home media libraries.

The system monitors designated media folders, analyses file naming structures, validates media metadata using external APIs, tracks server health metrics such as storage usage, and provides safe Plex-compatible rename suggestions through a Flask web dashboard.

PlexPrep was designed with a strong focus on safe automation. Rather than blindly renaming files, the system validates media against metadata sources and flags uncertain or unsafe cases for manual review.

PlexPrep aims to provide users with a practical tool for:

- Monitoring media server health
- Tracking storage space usage
- Detecting newly added media files
- Identifying incorrectly named or misplaced files
- Validating TV episode metadata
- Detecting subtitle languages
- Supporting multilingual subtitle files
- Suggesting Plex-friendly rename conventions
- Logging system activity and file events
- Providing dashboard visualisation and monitoring tools
- Preventing unsafe automatic renaming through manual review workflows

# Project Objectives

- Build a connected application that demonstrates data source, processing, networking, and  application layers
- Simulate and monitor a real-world media library environment
- Automate media organisation tasks safely
- Provide real-time monitoring and validation
- Demonstrate connected systems concepts using Flask and HTTP networking
- Develop a professional GitHub-based project with clear documentation and version control

# How PlexPrep Meets the Project Objectives

## Build a connected application that demonstrates data source, processing, networking, and application layers

PlexPrep demonstrates all major layers of a connected application architecture.

The data source layer is represented by the media library folders containing TV episodes, movies, subtitles, and supplementary media files. The application continuously scans these folders and retrieves file information for processing.

The processing layer analyses file naming structures, validates metadata using the TVMaze API, generates rename suggestions, detects subtitle languages, monitors storage usage, and applies manual review logic for uncertain cases.

The networking layer is implemented using Flask and HTTP communication. The Flask web server exposes the application dashboard through HTTP routes and allows media scan data to be accessed through a browser-based interface.

The application layer is represented by the Flask dashboard itself, which displays media information, metadata validation results, logs, rename suggestions, and system monitoring information to the user.

---

## Simulate and monitor a real-world media library environment

PlexPrep simulates a realistic home media server structure using organised movie and TV show folders containing intentionally mixed valid and invalid media files.

The project includes:
- correctly named Plex-compatible files
- badly named media files
- subtitle files in multiple languages
- invalid subtitle files
- manual review cases
- overflow or unknown episode cases

This allows the system to demonstrate realistic media management scenarios commonly encountered in real Plex or Jellyfin media libraries.

---

## Automate media organisation tasks safely

The project automates media organisation by generating Plex-compatible rename suggestions for incorrectly named TV and movie files.

However, the system was intentionally designed around safe automation principles. Rather than blindly renaming files, PlexPrep validates media against external metadata before suggesting changes.

The application also:
- prevents unsafe subtitle renaming
- detects unknown subtitle languages
- flags uncertain files for manual review
- prevents invalid episode numbering beyond official metadata
- avoids automatic handling of unsupported media extras

This demonstrates an emphasis on data integrity and safe automation workflows.

---

## Provide real-time monitoring and validation

PlexPrep provides real-time monitoring by scanning media folders and immediately displaying results through the Flask dashboard.

The application monitors:
- storage usage
- file naming compliance
- metadata validation status
- subtitle language detection
- rename suggestions
- manual review warnings
- scan activity logs

This allows users to monitor the health and organisation state of the media library in real time.

---

## Demonstrate connected systems concepts using Flask and HTTP networking

The application uses Flask to implement a lightweight HTTP-based connected system.

The Flask server:
- handles incoming HTTP requests
- serves dashboard pages
- displays live scan information
- processes application data
- provides browser-based access to monitoring information

This demonstrates practical networking concepts including:
- client/server architecture
- HTTP communication
- routing
- application-layer services
- connected dashboard interfaces

The project also integrates external API communication through TVMaze metadata requests, further demonstrating connected systems integration.

---

## Develop a professional GitHub-based project with clear documentation and version control

The project was developed using GitHub and Git version control throughout development.

The repository includes:
- structured source code organisation
- documented project architecture
- README documentation
- version-controlled feature development
- release tagging
- organised project structure

Development was managed through iterative commits and feature additions, reflecting a professional software development workflow.

# Final Features

## Release 1:
- Recursive media folder scanning
- Storage monitoring
- CSV activity logging
- File naming analysis
- Console scan output

## Release 2:
- Flask web dashboard
- HTTP networking/API
- Structured metadata display
- Historical activity logs
- Dashboard visualisation
- Storage health monitoring

## Release 3:
- Plex-compatible rename suggestions
- TV episode metadata validation
- Manual review workflows
- Safe rename architecture
- Improved UI/dashboard
- Rename preview system
- Overflow episode protection

## Stretch Goals:
- Subtitle language detection
- Multilingual subtitle support
- Subtitle validation workflows
- Metadata integration using TVMaze API
- Remote deployment
- Configurable settings dashboard
- Advanced analytics and reporting

# Technologies Used

## Programming Languages
- Python
- HTML
- CSS
- JavaScript

## Frameworks / Libraries
- Flask
- requests
- pathlib / shutil
- regex
- CSV

## APIs
- TVMaze API

## Tools
- GitHub
- Git
- VS Code
- GitHub Codespaces
- Local PC development environment

# System Architecture

```text
Media Library Folders
        ↓
File Scanning & Detection
        ↓
Metadata Validation Engine
        ↓
Rename Suggestion / Manual Review Logic
        ↓
Networking Layer (HTTP Flask Application)
        ↓
Dashboard / Logs / Monitoring Interface
```

# Repository Structure

```text
plexprep-media-monitor/
├── README.md
├── .gitignore
├── requirements.txt
├── src/
│   ├── app.py
│   └── main.py
├── data/
│   └── logs.csv
└── test_media/
    ├── Movies/
    └── TV/
```

# Current Development Stage

## Final Submission Version
- Media scanning engine completed
- Flask dashboard completed
- Metadata validation implemented
- Safe rename system implemented
- Manual review workflows implemented
- Subtitle language detection implemented
- Storage monitoring implemented
- Activity logging implemented
- GitHub repository completed
- Demo video preparation completed

# Future Improvements

A possible future improvement would be implementing more advanced episode identification logic for incorrectly named TV files. The current system safely suggests the next sequential episode number based on existing validated files within a season folder. While this reduces the risk of incorrect renaming, it does not attempt to intelligently determine the intended episode from vague or inconsistent filenames.

Future versions could improve this by analysing additional information such as:
- file creation order
- embedded media metadata
- release naming patterns
- external API search matching
- fuzzy string matching techniques

This would allow PlexPrep to make more accurate rename suggestions while still maintaining manual review safeguards for uncertain cases.

Another possible improvement would be expanding metadata support for movies. The current system validates movie folder naming structures, but future versions could integrate movie metadata providers such as OMDb or TMDb to automatically retrieve:
- movie titles
- release years
- posters
- genres
- runtime information
- ratings and descriptions

Additional future improvements could also include automatic organisation and classification of extra media content such as:
- behind-the-scenes clips
- commentary tracks
- interviews
- deleted scenes
- bonus features
- featurettes

At the moment, PlexPrep intentionally avoids automatically renaming or reorganising these files to prevent unsafe changes. Future versions could use metadata analysis, filename pattern recognition, or dedicated extras folders to safely classify and organise supplementary media content while still preserving manual review safeguards for uncertain cases.

Other future improvements may include:
- live filesystem monitoring
- remote deployment support
- configurable dashboard settings
- advanced analytics and reporting
- user authentication
- database integration for persistent storage

# Assignment Context

This project was developed as part of Assignment 2 for Computer Systems and Networks, focusing on connected applications, networking concepts, IoT-style architectures, monitoring systems, and practical software integration.

# How to Run the Project

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Flask application

```bash
python src/app.py
```

# Author

Student Name: Patrick O'Neill  
Student ID: 20119129

# Status

Final Submission Version – v1.0
