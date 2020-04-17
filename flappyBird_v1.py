# flappyBird_v1.py
# Creator - Danila Khomenko
# Date: 15/04/2020
# TODO: remove unnecessary comments
# TODO: ask about boundary input cases
# ===================  IMPORTS  ===================+
import tkinter as tk
import random
import time


# ==================  CLASS CODE  ==================+
class Bird:
    """"
    This class is responsible for creating the player (bird) object on the main canvas window
    and managing its motion (jumping and falling)
    """
    # Public variable to store the file path for the player image
    _PLAYER_IMAGE_FILE = "sprites/bird.png"
    # Private variable to store the maximum downward falling speed of the player
    _GRAVITY_Y_SPEED = 3
    # Private variable to store the maximum upward jump speed of the player (directly proportional to the jump height)
    _JUMP_Y_SPEED = -5  # -5

    def __init__(self, root, canvas, window_width, window_height):
        """
        Constructor function of the Bird class
        :param root: the Tkinter root window
        :param canvas: the Tkinter canvas class
        :param window_width: width of the Canvas window
        :param window_height: height of the Canvas window
        """
        self._root = root
        self._canvas = canvas
        self._window_width = window_width
        self._window_height = window_height
        # Tkinter private image variable to store the player sprite
        self._player_sprite = tk.PhotoImage(file=self._PLAYER_IMAGE_FILE)
        # Initialize player object (bird) from the canvas class and store it in a public attribute self.player
        self.player = self._canvas.create_image(self._window_width / 2, self._window_height / 2,
                                                image=self._player_sprite, anchor="c", tag="player")
        # Private variable to store the player's current vertical (y) speed
        self._y_speed = self._GRAVITY_Y_SPEED

    def player_fall(self):
        """
        Public method which makes the player move downward (fall)
        """
        self._canvas.move(self.player, 0, self._y_speed)
        self._y_speed += 0.25  # 0.25

    def player_jump(self):
        """
        Public method which makes the player jump upward
        """
        self._y_speed = self._JUMP_Y_SPEED

    def get_player_coords(self):
        """
        Public method which returns the x and y coordinates of the player (bird) on the canvas
        """
        return self._canvas.coords(self.player)


class Pipe:
    """
    This class is responsible for creating the pipe objects on the main canvas window
    and managing their motion (moving sideways)
    """
    # Private variable to store an integer-type for the width constant for each pipe
    _PIPE_WIDTH = 85
    # Private variable to store an integer-type for the vertical separation constant for each pipe
    _PIPE_SEPARATION_Y = 120  # 160
    # Private variable to store a float-type for the maximum horizontal speed constant for each pipe
    _MAX_X_SPEED = -2.6  # -2
    # Private variable to store an integer-type spawn x-coordinate for each pipe
    _SPAWN_X = 487
    # Private variable to store a float-type  for the frequency of generation of each pipe
    _PIPE_SPAWN_INTERVAL = 2.0  # 2.5

    def __init__(self, root, canvas, window_width, window_height):
        """
        Constructor function of the Pipe class
        :param root: the Tkinter root window
        :param canvas: the Tkinter canvas class
        :param window_width: width of the Canvas window
        :param window_height: height of the Canvas window
        """
        self._root = root
        self._canvas = canvas
        self._window_width = window_width
        self._window_height = window_height

        # Private variable to store an instance of the bottom pipe object
        self._pipe_bottom = None
        # Private variable to store an instance of the top pipe object
        self._pipe_top = None
        # Private integer-type variable to store the coordinate of the spawn origin of each pipe
        self._origin_x = self._SPAWN_X
        # Private boolean-type variable to indicate whenever a new pipe is drawn to allow for time-regulated generation
        self._pipe_drawn = False
        # Private integer-type variable to store a constant for the horizontal speed of each pipe
        self._x_speed = self._MAX_X_SPEED

    def pipe_initialization_timer(self):
        """
        This public method controls the initialisation process of new pipe objects at pre-defined
        time intervals (calls the pipe generator method when appropriate)
        """
        # Private float-type variable
        _time_elapsed = round(time.time(), 1)
        # An if statement that checks the time elapsed since the last pipe object has been generated
        if _time_elapsed % self._PIPE_SPAWN_INTERVAL == 0:
            # If a new pipe hasn't been drawn after the interval, generate a new pipe
            if not self._pipe_drawn:
                self._draw_pipe_on_canvas()
                self._pipe_drawn = True
        # If the time interval since the last pipe generated is not met, set the _pipe_drawn attribute to False
        else:
            self._pipe_drawn = False

    def _draw_pipe_on_canvas(self):
        """
        This private method creates and draws new pipe objects on the canvas
        """
        # Private integer-type variable to store a randomly-generated height-from-top of the top pipe
        _pipe1_len_from_top = random.randrange(self._window_height - 460, self._window_height - 90)
        # Private integer-type variable to store the height-from-top for the bottom pipe derived from the previous var
        _pipe2_len_from_top = _pipe1_len_from_top - self._PIPE_SEPARATION_Y
        # Initialize bottom pipe object as a rectangle from the canvas class and store it in a private attribute
        self._pipe_bottom = self._canvas.create_rectangle(self._origin_x, _pipe1_len_from_top,
                                                          self._origin_x + self._PIPE_WIDTH, self._window_height + 5,
                                                          fill="green", tags=("pipe", "bottom_pipe"))
        # Initialize top pipe object as a rectangle from the canvas class and store it in a private attribute
        self._pipe_top = self._canvas.create_rectangle(self._origin_x, 0, self._origin_x + self._PIPE_WIDTH,
                                                       _pipe2_len_from_top, fill="green", tags=("pipe", "top_pipe"))

    def move_pipe(self):
        """
        Public method which makes both of the generated pipes (combined with a common tag)
        move horizontally with a pre-set speed
        """
        self._canvas.move("pipe", self._x_speed, 0)


