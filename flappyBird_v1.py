# flappyBird_v1.py
# Creator - Danila Khomenko
# Date: 15/04/2020
# TODO: remove unnecessary comments
# ===================  IMPORTS  ===================+
import tkinter as tk
import random
import time

_BACKGROUND_IMAGE_FILE = "/Users/evgeniyk/cloned/learning/Flappy_Bird/Sprites/background.gif"

# ==================  CLASS CODE  ==================+
class MainApplication:
    """
    This class is orchestrating game behaviour.
    """
    def __init__(self):
        # Create Game Menu Manager
        self.menu_manager = MenuManager()
        # Launch the menu
        self.menu_manager.show_main_menu()


class GameWindow:
    """
    This class is used to create the basic game Window with Canvas
    """
    _GAME_TITLE = "Flappy Bird"
    _WINDOW_WIDTH = 485
    _WINDOW_HEIGHT = 640
    _BKG_COLOR = "#03adfc"

    def __init__(self):
        """
        Constructor of the new Game Window.
        """
        # Tkinter root window of the game
        self.root_window = tk.Tk()

        # Window Dimensions
        self.width = self._WINDOW_WIDTH
        self.height = self._WINDOW_HEIGHT

        # Configure Window Background 
        self.bkg_color =  self._BKG_COLOR
        self.bkg_image = tk.PhotoImage(file = _BACKGROUND_IMAGE_FILE)

        self._configure_window()
        self.canvas = self.create_canvas()

    def _configure_window(self):
        """
        Creates game root window
        """
        # Center the Tkinter root window on the user's screen
        self.root_window.eval('tk::PlaceWindow . center')
        # Disallow the user from re-sizing the game window
        self.root_window.resizable(False, False)
        # Set window title
        self.root_window.title(self._GAME_TITLE)

    def create_canvas(self):
        """
        Creates and configures Canvas
        """
        canvas = tk.Canvas(
            self.root_window, 
            width = self.width, 
            height = self.height, 
            background=self.bkg_color)
        # Place the canvas widget within the tkinter Root window
        canvas.grid(row=0, column=0)
        # Initialize the background image widget from the canvas class
        canvas.create_image(
            self.get_window_center_coordinates()[0], 
            self.get_window_center_coordinates()[1],
            image=self.bkg_image, 
            anchor="c", tag="background")
        return canvas

    def get_window_center_coordinates(self):
        """
        Returns (x,y) coordinates tuple of the root window centre. 
        """
        x = self.width / 2
        y = self.height / 2
        return (x, y)

    def get_root_window(self):
        """
        Returns the root window.
        """
        return self.root_window


