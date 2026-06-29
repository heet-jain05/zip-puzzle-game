# Zip Puzzle Game

A full-stack web-based puzzle game where players solve a shuffled tile puzzle in minimum moves and time. The application includes score tracking, persistent leaderboard storage, and an interactive browser-based interface.

## Features

- Interactive puzzle gameplay
- Shuffle and restart functionality
- Move counter tracking
- Completion detection
- Persistent leaderboard system
- Score storage using SQLite database
- Responsive web interface
- Fast Python backend processing

## Tech Stack

- Python
- SQLite
- HTML5
- CSS3
- JavaScript
- Flask (if used)

## Project Structure

```text
zip-puzzle-game/
│
├── frontend/
│   ├── index.html
│   └── leaderboard.html
│
├── backend/
│   ├── main.py
│   └── data.db
│
├── README.md
└── .gitignore
```

## Installation

### Clone Repository

```bash
git clone https://github.com/heet-jain05/zip-puzzle-game.git
```

### Navigate to Backend

```bash
cd zip-puzzle-game/backend
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Backend Server

```bash
python main.py
```

### Open Frontend

Open:

```text
frontend/index.html
```

in your browser.

## Future Enhancements

- Multiple difficulty levels
- Multiplayer mode
- AI puzzle solver
- Timer functionality
- Theme customization
- Online leaderboard support

## Author

**Heet Jain**
