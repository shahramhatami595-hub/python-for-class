import tkinter as tk
import random


class MiniCatchGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Catch the Star - Chapter 8")
        self.root.resizable(False, False)

        # Game state variables
        self.running = False
        self.score = 0
        self.star_speed = 4
        self.paddle_speed = 20

        # 1. Organize layout with Frames
        self.top_frame = tk.Frame(root, pady=8, bg="#2c3e50")
        self.top_frame.pack(fill="x")

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack()

        self.bottom_frame = tk.Frame(root, pady=8, bg="#2c3e50")
        self.bottom_frame.pack(fill="x")

        # Status display
        self.status_label = tk.Label(
            self.top_frame,
            text="Score: 0 | Position: (220, 360)",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#2c3e50",
        )
        self.status_label.pack()

        # 2. Canvas with at least three graphical objects
        self.canvas = tk.Canvas(
            self.canvas_frame, width=500, height=400, bg="#1a1a2e"
        )
        self.canvas.pack()

        # Object 1 & 2: Player Paddle + Decor Stripe (grouped with Canvas tag "player")
        self.paddle = self.canvas.create_rectangle(
            210, 360, 290, 375, fill="#00d2ff", outline="", tags="player"
        )
        self.paddle_stripe = self.canvas.create_line(
            215, 367, 285, 367, fill="white", width=2, tags="player"
        )

        # Object 3: Falling Star (Oval)
        self.star = self.canvas.create_oval(
            240, 20, 260, 40, fill="#ffd700", outline="#ffaa00", width=2, tags="star"
        )

        # 3. Start, Pause, and Reset Buttons
        tk.Button(
            self.bottom_frame, text="Start", width=10, command=self.start_game
        ).pack(side="left", padx=25)
        tk.Button(
            self.bottom_frame, text="Pause", width=10, command=self.pause_game
        ).pack(side="left", padx=25)
        tk.Button(
            self.bottom_frame, text="Reset", width=10, command=self.reset_game
        ).pack(side="right", padx=25)

        # 4. Event Bindings (4 Keyboard controls + Mouse click/drag)
        self.root.bind("<Left>", self.handle_move_left)
        self.root.bind("<Right>", self.handle_move_right)
        self.root.bind("<Up>", self.handle_speed_up)
        self.root.bind("<Down>", self.handle_speed_down)

        self.canvas.bind("<Button-1>", self.handle_mouse_move)
        self.canvas.bind("<B1-Motion>", self.handle_mouse_move)

        # Start animation loop
        self.animate()

    # --- Control Handlers ---
    def start_game(self):
        self.running = True

    def pause_game(self):
        self.running = False

    def reset_game(self):
        self.running = False
        self.score = 0
        self.star_speed = 4
        self.canvas.coords(self.paddle, 210, 360, 290, 375)
        self.canvas.coords(self.paddle_stripe, 215, 367, 285, 367)
        self.reset_star()
        self.update_status()

    def reset_star(self):
        x = random.randint(20, 460)
        self.canvas.coords(self.star, x, 10, x + 20, 30)

    # --- Keyboard & Mouse Handlers ---
    def handle_move_left(self, event):
        self.move_player(-self.paddle_speed)

    def handle_move_right(self, event):
        self.move_player(self.paddle_speed)

    def handle_speed_up(self, event):
        if self.star_speed < 15:
            self.star_speed += 1

    def handle_speed_down(self, event):
        if self.star_speed > 2:
            self.star_speed -= 1

    def handle_mouse_move(self, event):
        # Move tagged "player" group directly to mouse X coordinate
        coords = self.canvas.coords(self.paddle)
        current_center = (coords[0] + coords[2]) / 2
        dx = event.x - current_center
        self.move_player(dx)

    def move_player(self, dx):
        coords = self.canvas.coords(self.paddle)
        # Boundary detection for left and right walls
        if coords[0] + dx < 0:
            dx = -coords[0]
        elif coords[2] + dx > 500:
            dx = 500 - coords[2]

        # Move both paddle and stripe together using their shared tag
        self.canvas.move("player", dx, 0)
        self.update_status()

    def update_status(self):
        coords = self.canvas.coords(self.paddle)
        self.status_label.config(
            text=f"Score: {self.score} | Paddle X: {int(coords[0])} | Speed: {self.star_speed}"
        )

    # --- Animation Loop using after() ---
    def animate(self):
        if self.running:
            self.canvas.move(self.star, 0, self.star_speed)
            s_coords = self.canvas.coords(self.star)
            p_coords = self.canvas.coords(self.paddle)

            # Check collision with paddle
            if (
                s_coords[2] >= p_coords[0]
                and s_coords[0] <= p_coords[2]
                and s_coords[3] >= p_coords[1]
                and s_coords[1] <= p_coords[3]
            ):
                self.score += 1
                self.reset_star()
                self.update_status()

            # Boundary detection for bottom of canvas
            elif s_coords[3] >= 400:
                self.reset_star()

        self.root.after(30, self.animate)


if __name__ == "__main__":
    root = tk.Tk()
    app = MiniCatchGame(root)
    root.mainloop()