class MenuManager:
    _GAME_TITLE                 = "Flappy Bird"
    _INSTRUCTIONS_BUTTON_TITLE  = "Instructions"
    _START_BUTTON_TITLE         = "Start"
    _INSTRUCTIONS               = "Use <space>, <Button-1> \nor <Up-arrow> to make the \nbird jump. " \
                                  "Fly the bird as \nfar as you can without \nhitting a pipe."
    _SCORE_TITLE                = "Score"
    _BEST_TITLE                 = "Best"
    _RESTART_TITLE              = "Restart"
    """
    This class generates the main user menu containing the start button and an instructions page.
    """
    def __init__(self):
        # Create Main Window
        self.window = GameWindow()
        
        # Set Window configs
        self.canvas = self.window.canvas
        
        # Set Window centre coordinates
        self.window_center_x = self.window.get_window_center_coordinates()[0]
        self.window_center_y = self.window.get_window_center_coordinates()[1]

        # Create GameFlowManager
        self.game_flow_manager = GameFlowManager(window=self.window)

    def show_main_menu(self):
        """
        Creates the main menu with intro details, `Instructions` and `Start` buttons. 
        """
        # Create a canvas rectangle widget to serve as the main menu's background
        self.canvas.create_rectangle(
            self.window_center_x-110, 
            self.window_center_y-140,
            self.window_center_x+110, 
            self.window_center_y+15, 
            fill="yellow",
            tag="menu_window")
        # Create a canvas text widget which stores the game Title
        self.canvas.create_text(
            self.window_center_x, 
            self.window_center_y - 112, 
            text=self._GAME_TITLE, 
            fill="black",
            font=("ROBOTO", 12, "bold"), 
            justify="center", 
            tag="intro_menu_widget")
        # Create a canvas text widget which stores the game Author
        self.canvas.create_text(
            self.window_center_x, 
            self.window_center_y - 90, 
            text="Author: Danila Khomenko",
            fill="black", 
            font=("ROBOTO", 11),
            justify="center",
            tag="intro_menu_widget")
        # Create a canvas button widget to act as the main menu's "Start" button
        button_start_game = tk.Button(
            self.canvas, 
            text=self._START_BUTTON_TITLE,
            anchor='c', 
            font=("ROBOTO", 12, "bold"),
            command=self.game_start)
        button_start_game.configure(
            width=10, 
            background="orange")
        # Create a canvas window widget to host the "Start" button
        self.canvas.create_window(
            self.window_center_x, 
            self.window_center_y - 14, 
            window=button_start_game,
            tag="start_button")
        # Create a canvas button widget to act as the main menu's "instructions" button
        button_game_instructions = tk.Button(
            self.canvas, 
            text=self._INSTRUCTIONS_BUTTON_TITLE, 
            anchor='c',
            font=("ROBOTO", 12, "bold"),
            command=self.open_instructions_screen)
        button_game_instructions.configure(
            width=10,
            background="orange")
        # Create a canvas window widget to host the "restart" button
        self.canvas.create_window(
            self.window_center_x,
            self.window_center_y - 52,
            window=button_game_instructions,
            tag="intro_menu_widget")
        self.window.root_window.mainloop()

    def open_instructions_screen(self):
        """
        Displays Game Instructions to the user.
        """
        # Remove any widgets related to the main menu
        self.canvas.delete("intro_menu_widget")
        # Create a canvas text widget which stores the instructions text
        self.canvas.create_text(
            self.window_center_x, 
            self.window_center_y - 85, 
            text=self._INSTRUCTIONS, 
            fill="black",
            font=("ROBOTO", 12), 
            justify="center", 
            tag="instructions_menu_widget")

    def game_start(self):
        self.game_flow_manager.start()

    def show_game_over_menu(self, score, best_score):
        """
        Creates the "Game Over" menu with the user's end scores
        """
        # Remove score counter
        self.canvas.delete("score_counter")
        # Update best score if it was beaten
        if score > best_score:
            best_score = score
        # Create a canvas rectangle widget to serve as the menu's background
        self.canvas.create_rectangle(
            self.window_center_x - 50,
            self.window_center_y - 135,
            self.window_center_x + 50,
            self.window_center_y + 10,
            fill="yellow", 
            tag="game_over_t")
        # Create a canvas text widget to store and display the word "Score"
        self.canvas.create_text(
            self.window_center_x,
            self.window_center_y - 110,
            text=_SCORE_TITLE,
            fill="black",
            font=("Arial", 20),
            justify="center",
            tag="game_over_t")
        # Create a canvas text widget to store and display the user's current score
        self.canvas.create_text(
            self.window_center_x,
            self.window_center_y - 80,
            text=str(score),
            fill="red",
            font=("Arial", 20),
            justify="center",
            tag="game_over_t")
        # Create a canvas text widget to store and display the word "Best score"
        self.canvas.create_text(
            self.window_center_x,
            self.window_center_y - 45,
            text=_BEST_TITLE,
            fill="black",
            font=("Arial", 20),
            justify="center",
            tag="game_over_t")
        # Create a canvas text widget to store and display the user's best score
        self.canvas.create_text(
            self.window_center_x,
            self.window_center_y - 15,
            text=str(best_score),
            fill="red",
            font=("Arial", 20),
            justify="center",
            tag="game_over_t")
        # Create a canvas button widget to act as the "restart" button
        button_restart = tk.Button(
            self.canvas,
            text=_RESTART_TITLE,
            anchor='c',
            font=("ROBOTO", 12, "bold"),
            command= self.game_start)
        button_restart.configure(width=20, background="orange")
        # Create a canvas window widget to host the "restart" button
        self.canvas.create_window(
            self.window_center_x,
            self.window_center_y + 50,
            window=button_restart,
            tag="game_over_t")


class GameFlowManager:
    """
    This class is managing the game flow.
    """
    def __init__(self, window):
        self.window=window
        # Set Window configs
        self.canvas = self.window.canvas
        # Set Window centre coordinates
        self.window_center_x = self.window.get_window_center_coordinates()[0]
        self.window_center_y = self.window.get_window_center_coordinates()[1]

        # Variable to store an instance of the Bird class (player)
        self.bird = None
        self.pipe = None
        self.scores = Scores()
        # Private boolean-type variable to indicate whether a new game process has been initiated
        self._NEW_GAME = False
        # Private boolean-type variable to indicate whether the current game process has ended
        _GAME_OVER = False

    def start(self):
        self._initialise_game_layout()
        self._create_bird()
        self._setup_event_handlers()

    def _restart_game(self):
        """
        This private method clears the main canvas window and restarts the game
        """
        self.canvas.delete("all")
        self._GAME_OVER = False
        self.scores.player_score = 0
        self._NEW_GAME = False
        self.start()

    def _main(self):
        """
        This function carries out the primary game flow (logic within a single game session)
        """
        # Raise the score text widget above the pipe widgets (if exists)
        # if self._score_counter_text:
        #     self.canvas.tag_raise(self._score_counter_text)

        # Generate a new pipe pair on the screen if appropriate
        self.pipe.pipe_generator()

        # Check the game window for collisions or overlaps between the existing widgets
        # collision = self._overlap_detection()

        # Make the bird move downward (fall due to gravity)
        self.bird.bird_fall()

        # Move the pipe objects towards the bird
        self.pipe.move_pipe()

        # If no collision has been detected, repeat the process
        # if not collision:
        #     self.root.after(15, self._main)

        # If the bird has collided with a pipe or the floor, initiate "game over" scene (menu)
        # else:
        #     self._game_over_menu()

    def _initialise_game_layout(self):
        """
        Initialises the main game layout before each game session
        """
        # Remove all widgets present on the canvas
        self.canvas.delete("all")
        self.canvas.create_image(
            self.window_center_x,
            self.window_center_y,
            image=self.window.bkg_image,
            anchor="c", 
            tag="background")

    def _create_bird(self):
        """ 
        Initialise an instance of the Bird class
        """
        self.bird = Bird(window=self.window)
        # Indicate that a new game session has been initiated
        self._NEW_GAME = True

    def _create_pipe(self):
        self.pipe = Pipe(self.window)

    def _setup_event_handlers(self):
         # Binding input from a user (keypress) to a private method _user_input_handler
        self.canvas.bind("<KeyPress>", self._user_input_handler)
        # Binding input from a user (mouse click) to a private method _user_input_handler
        self.canvas.bind("<Button>", self._user_input_handler)
        # Setting keyboard focus to the main canvas window
        self.canvas.focus_set()

    def _user_input_handler(self, event):
        """
        This private method processes all input supplied by the user (excluding menu buttons) such as keyboard or mouse
        events
        :param event: information about the user event
        :return: None
        """
        # This private variable stores the name of the key pressed by the user
        key_press = event.keysym
        # This private variable stores the name of the mouse button pressed by the user
        button_press = event.num
        if key_press in ("space", "Up") or button_press == 1:
            # If a new game has just been started, treat the user input as a call to start a new game process
            if self._NEW_GAME:
                self._NEW_GAME = False
                # Set the keyboard focus on the canvas window
                self.canvas.focus_set()
                self.bird.bird_jump()
                # Initiate the game flow
                self._main()


