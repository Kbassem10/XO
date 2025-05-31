# 🎮 Tic Tac Toe AI Challenge

A beautiful, modern Tic Tac Toe game where you can challenge an AI opponent powered by the minimax algorithm.

## Features

- 🎨 **Beautiful UI**: Modern design with TailwindCSS and smooth animations
- 🤖 **Smart AI**: Minimax algorithm ensures the AI plays optimally
- 📊 **Score Tracking**: Persistent score tracking using localStorage
- 🎯 **Responsive Design**: Works perfectly on desktop and mobile
- ⚡ **Real-time Gameplay**: Instant feedback and smooth interactions
- 🔄 **Game Reset**: Easy game reset functionality

## How to Play

1. You are **X** (red), the AI is **O** (blue)
2. Click on any empty cell to make your move
3. The AI will automatically respond with its move
4. First to get three in a row (horizontally, vertically, or diagonally) wins!
5. If the board fills up with no winner, it's a draw

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Flask

### Installation
1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd XO
   ```

3. Install Flask if you don't have it:
   ```bash
   pip install flask
   ```

### Running the Application

#### Method 1: Using Flask CLI (Recommended)
```bash
python -m flask run --debug
```

#### Method 2: Direct Python execution
```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

## Project Structure

```
XO/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Frontend HTML template
├── static/
│   └── main.js           # Game logic and UI interactions
├── utils/
│   ├── __init__.py
│   ├── game_instructions.py  # Core game logic (winner checking, draw detection)
│   ├── minimax.py            # Minimax algorithm implementation
│   └── find_best_move.py     # AI move selection
├── tests/
│   └── test_xo_game.py      # Unit tests for game functions
└── README.md               # This file
```

## API Endpoints

### `GET /`
- Returns the main game page with an empty board

### `POST /play`
- **Body**: `{"board": [[...], [...], [...]]}`
- **Response**: Game state after AI move
- **Example**:
  ```json
  {
    "game_status": "ongoing",
    "result": "ONGOING",
    "board": [["X", " ", " "], [" ", "O", " "], [" ", " ", " "]]
  }
  ```

### `POST /reset`
- Resets the game to initial state
- **Response**: Empty board and reset game status

## Game Logic

### Minimax Algorithm
The AI uses the minimax algorithm to evaluate all possible future game states and choose the optimal move. This ensures the AI plays perfectly and will never lose (at worst, it will draw).

### Scoring System
- **AI Win**: +1 point
- **Human Win**: +1 point  
- **Draw**: +1 point
- Scores are saved in browser localStorage

## Technical Features

### Frontend (JavaScript/TailwindCSS)
- **Class-based Architecture**: Clean, maintainable code structure
- **Async/Await**: Modern JavaScript for API communication
- **Local Storage**: Persistent score tracking
- **Responsive Design**: Mobile-friendly interface
- **Animations**: Smooth transitions and feedback
- **Error Handling**: Graceful error management and user feedback

### Backend (Flask/Python)
- **RESTful API**: Clean API design
- **Error Handling**: Comprehensive error management
- **Game State Management**: Robust board state handling
- **Minimax AI**: Optimal move calculation

## Development

### Running Tests
```bash
cd tests
python test_xo_game.py
```

### Adding Features
The codebase is designed to be easily extensible:
- Game logic is in `utils/game_instructions.py`
- AI logic is in `utils/minimax.py` and `utils/find_best_move.py`
- Frontend logic is in `static/main.js`
- UI styling uses TailwindCSS classes

## Easter Eggs

Try entering the Konami Code (↑↑↓↓←→←→BA) while playing! 🎮

## Browser Compatibility

- Chrome/Edge: Full support
- Firefox: Full support  
- Safari: Full support
- Mobile browsers: Full support

## Contributing

Feel free to fork this project and submit pull requests for any improvements!

## License

This project is open source and available under the MIT License.
