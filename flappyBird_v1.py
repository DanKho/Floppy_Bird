# flappyBird_v1.py
# Creator - Danila Khomenko
# Date: 15/04/2020
# TODO: remove unnecessary comments
# TODO: make the bird edges round to increase precision of collision detection
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
    # Private variable to store the file path for the player image
    _PLAYER_IMAGE_FILE = "sprites/bird.png"
    # Private attribute to store the maximum downward falling speed of the player
    _GRAVITY_Y_SPEED = 3
    # Private attribute to store the maximum upward jump speed of the player (directly proportional to the jump height)
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
        # Tkinter private image attribute to store the player sprite
        self._player_sprite = tk.PhotoImage(file=self._PLAYER_IMAGE_FILE)
        # Initialize player object (bird) from the canvas class and store it in a private attribute self._player
        self._player = self._canvas.create_image(self._window_width / 2, self._window_height / 2,
                                                 image=self._player_sprite, anchor="c", tag="player")
        # Private attribute to store the player's current vertical (y) speed
        self._y_speed = self._GRAVITY_Y_SPEED

    def player_fall(self):
        """
        Public method which makes the player move downward (fall)
        """
        # If the player hits the upper window boundary, make it bounce back down
        if self.get_player_coords()[1] < 20:
            self._y_speed = self._GRAVITY_Y_SPEED
        # Make the payer move downward (fall)
        self._canvas.move(self._player, 0, self._y_speed)
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
        return self._canvas.coords(self._player)