class Bird:
    """"
    This class is responsible for creating the player (bird) object on the main canvas window
    and managing its motion (jumping and falling). 
    """
    # Private variable to store the file path for the bird image
    _BIRD_IMAGE_FILE = "/Users/evgeniyk/cloned/learning/Flappy_Bird/Sprites/bird.gif"
    # Private attribute to store the maximum downward falling speed of the bird
    _GRAVITY_Y_SPEED = 3
    # Private attribute to store the maximum upward jump speed of the bird (directly proportional to the jump height)
    _JUMP_Y_SPEED = -5
    # Private attribute to store the y-coordinate of the upper window boundary which the bird must not cross
    _UPPER_WINDOW_BOUNDARY = 20
    # Private attribute to store the deceleration speed, which visually simulates the weight of the bird
    _DOWNWARD_ACCELERATION = 0.25

    def __init__(self, window):
        """
        Constructor function of the Bird class
        :param window: the Tkinter root window
        :param canvas: the Tkinter canvas class
        :param window_width: width of the Canvas window
        :param window_height: height of the Canvas window
        """
        self.window = window

        # Set Window configs
        self.canvas = self.window.canvas

        self.window_width = window.width
        self.window_height = window.height
        
        # Set Window centre coordinates
        self.window_center_x = self.window.get_window_center_coordinates()[0]
        self.window_center_y = self.window.get_window_center_coordinates()[1]
        
        # Tkinter private image attribute to store the bird sprite
        self.bird_sprite = tk.PhotoImage(file=self._BIRD_IMAGE_FILE)
        
        # Initialize bird object (bird) from the canvas class and store it in a private attribute self._player
        self.bird = self.canvas.create_image(
            self.window_center_x, 
            self.window_center_y,
            image=self.bird_sprite, 
            anchor="c", 
            tag="bird")
        # Private attribute to store the bird's current vertical (y) speed
        self._y_speed = self._GRAVITY_Y_SPEED
        # Private attribute to store the bird's current horizontal (x) speed
        self._x_speed = 0


    def bird_fall(self):
        """
        Public method which makes the bird move downward (fall)
        """
        # If the bird hits the upper window boundary, make it bounce back down (the index of 1 indicates the y-coord)
        if self.get_bird_x_y_coords()[1] < self._UPPER_WINDOW_BOUNDARY:
            self._y_speed = self._GRAVITY_Y_SPEED
        # Make the payer move downward (fall)
        self.canvas.move(self.bird, self._x_speed, self._y_speed)
        self._y_speed += self._DOWNWARD_ACCELERATION

    def bird_jump(self):
        """
        Public method which makes the bird jump upward
        """
        self._y_speed = self._JUMP_Y_SPEED

    def get_bird_x_y_coords(self):
        """
        Public method which returns the x and y coordinates of the player (bird) on the canvas
        """
        return self.canvas.coords(self.bird)


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
    # Private variable to store a float-type variable for the frequency of generation of each pipe
    _PIPE_SPAWN_INTERVAL = 2.5  # only n-0.5 (where n = Whole num) i.e. 1.5; 2.5; 3.5
    # Private int-type variable for the maximum offset distance from the top and bottom window boundaries
    _PIPE_Y_OFFSET = 90
    # Private variable to store a string-type for the color of each pipe
    _PIPE_COLOR = "lime green"

    def __init__(self, window):
        """
        Constructor function of the Pipe class
        :param window: the Tkinter window
        """
        self.window = window

        # Set Window configs
        self.canvas = self.window.canvas

        self._window_width = window.width
        self._window_height = window.height

        # Private variable to store the bottom pipe widget
        self._pipe_bottom = None
        # Private variable to store the top pipe widget
        self._pipe_top = None
        # Private integer-type variable to store the x-coordinate of the spawn origin of each pipe
        self._origin_x = self._window_width
        # Private integer-type variable to store the y-coordinate of the spawn origin of each upper pipe
        self.top_pipe_origin_y = 0
        # Private boolean-type variable to indicate whenever a new pipe is drawn to allow for time-regulated generation
        self._pipe_drawn = False
        # Private integer-type variable to store a constant for the horizontal speed of each pipe
        self._x_speed = self._MAX_X_SPEED
        # Private integer-type variable to store a constant for the vertical speed of each pipe
        self._y_speed = 0
        # Private integer-type variable to store a constant the number of dp that the game run-time is rounded to
        self._pipe_generator_time_dp = 1
        # Private integer-type variable to store a derived constant for the smallest length of a pipe from the top
        self._min_length_from_top = self._PIPE_Y_OFFSET
        # Private integer-type variable to store a derived constant for the biggest length of a pipe from the top
        self._max_length_from_top = self._window_height - self._PIPE_Y_OFFSET - self._PIPE_SEPARATION_Y

    def pipe_generator(self):
        """
        This public method controls the initialisation process of new pipe objects at pre-defined
        time intervals (calls the pipe generator method when appropriate)
        """
        # Private float-type variable to store the time elapse since the start of the game instance
        time_elapsed = round(time.time(), self._pipe_generator_time_dp)
        """
        An if statement that checks if the time elapsed since the last pipe creation divided by the value of the set
        generation interval leaves no remained (output is 0), which implies that the pipe spawn time interval has 
        passed and a new pipe should be spawned
        """
        if time_elapsed % self._PIPE_SPAWN_INTERVAL == 0:
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
        top_pipe_len_from_top = random.randrange(
            self._min_length_from_top, 
            self._max_length_from_top)
        # Private integer-type variable to store the height-from-top for the bottom pipe derived from the previous var
        bottom_pipe_len_from_top = top_pipe_len_from_top + self._PIPE_SEPARATION_Y
        # Initialize bottom pipe object as a rectangle from the canvas class and store it in a private attribute
        self._pipe_bottom = self._canvas.create_rectangle(
            self._origin_x, 
            bottom_pipe_len_from_top,
            self._origin_x + self._PIPE_WIDTH, 
            self._window_height,
            fill=self._PIPE_COLOR, 
            tags=("pipe", "bottom_pipe"))
        # Initialize top pipe object as a rectangle from the canvas class and store it in a private attribute
        self._pipe_top = self._canvas.create_rectangle(
            self._origin_x, 
            self.top_pipe_origin_y,
            self._origin_x + self._PIPE_WIDTH, top_pipe_len_from_top,
            fill=self._PIPE_COLOR, 
            tags=("pipe", "top_pipe"))

    def move_pipe(self):
        """
        Public method which makes both of the generated pipes (combined with a common tag)
        move horizontally with a pre-set speed
        """
        self.canvas.move("pipe", self._x_speed, self._y_speed)



