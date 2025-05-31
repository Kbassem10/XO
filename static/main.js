class TicTacToeGame {
    constructor() {
        this.board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']];
        this.gameActive = true;
        this.playerTurn = true; // Player starts first
        this.scores = {
            player: 0,
            ai: 0,
            draws: 0
        };
        
        this.initializeGame();
        this.loadScores();
    }

    initializeGame() {
        this.createBoard();
        this.bindEvents();
        this.updateStatus("Your turn! Click a cell to play");
    }

    createBoard() {
        const boardElement = document.getElementById('game-board');
        boardElement.innerHTML = '';

        for (let row = 0; row < 3; row++) {
            for (let col = 0; col < 3; col++) {
                const cell = document.createElement('div');
                cell.className = 'bg-white rounded-xl h-20 w-20 flex items-center justify-center text-3xl font-bold cursor-pointer cell-hover border-2 border-gray-200 hover:border-blue-300 transition-all duration-200';
                cell.dataset.row = row;
                cell.dataset.col = col;
                cell.addEventListener('click', (e) => this.handleCellClick(e));
                boardElement.appendChild(cell);
            }
        }
    }

    bindEvents() {
        document.getElementById('reset-btn').addEventListener('click', () => this.resetGame());
    }

    handleCellClick(event) {
        if (!this.gameActive || !this.playerTurn) return;

        const row = parseInt(event.target.dataset.row);
        const col = parseInt(event.target.dataset.col);

        // Check if cell is already occupied
        if (this.board[row][col] !== ' ') {
            this.showError("Cell already occupied!");
            return;
        }

        // Make player move
        this.makeMove(row, col, 'X');
        this.playerTurn = false;

        // Send move to server and get AI response
        this.sendMoveToServer();
    }

    makeMove(row, col, player) {
        this.board[row][col] = player;
        const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
        
        // Add the mark with animation
        cell.textContent = player;
        cell.classList.add('animate-bounce-in');
        
        // Apply styling based on player
        if (player === 'X') {
            cell.classList.add('x-mark');
            cell.classList.remove('cursor-pointer', 'hover:border-blue-300');
        } else {
            cell.classList.add('o-mark');
            cell.classList.remove('cursor-pointer', 'hover:border-blue-300');
        }
    }

    async sendMoveToServer() {
        this.showLoading(true);
        this.updateStatus("AI is thinking...");

        try {
            const response = await fetch('/play', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    board: this.board
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            this.handleServerResponse(data);

        } catch (error) {
            console.error('Error:', error);
            this.showError("Connection error. Please try again.");
            this.playerTurn = true;
        } finally {
            this.showLoading(false);
        }
    }

    handleServerResponse(data) {
        if (data.error) {
            this.showError(data.error);
            this.playerTurn = true;
            return;
        }

        // Update board with server response
        this.updateBoardFromServer(data.board);

        // Check game status
        if (data.game_status === 'finished') {
            this.handleGameEnd(data.result);
        } else {
            this.playerTurn = true;
            this.updateStatus("Your turn! Click a cell to play");
        }
    }

    updateBoardFromServer(serverBoard) {
        for (let row = 0; row < 3; row++) {
            for (let col = 0; col < 3; col++) {
                if (this.board[row][col] !== serverBoard[row][col]) {
                    // AI made a move here
                    this.makeMove(row, col, serverBoard[row][col]);
                }
                this.board[row][col] = serverBoard[row][col];
            }
        }
    }

    handleGameEnd(result) {
        this.gameActive = false;
        
        let message = "";
        let statusClass = "";

        switch (result) {
            case 'X_WINS':
                message = "🎉 Congratulations! You won!";
                statusClass = "bg-green-500/90";
                this.scores.player++;
                break;
            case 'O_WINS':
                message = "🤖 AI wins! Better luck next time!";
                statusClass = "bg-red-500/90";
                this.scores.ai++;
                break;
            case 'DRAW':
                message = "🤝 It's a draw! Great game!";
                statusClass = "bg-yellow-500/90";
                this.scores.draws++;
                break;
            default:
                message = "Game ended";
                statusClass = "bg-gray-500/90";
        }

        this.updateStatus(message, statusClass);
        this.updateScoreDisplay();
        this.saveScores();
        
        // Disable all cells
        const cells = document.querySelectorAll('#game-board > div');
        cells.forEach(cell => {
            cell.classList.remove('cursor-pointer', 'cell-hover');
        });
    }

    updateStatus(message, additionalClass = "") {
        const statusElement = document.getElementById('game-status');
        statusElement.textContent = message;
        
        // Reset classes
        statusElement.className = "bg-white/20 backdrop-blur-sm rounded-xl px-4 py-3 text-white font-semibold text-lg animate-fade-in";
        
        if (additionalClass) {
            statusElement.className = `${additionalClass} backdrop-blur-sm rounded-xl px-4 py-3 text-white font-semibold text-lg animate-fade-in`;
        }
    }

    async resetGame() {
        this.showLoading(true);
        
        try {
            const response = await fetch('/reset', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Reset game state
            this.board = data.board;
            this.gameActive = true;
            this.playerTurn = true;
            
            // Recreate the board
            this.createBoard();
            this.updateStatus("Your turn! Click a cell to play");
            
        } catch (error) {
            console.error('Error:', error);
            this.showError("Failed to reset game. Please refresh the page.");
        } finally {
            this.showLoading(false);
        }
    }

    updateScoreDisplay() {
        document.getElementById('player-score').textContent = this.scores.player;
        document.getElementById('ai-score').textContent = this.scores.ai;
        document.getElementById('draw-score').textContent = this.scores.draws;
    }

    saveScores() {
        localStorage.setItem('ticTacToeScores', JSON.stringify(this.scores));
    }

    loadScores() {
        const savedScores = localStorage.getItem('ticTacToeScores');
        if (savedScores) {
            this.scores = JSON.parse(savedScores);
            this.updateScoreDisplay();
        }
    }

    showLoading(show) {
        const loadingElement = document.getElementById('loading');
        if (show) {
            loadingElement.classList.remove('hidden');
        } else {
            loadingElement.classList.add('hidden');
        }
    }

    showError(message) {
        const statusElement = document.getElementById('game-status');
        const originalMessage = statusElement.textContent;
        
        // Show error message with red background
        statusElement.textContent = message;
        statusElement.className = "bg-red-500/90 backdrop-blur-sm rounded-xl px-4 py-3 text-white font-semibold text-lg animate-shake";
        
        // Restore original message after 3 seconds
        setTimeout(() => {
            statusElement.textContent = originalMessage;
            statusElement.className = "bg-white/20 backdrop-blur-sm rounded-xl px-4 py-3 text-white font-semibold text-lg animate-fade-in";
        }, 3000);
    }
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new TicTacToeGame();
});

// Add some fun easter eggs
document.addEventListener('keydown', (e) => {
    // Konami code: up, up, down, down, left, right, left, right, B, A
    const konamiCode = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'KeyB', 'KeyA'];
    
    if (!window.konamiProgress) window.konamiProgress = 0;
    
    if (e.code === konamiCode[window.konamiProgress]) {
        window.konamiProgress++;
        if (window.konamiProgress === konamiCode.length) {
            // Easter egg activated!
            document.body.style.filter = 'hue-rotate(180deg)';
            setTimeout(() => {
                document.body.style.filter = '';
            }, 5000);
            window.konamiProgress = 0;
        }
    } else {
        window.konamiProgress = 0;
    }
});