class Pipe:
    """
    This class is responsible for creating the pipe objects on the main canvas window
    and managing their motion (moving sideways)
    """
    # Private attribute to store an integer-type variable for the width constant for each pipe
    _PIPE_WIDTH = 85
    # Private attribute to store an integer-type variable for the vertical separation constant for each pipe
    _PIPE_SEPARATION_Y = 120  # 160
    # Private attribute to store a float-type variable for the maximum horizontal speed constant for each pipe
    _MAX_X_SPEED = -2.6  # -2
    # Private attribute to store an integer-type variable for the spawn x-coordinate for each pipe
    _SPAWN_X = 487
    # Private variable to store a float-type variable for the frequency of generation of each pipe
    _PIPE_SPAWN_INTERVAL = 1.5  # 2.5
    # Private variable to store a string-type for the color of each pipe
    _PIPE_COLOR = "lime green"

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

        # Private variable to store the bottom pipe widget
        self._pipe_bottom = None
        # Private variable to store the top pipe widget
        self._pipe_top = None
        # Private integer-type variable to store the coordinate of the spawn origin of each pipe
        self._origin_x = self._SPAWN_X
        # Private boolean-type variable to indicate whenever a new pipe is drawn to allow for time-regulated generation
        self._pipe_drawn = False
        # Private integer-type variable to store a constant for the horizontal speed of each pipe
        self._x_speed = self._MAX_X_SPEED

    def pipe_generator(self):
        """
        This public method controls the initialisation process of new pipe objects at pre-defined
        time intervals (calls the pipe generator method when appropriate)
        """
        # Private float-type variable to store the time elapse since the start of the game instance
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
                                                          fill=self._PIPE_COLOR, tags=("pipe", "bottom_pipe"))
        # Initialize top pipe object as a rectangle from the canvas class and store it in a private attribute
        self._pipe_top = self._canvas.create_rectangle(self._origin_x, 0, self._origin_x + self._PIPE_WIDTH,
                                                       _pipe2_len_from_top, fill=self._PIPE_COLOR,
                                                       tags=("pipe", "top_pipe"))

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
    # Private variable to store the file path for the game background image
    _BACKGROUND_IMAGE_FILE = "sprites/background.png"

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

        # Tkinter private image attribute to store the game background PhotoImage
        self._background_image = tk.PhotoImage(file=self._BACKGROUND_IMAGE_FILE)
        # Initialize the background image widget from the canvas class
        self._canvas.create_image(self._width / 2, self._height / 2,
                                  image=self._background_image, anchor="c", tag="background")

        # Private variable to store an instance of the Bird class (player)
        self._player = None

        # Initialise an instance of the Pipe class and store in a private variable _pipe
        self._pipe = Pipe(self.root, self._canvas, self._width, self._height)
        # Private variable to store the id of the last pipe pair (bottom pipe) that the user has passed through
        self._scored_pipe = None

        # Binding input from a user (keypress) to a private method _user_input_handler
        self._canvas.bind("<KeyPress>", self._user_input_handler)
        # Binding input from a user (mouse click) to a private method _user_input_handler
        self._canvas.bind("<Button>", self._user_input_handler)
        # Setting keyboard focus to the main canvas window
        self._canvas.focus_set()

        # Private integer-type variable to store the user's best scores
        self._best_score = 0
        # Private integer-type variable to store the user's current score (within a single game session)
        self._player_score = 0
        # Private variable to store the score counter widget
        self._score_counter_text = None

        # Center the Tkinter root window on the user's screen
        self.root.eval('tk::PlaceWindow . center')
        # Disallow the user from re-sizing the game window
        self.root.resizable(False, False)

        # Call to the initialisation of the game
        self._start()

        self.root.mainloop()

    def _intro_menu(self):
        """
        This private method generates the main user menu containing the start button and an instructions page
        """
        # Create a canvas rectangle widget to serve as the main menu's background
        self._canvas.create_rectangle(self._width / 2 - 110, self._height / 2 - 140, self._width / 2 + 110,
                                      self._height / 2 + 15, fill="yellow", tag="menu_window")
        # Create a canvas text widget which stores the game title
        self._canvas.create_text(self._width / 2, self._height / 2 - 112, text="FloppyBird_v1", fill="black",
                                 font=("ROBOTO", 12, "bold"), justify="center", tag="intro_menu_widget")
        # Create a canvas text widget which stores the game author
        self._canvas.create_text(self._width / 2, self._height / 2 - 90, text="Author: Danila Khomenko", fill="black",
                                 font=("ROBOTO", 11), justify="center", tag="intro_menu_widget")
        # Create a canvas button widget to act as the main menu's "start" button
        _button_start_game = tk.Button(self._canvas, text="Start", anchor='c', font=("ROBOTO", 12, "bold"),
                                       command=self._initialise_game_layout)
        _button_start_game.configure(width=10, background="orange")
        # Create a canvas window widget to host the "start" button
        self._canvas.create_window(self._width / 2, self._height / 2 - 14, window=_button_start_game,
                                   tag="start_button")
        # Create a canvas button widget to act as the main menu's "instructions" button
        _button_game_instructions = tk.Button(self._canvas, text="Instructions", anchor='c',
                                              font=("ROBOTO", 12, "bold"),
                                              command=self._instructions_screen)
        _button_game_instructions.configure(width=10, background="orange")
        # Create a canvas window widget to host the "restart" button
        self._canvas.create_window(self._width / 2, self._height / 2 - 52, window=_button_game_instructions,
                                   tag="intro_menu_widget")

    def _instructions_screen(self):
        """
        This private method presents the user with the game instructions
        """
        # Game instructions text
        _instructions = "Use <space>, <Button-1> \nor <Up-arrow> to make the \nbird jump. " \
                        "Fly the bird as \nfar as you can without \nhitting a pipe."
        # Remove any widgets related to the main menu
        self._canvas.delete("intro_menu_widget")
        # Create a canvas text widget which stores the instructions text
        self._canvas.create_text(self._width / 2, self._height / 2 - 85, text=_instructions, fill="black",
                                 font=("ROBOTO", 12), justify="center", tag="instructions_menu_widget")

    def _user_input_handler(self, event):
        """
        This private method processes all input supplied by the user (excluding menu buttons) such as keyboard or mouse
        events
        :param event: information about the user event
        :return: None
        """
        # This private variable stores the name of the key pressed by the user
        _key_press = event.keysym
        # This private variable stores the name of the mouse button pressed by the user
        _button_press = event.num
        if _key_press in ("space", "Up") or _button_press == 1:
            # If a new game has just een started, treat the user input as a call to start a new game process
            if self._NEW_GAME:
                self._NEW_GAME = False
                # Set the keyboard focus on the canvas window
                self._canvas.focus_set()
                self._player.player_jump()
                # Initiate the game flow
                self._main()

            # If a game session has ended, treat the user input as a call to start a new game session (restart)
            elif self._GAME_OVER and _button_press != 1 and _key_press == "space":
                self._restart_game()

            # If a game session is currently running, treat the user input as calls for in-game mechanics (jumping)
            else:
                # If the player exists, make it jump up
                if self._player:
                    self._player.player_jump()

    def _initialise_game_layout(self):
        """
        This function initialises the main game layout before each game session
        """
        # Remove all widgets present on the canvas
        self._canvas.delete("all")
        self._canvas.create_image(self._width / 2, self._height / 2,
                                  image=self._background_image, anchor="c", tag="background")
        # Initialise an instance of the Bird class and store in a private variable _player
        self._player = Bird(self.root, self._canvas, self._width, self._height)
        # Indicate that a new game session has been initiated
        self._NEW_GAME = True

    def _overlap_detection(self):
        """
        This private method detects when a collision or an overlap occurs within the game between the player
        and other specified widgets
        :return: a boolean indicating whether a collision has occurred between the player and a pipe object or the floor
        """
        # A private tuple containing IDs of canvas widgets under the "pipe" tag present on the screen
        _pipe_objects = self._canvas.find_withtag("pipe")
        # A private list containing the coordinates of the player (bird) on the canvas
        _player_coords = self._player.get_player_coords()
        # A private int-type variable containing the x coordinate of the player on the canvas
        _player_x = _player_coords[0]
        # A private int-type variable containing the y coordinate of the player on the canvas
        _player_y = _player_coords[1]
        # A tuple containing the IDs of canvas widgets that overlap with the player (bird) widget
        _overlapping_objects = self._canvas.find_overlapping(_player_x - 18, _player_y - 18, _player_x + 22,
                                                             _player_y + 20)

        for pipe in _pipe_objects:
            # Remove pipes that have left the canvas window to maximise performance
            if self._canvas.coords(pipe)[2] < 0:
                self._canvas.delete(pipe)
            # Check whether the chosen pipe object is a bottom pipe
            if "bottom_pipe" in self._canvas.gettags(pipe):
                # Check if the player has flown above the specified pipe without colliding with it (through the gap)
                if self._canvas.coords(pipe)[0] < _player_x:
                    # Check that the player hasn't yet been scored for passing through the given pipe pair
                    if pipe != self._scored_pipe:
                        # If not, assign the given pipe to _scored_pipe
                        self._scored_pipe = pipe
                        # Give the player 1 point and update the score board
                        self._player_score += 1
                        self._update_score()
            # If, however, the player has physically collided with the given pipe or the floor, return True
            if pipe in _overlapping_objects:
                # Indicates a collision between the bird and a pipe, so a game over call should be made
                return True
        # Indicates that a collision between the bird and the ground, so a game over call should be made
        if self._player.get_player_coords()[1] > self._height - 31:
            return True
        else:
            # Return False to indicate that no collision had occurred
            return False

    def _update_score(self):
        """
        This private method updates the game score text every time the user scores
        """
        # Clear the scoring board (if exists)
        self._canvas.delete("score_counter")
        # Initialize a new game score counter widget and store it in the private attribute _score_counter_text
        self._score_counter_text = self._canvas.create_text(self._width / 2, 120, text="{}".format(self._player_score),
                                                            fill="white", font=("Arial", 50), justify="center",
                                                            tag="score_counter")

    def _game_over_menu(self):
        """
        This private method generates the "game over" menu with the user's end scores
        """
        self._GAME_OVER = True
        self._canvas.delete("score_counter")
        # Check whether the user had reached a new high score
        if self._player_score > self._best_score:
            # If so, set the new high score
            self._best_score = self._player_score
        # Create a canvas rectangle widget to serve as the menu's background
        self._canvas.create_rectangle(self._width / 2 - 50, self._height / 2 - 135, self._width / 2 + 50,
                                      self._height / 2 + 10, fill="yellow", tag="game_over_t")
        # Create a canvas text widget to store and display the word "Score"
        self._canvas.create_text(self._width / 2, self._height / 2 - 110, text="Score", fill="black",
                                 font=("Arial", 20), justify="center", tag="game_over_t")
        # Create a canvas text widget to store and display the user's current score
        self._canvas.create_text(self._width / 2, self._height / 2 - 80, text=f"{self._player_score}", fill="red",
                                 font=("Arial", 20), justify="center", tag="game_over_t")
        # Create a canvas text widget to store and display the word "Best score"
        self._canvas.create_text(self._width / 2, self._height / 2 - 45, text="Best", fill="black",
                                 font=("Arial", 20), justify="center", tag="game_over_t")
        # Create a canvas text widget to store and display the user's best score
        self._canvas.create_text(self._width / 2, self._height / 2 - 15, text=f"{self._best_score}", fill="red",
                                 font=("Arial", 20), justify="center", tag="game_over_t")
        # Create a canvas button widget to act as the "restart" button
        button_restart = tk.Button(self._canvas, text="Restart", anchor='c', font=("ROBOTO", 12, "bold"),
                                   command=self._restart_game)
        button_restart.configure(width=20, background="orange")
        # Create a canvas window widget to host the "restart" button
        self._canvas.create_window(self._width / 2, self._height / 2 + 50, window=button_restart, tag="game_over_t")

    def _restart_game(self):
        """
        This private method clears the main canvas window and restarts the game
        """
        self._canvas.delete("all")
        self._GAME_OVER = False
        self._player_score = 0
        self._NEW_GAME = False
        self._initialise_game_layout()

    def _start(self):
        """
        This private method acts as a trigger to initiate a new game process
        """
        self._intro_menu()

    def _main(self):
        """
        This function carries out the primary game flow (logic within a single game session)
        """
        # Raise the score text widget above the pipe widgets (if exists)
        if self._score_counter_text:
            self._canvas.tag_raise(self._score_counter_text)
        # Generate a new pipe pair on the screen if appropriate
        self._pipe.pipe_generator()
        # Check the game window for collisions or overlaps between the existing widgets
        collision = self._overlap_detection()
        # Make the player more downward (fall due to gravity)
        self._player.player_fall()
        # Move the pipe objects towards the player
        self._pipe.move_pipe()
        # If no collision has been detected, repeat the process
        if not collision:
            self.root.after(15, self._main)
        # If the player has collided with a pipe or the floor, initiate "game over" scene (menu)
        else:
            self._game_over_menu()


MainApplication()