class Scores:
    """
    This is a simple class to create and manage game score.
    """
    def __init__(self):
        self.best_score = 0
        self.player_score = 0
        self.score_counter = None


# class GameMenu:
#     """
#     This class is used to initialise the game menus.
#     """
#     def __init__(self, game_canvas):
#         self.root = tk.Tk()
#         self.canvas = canvas

#     def run_main_menu(self):
#         """
#         Method that generates the main user menu containing the start button and an instructions page.
#         """

#         # Create a canvas text widget which stores the game title
#         self.canvas.create_text(self.window_center_x, self.window_center_y - 112, text="FloppyBird_v1", fill="black",
#                                  font=("ROBOTO", 12, "bold"), justify="center", tag="intro_menu_widget")
#         # Create a canvas text widget which stores the game author
#         self.canvas.create_text(self.window_center_x, self.window_center_y - 90, text="Author: Danila Khomenko",
#                                  fill="black", font=("ROBOTO", 11), justify="center", tag="intro_menu_widget")
#         # Create a canvas button widget to act as the main menu's "start" button
#         button_start_game = tk.Button(self.canvas, text="Start", anchor='c', font=("ROBOTO", 12, "bold"),
#                                       command=self._initialise_game_layout)
#         button_start_game.configure(width=10, background="orange")
#         # Create a canvas window widget to host the "start" button
#         self.canvas.create_window(self.window_center_x, self.window_center_y - 14, window=button_start_game,
#                                    tag="start_button")
#         # Create a canvas button widget to act as the main menu's "instructions" button
#         button_game_instructions = tk.Button(self.canvas, text="Instructions", anchor='c',
#                                              font=("ROBOTO", 12, "bold"),
#                                              command=self._instructions_screen)
#         button_game_instructions.configure(width=10, background="orange")
#         # Create a canvas window widget to host the "restart" button
#         self.canvas.create_window(self.window_center_x, self.window_center_y - 52, window=button_game_instructions,
#                                    tag="intro_menu_widget")

