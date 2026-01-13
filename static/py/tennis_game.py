"""
Classic Tennis/Pong Game - Python/PyScript Implementation
Ported from JavaScript to Python for browser execution via Pyodide
"""

from js import document, window
from pyodide.ffi import create_proxy
import math
import random

# Game constants
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_RADIUS = 10
PADDLE_OFFSET = 30
WINNING_SCORE = 3

# Colors (neon arcade style)
COLOR_BG = "#0a0a0a"
COLOR_PADDLE = "#00ff00"
COLOR_BALL = "#ff00ff"
COLOR_CENTER_LINE = "#333333"


class Paddle:
    """Represents a paddle in the game"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.score = 0

    def draw(self, ctx):
        ctx.fillStyle = COLOR_PADDLE
        ctx.shadowColor = COLOR_PADDLE
        ctx.shadowBlur = 15
        ctx.fillRect(self.x, self.y, self.width, self.height)
        ctx.shadowBlur = 0

    def move_to(self, y):
        """Move paddle to y position (clamped to canvas bounds)"""
        self.y = max(0, min(y - self.height / 2, CANVAS_HEIGHT - self.height))


class Ball:
    """Represents the ball in the game"""
    def __init__(self):
        self.reset()

    def reset(self):
        """Reset ball to center with random direction"""
        self.x = CANVAS_WIDTH / 2
        self.y = CANVAS_HEIGHT / 2
        self.radius = BALL_RADIUS

        # Random direction with slight angle
        angle = random.uniform(-0.5, 0.5)
        direction = random.choice([-1, 1])

        self.speed = 6
        self.vx = self.speed * direction
        self.vy = self.speed * angle

    def draw(self, ctx):
        ctx.beginPath()
        ctx.arc(self.x, self.y, self.radius, 0, 2 * math.pi)
        ctx.fillStyle = COLOR_BALL
        ctx.shadowColor = COLOR_BALL
        ctx.shadowBlur = 20
        ctx.fill()
        ctx.shadowBlur = 0

    def update(self):
        """Update ball position"""
        self.x += self.vx
        self.y += self.vy

        # Bounce off top and bottom walls
        if self.y - self.radius <= 0 or self.y + self.radius >= CANVAS_HEIGHT:
            self.vy *= -1
            self.y = max(self.radius, min(self.y, CANVAS_HEIGHT - self.radius))


class AIController:
    """Simple AI controller for the computer paddle"""
    def __init__(self, paddle, difficulty=0.5):
        self.paddle = paddle
        self.difficulty = difficulty
        self.target_y = CANVAS_HEIGHT / 2
        self.reaction_delay = 0  # Frames before AI reacts to ball direction change
        self.frames_since_direction_change = 0
        self.last_ball_vx = 0

    def update(self, ball):
        """Update AI paddle position based on ball"""
        # Detect when ball changes direction (was hit by player)
        if ball.vx > 0 and self.last_ball_vx <= 0:
            self.frames_since_direction_change = 0
            self.reaction_delay = random.randint(15, 35)  # Random delay before reacting
        self.last_ball_vx = ball.vx

        # Only react when ball is coming towards AI AND after reaction delay
        if ball.vx > 0:
            self.frames_since_direction_change += 1

            # Wait for reaction delay before tracking
            if self.frames_since_direction_change < self.reaction_delay:
                return  # AI is "thinking"

            # Predict where ball will be
            if ball.vx != 0:
                time_to_reach = (self.paddle.x - ball.x) / ball.vx
                predicted_y = ball.y + ball.vy * time_to_reach

                # Add some randomness based on difficulty
                error = (1 - self.difficulty) * 150  # Increased error range
                self.target_y = predicted_y + random.uniform(-error, error)

        # Move towards target with some lag
        diff = self.target_y - (self.paddle.y + self.paddle.height / 2)
        move_speed = 5 * self.difficulty  # Slightly slower base speed

        if abs(diff) > move_speed:
            if diff > 0:
                self.paddle.y += move_speed
            else:
                self.paddle.y -= move_speed

        # Clamp to bounds
        self.paddle.y = max(0, min(self.paddle.y, CANVAS_HEIGHT - self.paddle.height))


class TennisGame:
    """Main game class"""
    def __init__(self):
        self.canvas = document.getElementById("game-canvas")
        self.ctx = self.canvas.getContext("2d")
        self.overlay = document.getElementById("game-overlay")
        self.start_btn = document.getElementById("start-btn")

        # Game objects
        self.player = Paddle(PADDLE_OFFSET, CANVAS_HEIGHT / 2 - PADDLE_HEIGHT / 2)
        self.ai_paddle = Paddle(
            CANVAS_WIDTH - PADDLE_OFFSET - PADDLE_WIDTH,
            CANVAS_HEIGHT / 2 - PADDLE_HEIGHT / 2
        )
        self.ball = Ball()
        self.ai = AIController(self.ai_paddle)

        # Game state
        self.running = False
        self.game_over = False
        self.animation_id = None

        # Score display elements
        self.player_score_el = document.getElementById("player-score")
        self.ai_score_el = document.getElementById("ai-score")

        # Setup input
        self.setup_input()

        # Draw initial state
        self.draw()

    def setup_input(self):
        """Setup mouse movement and button handlers"""
        def on_mouse_move(event):
            if not self.running:
                return
            rect = self.canvas.getBoundingClientRect()
            mouse_y = event.clientY - rect.top
            self.player.move_to(mouse_y)

        def on_start_click(event):
            self.start()

        self.mouse_proxy = create_proxy(on_mouse_move)
        self.start_proxy = create_proxy(on_start_click)

        self.canvas.addEventListener("mousemove", self.mouse_proxy)
        self.start_btn.addEventListener("click", self.start_proxy)

    def start(self):
        """Start the game"""
        self.running = True
        self.game_over = False
        self.player.score = 0
        self.ai_paddle.score = 0
        self.ball.reset()
        self.update_score_display()
        self.overlay.classList.add("hidden")
        self.game_loop()

    def game_loop(self):
        """Main game loop"""
        if not self.running:
            return

        self.update()
        self.draw()

        if not self.game_over:
            self.animation_id = window.requestAnimationFrame(
                create_proxy(lambda _: self.game_loop())
            )

    def update(self):
        """Update game state"""
        # Update ball
        self.ball.update()

        # Update AI
        self.ai.update(self.ball)

        # Check paddle collisions
        self.check_paddle_collision(self.player)
        self.check_paddle_collision(self.ai_paddle)

        # Check scoring
        if self.ball.x - self.ball.radius <= 0:
            # AI scores
            self.ai_paddle.score += 1
            self.update_score_display()
            if self.check_win():
                return
            self.ball.reset()

        elif self.ball.x + self.ball.radius >= CANVAS_WIDTH:
            # Player scores
            self.player.score += 1
            self.update_score_display()
            if self.check_win():
                return
            self.ball.reset()

    def check_paddle_collision(self, paddle):
        """Check and handle ball-paddle collision"""
        if (self.ball.x - self.ball.radius <= paddle.x + paddle.width and
            self.ball.x + self.ball.radius >= paddle.x and
            self.ball.y >= paddle.y and
            self.ball.y <= paddle.y + paddle.height):

            # Reverse horizontal direction
            self.ball.vx *= -1.05  # Slight speed increase

            # Adjust vertical speed based on where ball hit paddle
            hit_pos = (self.ball.y - paddle.y) / paddle.height
            self.ball.vy = (hit_pos - 0.5) * 10

            # Move ball outside paddle to prevent multiple collisions
            if paddle.x < CANVAS_WIDTH / 2:
                self.ball.x = paddle.x + paddle.width + self.ball.radius
            else:
                self.ball.x = paddle.x - self.ball.radius

    def check_win(self):
        """Check if someone has won"""
        if self.player.score >= WINNING_SCORE:
            self.end_game("YOU WIN!")
            return True
        elif self.ai_paddle.score >= WINNING_SCORE:
            self.end_game("GAME OVER")
            return True
        return False

    def end_game(self, message):
        """End the game and show message"""
        self.running = False
        self.game_over = True

        # Show overlay with result
        self.overlay.classList.remove("hidden")
        self.overlay.innerHTML = f'''
            <p class="arcade-instructions">{message}</p>
            <p class="arcade-instructions-sub">Final Score: {self.player.score} - {self.ai_paddle.score}</p>
            <button id="restart-btn" class="arcade-start-btn">
                PLAY AGAIN
            </button>
        '''

        # Setup restart button
        restart_btn = document.getElementById("restart-btn")
        restart_btn.addEventListener("click", create_proxy(lambda e: self.start()))

    def update_score_display(self):
        """Update the score display elements"""
        self.player_score_el.textContent = str(self.player.score)
        self.ai_score_el.textContent = str(self.ai_paddle.score)

    def draw(self):
        """Draw the game"""
        ctx = self.ctx

        # Clear canvas
        ctx.fillStyle = COLOR_BG
        ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)

        # Draw center line
        ctx.setLineDash([10, 10])
        ctx.strokeStyle = COLOR_CENTER_LINE
        ctx.lineWidth = 2
        ctx.beginPath()
        ctx.moveTo(CANVAS_WIDTH / 2, 0)
        ctx.lineTo(CANVAS_WIDTH / 2, CANVAS_HEIGHT)
        ctx.stroke()
        ctx.setLineDash([])

        # Draw game objects
        self.player.draw(ctx)
        self.ai_paddle.draw(ctx)
        self.ball.draw(ctx)


# Initialize game when script loads
game = TennisGame()
