"""
Guess My Number Game - Python/PyScript Implementation
Adapted from console game to browser GUI
"""

from js import document
from pyodide.ffi import create_proxy
import random


class GuessNumberGame:
    """Main game class managing both game modes"""

    def __init__(self):
        # DOM elements
        self.overlay = document.getElementById("game-overlay")
        self.start_btn = document.getElementById("start-btn")
        self.mode_display = document.getElementById("game-mode")
        self.message_display = document.getElementById("game-message")
        self.hint_display = document.getElementById("game-hint")
        self.range_display = document.getElementById("game-range")
        self.attempt_display = document.getElementById("attempt-count")

        # Player mode controls
        self.player_controls = document.getElementById("player-controls")
        self.guess_input = document.getElementById("guess-input")
        self.submit_btn = document.getElementById("submit-guess")

        # Computer mode controls
        self.computer_controls = document.getElementById("computer-controls")
        self.btn_higher = document.getElementById("btn-higher")
        self.btn_correct = document.getElementById("btn-correct")
        self.btn_lower = document.getElementById("btn-lower")

        # Game state
        self.current_mode = None  # 'player' or 'computer'
        self.secret_number = 0
        self.attempts = 0
        self.player_score = 0
        self.computer_score = 0

        # Computer mode state (binary search)
        self.low = 1
        self.high = 100
        self.computer_guess = 0

        # Setup event handlers
        self.setup_handlers()

    def setup_handlers(self):
        """Setup all button click handlers"""
        self.start_btn.addEventListener("click", create_proxy(lambda e: self.start_game()))
        self.submit_btn.addEventListener("click", create_proxy(lambda e: self.handle_player_guess()))
        self.guess_input.addEventListener("keypress", create_proxy(self.handle_keypress))
        self.btn_higher.addEventListener("click", create_proxy(lambda e: self.handle_computer_feedback("higher")))
        self.btn_lower.addEventListener("click", create_proxy(lambda e: self.handle_computer_feedback("lower")))
        self.btn_correct.addEventListener("click", create_proxy(lambda e: self.handle_computer_feedback("correct")))

    def handle_keypress(self, event):
        """Handle Enter key in input field"""
        if event.key == "Enter":
            self.handle_player_guess()

    def start_game(self):
        """Start the game with Mode 1 (player guesses)"""
        self.overlay.classList.add("hidden")
        self.start_player_mode()

    def start_player_mode(self):
        """Initialize Mode 1: Player guesses computer's number"""
        self.current_mode = "player"
        self.secret_number = random.randint(1, 100)
        self.attempts = 0

        # Update display
        self.mode_display.textContent = "MODE 1: YOUR TURN"
        self.message_display.textContent = "I'm thinking of a number between 1 and 100..."
        self.hint_display.textContent = ""
        self.range_display.textContent = "Range: 1 - 100"
        self.attempt_display.textContent = "0"

        # Show correct controls
        self.player_controls.classList.remove("hidden")
        self.computer_controls.classList.add("hidden")
        self.guess_input.value = ""
        self.guess_input.focus()

    def handle_player_guess(self):
        """Process the player's guess in Mode 1"""
        try:
            guess = int(self.guess_input.value)
        except (ValueError, TypeError):
            self.hint_display.textContent = "ENTER A NUMBER!"
            self.hint_display.style.color = "#ff6600"
            return

        if guess < 1 or guess > 100:
            self.hint_display.textContent = "1 TO 100 ONLY!"
            self.hint_display.style.color = "#ff6600"
            return

        self.attempts += 1
        self.attempt_display.textContent = str(self.attempts)
        self.guess_input.value = ""

        if guess < self.secret_number:
            self.hint_display.textContent = "TOO LOW!"
            self.hint_display.style.color = "#00ff00"
            self.message_display.textContent = f"Your guess: {guess}. Try higher!"
        elif guess > self.secret_number:
            self.hint_display.textContent = "TOO HIGH!"
            self.hint_display.style.color = "#ff6600"
            self.message_display.textContent = f"Your guess: {guess}. Try lower!"
        else:
            # Correct!
            self.player_wins()

    def player_wins(self):
        """Handle player winning Mode 1"""
        self.player_score = self.attempts
        self.hint_display.textContent = f"CORRECT! IT WAS {self.secret_number}!"
        self.hint_display.style.color = "#ff00ff"
        self.message_display.textContent = f"You got it in {self.attempts} tries!"

        # Hide input, show continue button
        self.player_controls.classList.add("hidden")

        # Show overlay with continue option
        self.overlay.classList.remove("hidden")
        self.overlay.innerHTML = '''
            <p class="arcade-instructions">NICE GUESSING!</p>
            <p class="arcade-instructions-sub">You found it in ''' + str(self.attempts) + ''' tries!</p>
            <p class="arcade-instructions-sub" style="color: #00ffff; margin-top: 1rem;">
                Now it's MY turn to guess YOUR number!
            </p>
            <button id="continue-btn" class="arcade-start-btn">
                CONTINUE TO MODE 2
            </button>
        '''
        continue_btn = document.getElementById("continue-btn")
        continue_btn.addEventListener("click", create_proxy(lambda e: self.start_computer_mode()))

    def start_computer_mode(self):
        """Initialize Mode 2: Computer guesses player's number"""
        self.overlay.classList.add("hidden")
        self.current_mode = "computer"
        self.attempts = 0
        self.low = 1
        self.high = 100

        # Update display
        self.mode_display.textContent = "MODE 2: MY TURN"
        self.message_display.textContent = "Think of a number between 1 and 100..."
        self.hint_display.textContent = "GOT IT? CLICK BELOW!"
        self.hint_display.style.color = "#00ffff"
        self.range_display.textContent = "I'll try to guess it!"
        self.attempt_display.textContent = "0"

        # Show correct controls
        self.player_controls.classList.add("hidden")
        self.computer_controls.classList.remove("hidden")

        # Make first guess after short delay
        self.make_computer_guess()

    def make_computer_guess(self):
        """Computer makes a guess using binary search"""
        self.attempts += 1
        self.attempt_display.textContent = str(self.attempts)

        # Binary search: guess middle of range
        self.computer_guess = (self.low + self.high) // 2

        self.message_display.textContent = "Is your number..."
        self.hint_display.textContent = str(self.computer_guess) + "?"
        self.hint_display.style.color = "#ff00ff"
        self.range_display.textContent = f"Searching: {self.low} - {self.high}"

    def handle_computer_feedback(self, feedback):
        """Process player's feedback on computer's guess"""
        if feedback == "higher":
            self.low = self.computer_guess + 1
            if self.low > self.high:
                self.cheating_detected()
                return
            self.make_computer_guess()

        elif feedback == "lower":
            self.high = self.computer_guess - 1
            if self.high < self.low:
                self.cheating_detected()
                return
            self.make_computer_guess()

        elif feedback == "correct":
            self.computer_wins()

    def cheating_detected(self):
        """Handle impossible feedback (player cheated)"""
        self.hint_display.textContent = "HEY! NO CHEATING!"
        self.hint_display.style.color = "#ff0000"
        self.message_display.textContent = "That's mathematically impossible... Let's try again!"
        self.computer_controls.classList.add("hidden")

        self.overlay.classList.remove("hidden")
        self.overlay.innerHTML = '''
            <p class="arcade-instructions" style="color: #ff0000;">CHEATER DETECTED!</p>
            <p class="arcade-instructions-sub">Your answers don't add up...</p>
            <button id="restart-btn" class="arcade-start-btn">
                TRY AGAIN
            </button>
        '''
        restart_btn = document.getElementById("restart-btn")
        restart_btn.addEventListener("click", create_proxy(lambda e: self.start_game()))

    def computer_wins(self):
        """Handle computer guessing correctly in Mode 2"""
        self.computer_score = self.attempts
        self.computer_controls.classList.add("hidden")

        # Compare scores
        if self.player_score < self.computer_score:
            result = "YOU WIN!"
            result_color = "#00ff00"
            result_msg = f"You: {self.player_score} tries | Computer: {self.computer_score} tries"
        elif self.computer_score < self.player_score:
            result = "COMPUTER WINS!"
            result_color = "#ff00ff"
            result_msg = f"Computer: {self.computer_score} tries | You: {self.player_score} tries"
        else:
            result = "IT'S A TIE!"
            result_color = "#ffff00"
            result_msg = f"Both guessed in {self.player_score} tries!"

        self.overlay.classList.remove("hidden")
        self.overlay.innerHTML = f'''
            <p class="arcade-instructions">YOUR NUMBER: {self.computer_guess}</p>
            <p class="arcade-instructions" style="color: {result_color}; margin-top: 1rem;">{result}</p>
            <p class="arcade-instructions-sub">{result_msg}</p>
            <button id="replay-btn" class="arcade-start-btn" style="margin-top: 1.5rem;">
                PLAY AGAIN
            </button>
        '''
        replay_btn = document.getElementById("replay-btn")
        replay_btn.addEventListener("click", create_proxy(lambda e: self.start_game()))


# Initialize game when script loads
game = GuessNumberGame()