#     def _get_menu_background(self):
#         """
#         Create a canvas rectangle widget to serve as the main menu's background
#         """
#         return self.canvas.create_rectangle(
#                 self.window_center_x-110, 
#                 self.window_center_y-140,
#                 self.window_center_x+110, 
#                 self.window_center_y+15, 
#                 fill="yellow",
#                 tag="menu_window")




# class Bird:
#     """"
#     This class is responsible for creating the player (bird) object on the main canvas window
#     and managing its motion (jumping and falling). 
#     """
#     # Private variable to store the file path for the player image
#     _PLAYER_IMAGE_FILE = "sprites/bird.png"
#     # Private attribute to store the maximum downward falling speed of the player
#     _GRAVITY_Y_SPEED = 3
#     # Private attribute to store the maximum upward jump speed of the player (directly proportional to the jump height)
#     _JUMP_Y_SPEED = -5
#     # Private attribute to store the y-coordinate of the upper window boundary which the bird must not cross
#     _UPPER_WINDOW_BOUNDARY = 20
#     # Private attribute to store the deceleration speed, which visually simulates the weight of the bird
#     _DOWNWARD_ACCELERATION = 0.25

#     def __init__(self, root, canvas, window_width, window_height):
#         """
#         Constructor function of the Bird class
#         :param root: the Tkinter root window
#         :param canvas: the Tkinter canvas class
#         :param window_width: width of the Canvas window
#         :param window_height: height of the Canvas window
#         """
#         self._root = root
#         self._canvas = canvas
#         self._window_width = window_width
#         self._window_height = window_height
#         # Variable to store the x-coordinate of the center of the window derived from its width
#         self.window_center_x = self._window_width/2
#         # Variable to store the y-coordinate of the center of the window derived from its height
#         self.window_center_y = self._window_height/2
#         # Tkinter private image attribute to store the player sprite
#         self._player_sprite = tk.PhotoImage(file=self._PLAYER_IMAGE_FILE)
#         # Initialize player object (bird) from the canvas class and store it in a private attribute self._player
#         self._player = self._canvas.create_image(self.window_center_x, self.window_center_y,
#                                                  image=self._player_sprite, anchor="c", tag="player")
#         # Private attribute to store the player's current vertical (y) speed
#         self._y_speed = self._GRAVITY_Y_SPEED
#         # Private attribute to store the player's current horizontal (x) speed
#         self._x_speed = 0

#     def player_fall(self):
#         """
#         Public method which makes the player move downward (fall)
#         """
#         # If the player hits the upper window boundary, make it bounce back down (the index of 1 indicates the y-coord)
#         if self.get_player_x_y_coords()[1] < self._UPPER_WINDOW_BOUNDARY:
#             self._y_speed = self._GRAVITY_Y_SPEED
#         # Make the payer move downward (fall)
#         self._canvas.move(self._player, self._x_speed, self._y_speed)
#         self._y_speed += self._DOWNWARD_ACCELERATION

#     def player_jump(self):
#         """
#         Public method which makes the player jump upward
#         """
#         self._y_speed = self._JUMP_Y_SPEED

#     def get_player_x_y_coords(self):
#         """
#         Public method which returns the x and y coordinates of the player (bird) on the canvas
#         """
#         return self._canvas.coords(self._player)


# class Pipe:
#     """
#     This class is responsible for creating the pipe objects on the main canvas window
#     and managing their motion (moving sideways)
#     """
#     # Private attribute to store an integer-type variable for the width constant for each pipe
#     _PIPE_WIDTH = 85
#     # Private attribute to store an integer-type variable for the vertical separation constant for each pipe
#     _PIPE_SEPARATION_Y = 120  # 160
#     # Private attribute to store a float-type variable for the maximum horizontal speed constant for each pipe
#     _MAX_X_SPEED = -2.6  # -2
#     # Private variable to store a float-type variable for the frequency of generation of each pipe
#     _PIPE_SPAWN_INTERVAL = 2.5  # only n-0.5 (where n = Whole num) i.e. 1.5; 2.5; 3.5
#     # Private int-type variable for the maximum offset distance from the top and bottom window boundaries
#     _PIPE_Y_OFFSET = 90
#     # Private variable to store a string-type for the color of each pipe
#     _PIPE_COLOR = "lime green"

#     def __init__(self, root, canvas, window_width, window_height):
#         """
#         Constructor function of the Pipe class
#         :param root: the Tkinter root window
#         :param canvas: the Tkinter canvas class
#         :param window_width: width of the Canvas window
#         :param window_height: height of the Canvas window
#         """
#         self._root = root
#         self._canvas = canvas
#         self._window_width = window_width
#         self._window_height = window_height