class MainApplication:
    """
    This class containing that constructs the main game window, initializes widgets on the screen, and controls
    the main game logic (flow)
    """
    # Private boolean-type variable to indicate whether a new game process has been initiated
    _NEW_GAME = False
    # Private boolean-type variable to indicate whether the current game process has ended
    _GAME_OVER = False

    def __init__(self):
        """
        Constructor function of the MainApplication class
        """
        # Tkinter root window of the game
        self.root = tk.Tk()
        # Title of the game
        self.root.title("FlappyBird_v1")

        # Private integer-type variable to store the width of the game window
        self._width = 485
        # Private integer-type variable to store the height of the game window
        self._height = 640
        # Private string-type variable to store the color of the game window's background
        self._background_color = "#03adfc"

        # Create an instance of the tkinter Canvas widget
        self._canvas = tk.Canvas(self.root, width=self._width, height=self._height, background=self._background_color)
        # Place the canvas widget within the tkinter Root window
        self._canvas.grid(row=0, column=0)

        self._player = Bird(self.root, self._canvas, self._width, self._height)
        self._canvas.bind("<KeyPress>", self._user_input_handler)
        self._canvas.bind("<Button>", self._user_input_handler)
        self._canvas.focus_set()

        self._best_score = 0
        self._player_score = 0
        self._score_counter_text = self._canvas.create_text(self._width / 2, 120, text="{}".format(self._player_score),
                                                            fill="white", font=("Arial", 50), justify="center",
                                                            tag="score_counter")

        self._canvas.itemconfigure(self._player.player, state='hidden')
        self._canvas.itemconfigure(self._score_counter_text, state='hidden')

        self._pipe = Pipe(self.root, self._canvas, self._width, self._height)
        self._scored_pipe = None

        self.root.eval('tk::PlaceWindow . center')
        self.root.resizable(False, False)

        self._start()

        self.root.mainloop()

    def _intro_screen(self):
        """
        Generate the main menu of the game
        """
        self._canvas.create_rectangle(self._width / 2 - 100, self._height / 2 - 135, self._width / 2 + 100,
                                      self._height / 2 + 10, fill="yellow", tag="menu_window")

        self._canvas.create_text(self._width / 2, self._height / 2 - 110, text="FlappyBird_v1", fill="black",
                                 font=("Arial", 12), justify="center", tag="intro_menu_widget")

        button_start_game = tk.Button(self._canvas, text="Start", anchor='c', font=("ROBOTO", 12, "bold"),
                                      command=self._initialise_game_layout)
        button_start_game.configure(width=10, background="orange")
        self._canvas.create_window(self._width / 2, self._height / 2 - 20, window=button_start_game, tag="start_button")
        button_game_instructions = tk.Button(self._canvas, text="Instructions", anchor='c', font=("ROBOTO", 12, "bold"),
                                             command=self._instructions_screen)
        button_game_instructions.configure(width=10, background="orange")
        self._canvas.create_window(self._width / 2, self._height / 2 - 65, window=button_game_instructions,
                                   tag="intro_menu_widget")

    def _instructions_screen(self):
        """
        Present the game instructions to the user
        """
        instructions = "Use <space> or <Button-1> \nto make the bird jump. " \
                       "\nFly the bird as far as you \ncan without hitting a pipe."
        self._canvas.delete("intro_menu_widget")
        self._canvas.create_text(self._width / 2, self._height / 2 - 85, text=instructions, fill="black",
                                 font=("Arial", 12), justify="center", tag="instructions_menu_widget")

    def _user_input_handler(self, event):
        """
        Do something when the user presses a key (keyboard event handler)
        """
        key_press = event.keysym
        button_press = event.num
        if key_press in ("space", "Up") or button_press == 1:
            if self._NEW_GAME:
                self._NEW_GAME = False
                self._canvas.focus_set()
                self._player.player_jump()
                self._main()

            elif self._GAME_OVER and button_press != 1:
                self._restart_game()

            else:
                if self._player.get_player_coords()[1] > 35:
                    self._player.player_jump()

    def _initialise_game_layout(self):
        """
        This function initialises the main game layout before each game starts
        """
        self._canvas.delete("all")
        self._canvas.itemconfigure(self._score_counter_text, state='normal')
        self._canvas.itemconfigure(self._player.player, state='normal')
        self._player = Bird(self.root, self._canvas, self._width, self._height)
        self._NEW_GAME = True

    def _main(self):
        """
        This function carries out the game process
        """
        self._canvas.tag_raise(self._score_counter_text)
        collision = self._overlap_detection()
        self._pipe.pipe_initialization_timer()
        self._player.player_fall()
        self._pipe.move_pipe()
        if not collision:
            self.root.after(15, self._main)
        else:
            self._game_over_menu()

    def _overlap_detection(self):
        """
        Detect when a collision or overlap occurs within the game between the player and other specified objects
        """
        pipe_objects = self._canvas.find_withtag("pipe")
        player_coords = self._player.get_player_coords()
        player_x = player_coords[0]
        player_y = player_coords[1]
        # TODO: make the bird edges round to increase precision of collision detection
        overlapping_objects = self._canvas.find_overlapping(player_x - 20, player_y - 20, player_x + 24, player_y + 18)
        for pipe in pipe_objects:
            if self._canvas.coords(pipe)[2] < 0:
                self._canvas.delete(pipe)
            if "bottom_pipe" in self._canvas.gettags(pipe):
                if self._canvas.coords(pipe)[0] < player_x:
                    if pipe != self._scored_pipe:
                        self._scored_pipe = pipe
                        self._player_score += 1
                        self._update_score()
            # Utilising player_x would be more efficient, but requesting for a new set of coordinates is a necessity
            if pipe in overlapping_objects or self._player.get_player_coords()[1] > self._height - 28:
                return True
        return False

    def _update_score(self):
        """
        This function updates the main game score when the player scores a point
        """
        self._canvas.delete("score_counter")
        self._score_counter_text = self._canvas.create_text(self._width / 2, 120, text="{}".format(self._player_score),
                                                            fill="white", font=("Arial", 50), justify="center",
                                                            tag="score_counter")

    def _game_over_menu(self):
        """
        Generate the "game over" menu
        """
        self._GAME_OVER = True
        self._canvas.delete("score_counter")
        if self._player_score > self._best_score:
            self._best_score = self._player_score
        # Menu window
        self._canvas.create_rectangle(self._width / 2 - 50, self._height / 2 - 135, self._width / 2 + 50,
                                      self._height / 2 + 10, fill="yellow", tag="game_over_t")
        # Score text
        self._canvas.create_text(self._width / 2, self._height / 2 - 110, text="Score", fill="black",
                                 font=("Arial", 20), justify="center", tag="game_over_t")
        # Score number
        self._canvas.create_text(self._width / 2, self._height / 2 - 80, text=f"{self._player_score}", fill="red",
                                 font=("Arial", 20), justify="center", tag="game_over_t")
        # Best score text
        self._canvas.create_text(self._width / 2, self._height / 2 - 45, text="Best", fill="black",
                                 font=("Arial", 20), justify="center", tag="game_over_t")
        # Best score number
        self._canvas.create_text(self._width / 2, self._height / 2 - 15, text=f"{self._best_score}", fill="red",
                                 font=("Arial", 20), justify="center", tag="game_over_t")
        button_restart = tk.Button(self._canvas, text="Restart", anchor='c', font=("ROBOTO", 12, "bold"),
                                   command=self._restart_game)
        button_restart.configure(width=20, background="orange")
        # Button background window
        self._canvas.create_window(self._width / 2, self._height / 2 + 50, window=button_restart, tag="game_over_t")

    def _restart_game(self):
        """
        This function clears the main canvas window and restarts the game
        """
        self._canvas.delete("all")
        self._GAME_OVER = False
        self._player_score = 0
        self._NEW_GAME = False
        self._initialise_game_layout()

    def _start(self):
        """
        Start the game process
        """
        self._intro_screen()


MainApplication()
