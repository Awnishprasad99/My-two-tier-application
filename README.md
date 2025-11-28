# My Two-Tier Application

A simple two-tier application running on Docker with Flask (web tier) and MySQL (database tier).

## Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Flask App     │───▶│     MySQL       │
│   (Web Tier)    │    │  (Database Tier)│
│   Port: 5000    │    │   Port: 3306    │
└─────────────────┘    └─────────────────┘
```

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/Awnishprasad99/My-two-tier-application.git
cd My-two-tier-application
```

2. Create the environment file:
```bash
cp .env.example .env
# Edit .env and set secure passwords
```

3. Build and run the containers:
```bash
docker-compose up --build
```

4. Access the application at [http://localhost:5000](http://localhost:5000)

## Services

### Web Tier (Flask)
- Python Flask web application
- Connects to MySQL database
- Exposes port 5000

### Database Tier (MySQL)
- MySQL 8.0 database
- Persistent data storage using Docker volumes
- Exposes port 3306

## Stopping the Application

```bash
docker-compose down
```

To remove all data (including the database volume):
```bash
docker-compose down -v
```

## Project Structure

```
.
├── app.py              # Flask application
├── Dockerfile          # Docker image for Flask app
├── docker-compose.yml  # Docker Compose configuration
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── templates/
│   └── index.html      # HTML template
└── README.md           # This file
```