#         # Private variable to store the bottom pipe widget
#         self._pipe_bottom = None
#         # Private variable to store the top pipe widget
#         self._pipe_top = None
#         # Private integer-type variable to store the x-coordinate of the spawn origin of each pipe
#         self._origin_x = self._window_width
#         # Private integer-type variable to store the y-coordinate of the spawn origin of each upper pipe
#         self.top_pipe_origin_y = 0
#         # Private boolean-type variable to indicate whenever a new pipe is drawn to allow for time-regulated generation
#         self._pipe_drawn = False
#         # Private integer-type variable to store a constant for the horizontal speed of each pipe
#         self._x_speed = self._MAX_X_SPEED
#         # Private integer-type variable to store a constant for the vertical speed of each pipe
#         self._y_speed = 0
#         # Private integer-type variable to store a constant the number of dp that the game run-time is rounded to
#         self._pipe_generator_time_dp = 1
#         # Private integer-type variable to store a derived constant for the smallest length of a pipe from the top
#         self._min_length_from_top = self._PIPE_Y_OFFSET
#         # Private integer-type variable to store a derived constant for the biggest length of a pipe from the top
#         self._max_length_from_top = self._window_height - self._PIPE_Y_OFFSET - self._PIPE_SEPARATION_Y

#     def pipe_generator(self):
#         """
#         This public method controls the initialisation process of new pipe objects at pre-defined
#         time intervals (calls the pipe generator method when appropriate)
#         """
#         # Private float-type variable to store the time elapse since the start of the game instance
#         time_elapsed = round(time.time(), self._pipe_generator_time_dp)
#         """
#         An if statement that checks if the time elapsed since the last pipe creation divided by the value of the set
#         generation interval leaves no remained (output is 0), which implies that the pipe spawn time interval has 
#         passed and a new pipe should be spawned
#         """
#         if time_elapsed % self._PIPE_SPAWN_INTERVAL == 0:
#             # If a new pipe hasn't been drawn after the interval, generate a new pipe
#             if not self._pipe_drawn:
#                 self._draw_pipe_on_canvas()
#                 self._pipe_drawn = True
#         # If the time interval since the last pipe generated is not met, set the _pipe_drawn attribute to False
#         else:
#             self._pipe_drawn = False

#     def _draw_pipe_on_canvas(self):
#         """
#         This private method creates and draws new pipe objects on the canvas
#         """
#         # Private integer-type variable to store a randomly-generated height-from-top of the top pipe
#         top_pipe_len_from_top = random.randrange(self._min_length_from_top, self._max_length_from_top)
#         # Private integer-type variable to store the height-from-top for the bottom pipe derived from the previous var
#         bottom_pipe_len_from_top = top_pipe_len_from_top + self._PIPE_SEPARATION_Y
#         # Initialize bottom pipe object as a rectangle from the canvas class and store it in a private attribute
#         self._pipe_bottom = self._canvas.create_rectangle(self._origin_x, bottom_pipe_len_from_top,
#                                                           self._origin_x + self._PIPE_WIDTH, self._window_height,
#                                                           fill=self._PIPE_COLOR, tags=("pipe", "bottom_pipe"))
#         # Initialize top pipe object as a rectangle from the canvas class and store it in a private attribute
#         self._pipe_top = self._canvas.create_rectangle(self._origin_x, self.top_pipe_origin_y,
#                                                        self._origin_x + self._PIPE_WIDTH, top_pipe_len_from_top,
#                                                        fill=self._PIPE_COLOR, tags=("pipe", "top_pipe"))

#     def move_pipe(self):
#         """
#         Public method which makes both of the generated pipes (combined with a common tag)
#         move horizontally with a pre-set speed
#         """
#         self._canvas.move("pipe", self._x_speed, self._y_speed)


# class MainApplication:
#     """
#     This class containing that constructs the main game window, initializes widgets on the screen, and controls
#     the main game logic (flow)
#     """
#     # Private boolean-type variable to indicate whether a new game process has been initiated
#     _NEW_GAME = False
#     # Private boolean-type variable to indicate whether the current game process has ended
#     _GAME_OVER = False
#     # Private variable to store the file path for the game background image
#     _BACKGROUND_IMAGE_FILE = "sprites/background.png"

#     def __init__(self):
#         """
#         Constructor function of the MainApplication class
#         """



#         # Private variable to store an instance of the Bird class (player)
#         self._player = None

#         # Initialise an instance of the Pipe class and store in a private variable _pipe
#         self._pipe = Pipe(self.root, self._canvas, self._width, self._height)
#         # Private list to store the id of the last pipe pair (bottom pipe) that the user has passed through
#         self._scored_pipes = []


        # # Binding input from a user (keypress) to a private method _user_input_handler
        # self._canvas.bind("<KeyPress>", self._user_input_handler)
        # # Binding input from a user (mouse click) to a private method _user_input_handler
        # self._canvas.bind("<Button>", self._user_input_handler)
        # # Setting keyboard focus to the main canvas window
        # self._canvas.focus_set()


# # Score class
#         # Private integer-type variable to store the user's best scores
#         # self._best_score = 0
#         # # Private integer-type variable to store the user's current score (within a single game session)
#         # self._player_score = 0
#         # # Private variable to store the score counter widget
#         # self._score_counter_text = None
# # Score class


# # to Game Manager... 
#         # # Call to the initialisation of the game
#         # self._start()
#         # self.root.mainloop()

#     def _menu(self):
#         """
#         This private method generates the main user menu containing the start button and an instructions page
#         """
#         # Create a canvas rectangle widget to serve as the main menu's background
#         self._canvas.create_rectangle(
#             self.window_center_x-110, 
#             self.window_center_y-140,
#             self.window_center_x+110, 
#             self.window_center_y+15, 
#             fill="yellow",
#             tag="menu_window")
#         # Create a canvas text widget which stores the game title
#         self._canvas.create_text(self.window_center_x, self.window_center_y - 112, text="FloppyBird_v1", fill="black",
#                                  font=("ROBOTO", 12, "bold"), justify="center", tag="intro_menu_widget")
#         # Create a canvas text widget which stores the game author
#         self._canvas.create_text(self.window_center_x, self.window_center_y - 90, text="Author: Danila Khomenko",
#                                  fill="black", font=("ROBOTO", 11), justify="center", tag="intro_menu_widget")
#         # Create a canvas button widget to act as the main menu's "start" button
#         button_start_game = tk.Button(self._canvas, text="Start", anchor='c', font=("ROBOTO", 12, "bold"),
#                                       command=self._initialise_game_layout)
#         button_start_game.configure(width=10, background="orange")
#         # Create a canvas window widget to host the "start" button
#         self._canvas.create_window(self.window_center_x, self.window_center_y - 14, window=button_start_game,
#                                    tag="start_button")
#         # Create a canvas button widget to act as the main menu's "instructions" button
#         button_game_instructions = tk.Button(self._canvas, text="Instructions", anchor='c',
#                                              font=("ROBOTO", 12, "bold"),
#                                              command=self._instructions_screen)
#         button_game_instructions.configure(width=10, background="orange")
#         # Create a canvas window widget to host the "restart" button
#         self._canvas.create_window(self.window_center_x, self.window_center_y - 52, window=button_game_instructions,
#                                    tag="intro_menu_widget")

#     def _instructions_screen(self):
#         """
#         This private method presents the user with the game instructions
#         """
#         # Game instructions text
#         instructions = "Use <space>, <Button-1> \nor <Up-arrow> to make the \nbird jump. " \
#                        "Fly the bird as \nfar as you can without \nhitting a pipe."
#         # Remove any widgets related to the main menu
#         self._canvas.delete("intro_menu_widget")
#         # Create a canvas text widget which stores the instructions text
#         self._canvas.create_text(self.window_center_x, self.window_center_y - 85, text=instructions, fill="black",
#                                  font=("ROBOTO", 12), justify="center", tag="instructions_menu_widget")

#     def _user_input_handler(self, event):
#         """
#         This private method processes all input supplied by the user (excluding menu buttons) such as keyboard or mouse
#         events
#         :param event: information about the user event
#         :return: None
#         """
#         # This private variable stores the name of the key pressed by the user
#         key_press = event.keysym
#         # This private variable stores the name of the mouse button pressed by the user
#         button_press = event.num
#         if key_press in ("space", "Up") or button_press == 1:
#             # If a new game has just een started, treat the user input as a call to start a new game process
#             if self._NEW_GAME:
#                 self._NEW_GAME = False
#                 # Set the keyboard focus on the canvas window
#                 self._canvas.focus_set()
#                 self._player.player_jump()
#                 # Initiate the game flow
#                 self._main()

#             # If a game session has ended, treat the user input as a call to start a new game session (restart)
#             elif self._GAME_OVER and button_press != 1 and key_press == "space":
#                 self._restart_game()

#             # If a game session is currently running, treat the user input as calls for in-game mechanics (jumping)
#             else:
#                 # If the player exists, make it jump up
#                 if self._player:
#                     self._player.player_jump()

#     def _initialise_game_layout(self):
#         """
#         This function initialises the main game layout before each game session
#         """
#         # Remove all widgets present on the canvas
#         self._canvas.delete("all")
#         self._canvas.create_image(self.window_center_x, self.window_center_y,
#                                   image=self._background_image, anchor="c", tag="background")
#         # Initialise an instance of the Bird class and store in a private variable _player
#         self._player = Bird(self.root, self._canvas, self._width, self._height)
#         # Indicate that a new game session has been initiated
#         self._NEW_GAME = True

#     def _overlap_detection(self):
#         """
#         This private method detects when a collision or an overlap occurs within the game between the player
#         and other specified widgets
#         :return: a boolean indicating whether a collision has occurred between the player and a pipe object or the floor
#         """
#         # A private tuple containing IDs of canvas widgets under the "pipe" tag present on the screen
#         pipe_objects = self._canvas.find_withtag("pipe")
#         # A private list containing the coordinates of the player (bird) on the canvas
#         player_coords = self._player.get_player_x_y_coords()
#         # A private int-type variable containing the x coordinate of the player on the canvas
#         player_x = player_coords[0]
#         # A private int-type variable containing the y coordinate of the player on the canvas
#         player_y = player_coords[1]
#         # A tuple containing the IDs of canvas widgets that overlap with the player (bird) widget
#         overlapping_objects = self._canvas.find_overlapping(player_x - 18, player_y - 18, player_x + 22,
#                                                             player_y + 20)
#         for pipe in pipe_objects:
#             # Remove pipes that have left the canvas window to maximise performance
#             if self._canvas.coords(pipe)[2] < 0:
#                 # Check whether the current pipe object's id is in the _scored_pipes list
#                 if pipe in self._scored_pipes:
#                     # Remove the redundant widget ID from the list
#                     self._scored_pipes.remove(pipe)
#                 self._canvas.delete(pipe)
#             # Check whether the chosen pipe object is a bottom pipe
#             if "bottom_pipe" in self._canvas.gettags(pipe):
#                 # Check if the player has flown above the specified pipe without colliding with it (through the gap)
#                 if self._canvas.coords(pipe)[0] < player_x:
#                     # Check that the player hasn't yet been scored for passing through the given pipe pair
#                     if pipe not in self._scored_pipes:
#                         # If not, assign the given pipe to _scored_pipe
#                         self._scored_pipes.append(pipe)
#                         # Give the player 1 point and update the score board
#                         self._player_score += 1
#                         self._update_score()
#             # If, however, the player has physically collided with the given pipe or the floor, return True
#             if pipe in overlapping_objects:
#                 # Indicates a collision between the bird and a pipe, so a game over call should be made
#                 return True
#         # Indicates that a collision between the bird and the ground, so a game over call should be made
#         if self._player.get_player_x_y_coords()[1] > self._height - 31:
#             return True
#         else:
#             # Return False to indicate that no collision had occurred
#             return False

#     def _update_score(self):
#         """
#         This private method updates the game score text every time the user scores
#         """
#         # Clear the scoring board (if exists)
#         self._canvas.delete("score_counter")
#         # Initialize a new game score counter widget and store it in the private attribute _score_counter_text
#         self._score_counter_text = self._canvas.create_text(self.window_center_x, 120,
#                                                             text="{}".format(self._player_score), fill="white",
#                                                             font=("Arial", 50), justify="center", tag="score_counter")

#     def _game_over_menu(self):
#         """
#         This private method generates the "game over" menu with the user's end scores
#         """
#         self._GAME_OVER = True
#         self._canvas.delete("score_counter")
#         # Check whether the user had reached a new high score
#         if self._player_score > self._best_score:
#             # If so, set the new high score
#             self._best_score = self._player_score
#         # Create a canvas rectangle widget to serve as the menu's background
#         self._canvas.create_rectangle(self.window_center_x - 50, self.window_center_y - 135, self.window_center_x + 50,
#                                       self.window_center_y + 10, fill="yellow", tag="game_over_t")
#         # Create a canvas text widget to store and display the word "Score"
#         self._canvas.create_text(self.window_center_x, self.window_center_y - 110, text="Score", fill="black",
#                                  font=("Arial", 20), justify="center", tag="game_over_t")
#         # Create a canvas text widget to store and display the user's current score
#         self._canvas.create_text(self.window_center_x, self.window_center_y - 80, text=f"{self._player_score}", fill="red",
#                                  font=("Arial", 20), justify="center", tag="game_over_t")
#         # Create a canvas text widget to store and display the word "Best score"
#         self._canvas.create_text(self.window_center_x, self.window_center_y - 45, text="Best", fill="black",
#                                  font=("Arial", 20), justify="center", tag="game_over_t")
#         # Create a canvas text widget to store and display the user's best score
#         self._canvas.create_text(self.window_center_x, self.window_center_y - 15, text=f"{self._best_score}", fill="red",
#                                  font=("Arial", 20), justify="center", tag="game_over_t")
#         # Create a canvas button widget to act as the "restart" button
#         button_restart = tk.Button(self._canvas, text="Restart", anchor='c', font=("ROBOTO", 12, "bold"),
#                                    command=self._restart_game)
#         button_restart.configure(width=20, background="orange")
#         # Create a canvas window widget to host the "restart" button
#         self._canvas.create_window(self.window_center_x, self.window_center_y + 50, window=button_restart, tag="game_over_t")

#     def _restart_game(self):
#         """
#         This private method clears the main canvas window and restarts the game
#         """
#         self._canvas.delete("all")
#         self._GAME_OVER = False
#         self._player_score = 0
#         self._NEW_GAME = False
#         self._initialise_game_layout()

#     def _start(self):
#         """
#         This private method acts as a trigger to initiate a new game process
#         """
#         self._intro_menu()

#     def _main(self):
#         """
#         This function carries out the primary game flow (logic within a single game session)
#         """
#         # Raise the score text widget above the pipe widgets (if exists)
#         if self._score_counter_text:
#             self._canvas.tag_raise(self._score_counter_text)
#         # Generate a new pipe pair on the screen if appropriate
#         self._pipe.pipe_generator()
#         # Check the game window for collisions or overlaps between the existing widgets
#         collision = self._overlap_detection()
#         # Make the player move downward (fall due to gravity)
#         self._player.player_fall()
#         # Move the pipe objects towards the player
#         self._pipe.move_pipe()
#         # If no collision has been detected, repeat the process
#         if not collision:
#             self.root.after(15, self._main)
#         # If the player has collided with a pipe or the floor, initiate "game over" scene (menu)
#         else:
#             self._game_over_menu()


MainApplication()
