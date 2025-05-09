# settings.py

import pygame
import os

# --- Base Project Path ---
# Determine the absolute path of the directory where this file is located.
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Crucial for relative paths!

# --- Screen Settings ---
SCREEN_WIDTH = 800  # Width of the game window (pixels)
SCREEN_HEIGHT = 600 # Height of the game window (pixels)
FPS = 60            # Frames per second (game speed)

# --- Color Palette (Named Colors) ---
INDIGO = (48, 25, 125)
DARK_PURPLE = (72, 61, 139)
LIGHT_PURPLE = (138, 121, 209)
PINK_RASPBERRY = (222, 49, 99)
TEAL_GREEN = (26, 188, 156) # Additional color for positive emphasis
WHITE_ISH = (245, 245, 245) # Slightly off-white instead of pure white
YELLOW_HIGHLIGHT = (255, 210, 0) # For selection highlights
DARK_TEXT_ON_LIGHT = INDIGO # Dark text color on light background
INPUT_TEXT_COLOR = (10, 10, 10) # Text color in the player name input box
PAUSE_OVERLAY_COLOR = (0, 0, 0, 175) # Pause screen dimming color (RGBA - A: Alpha/transparency)

# --- Color Constants (By Purpose) ---
# Assigns palette colors to specific UI elements or states.
COLOR_BACKGROUND_DARK = INDIGO                     # Default in-game background color (if images fail)
COLOR_BACKGROUND_MENU_TOP = LIGHT_PURPLE           # Top color of menu gradient background
COLOR_BACKGROUND_MENU_BOTTOM = DARK_PURPLE         # Bottom color of menu gradient background
COLOR_PRIMARY = LIGHT_PURPLE                       # Primary button color, highlight color
COLOR_PRIMARY_HOVER = (160, 140, 230)              # Color when hovering over primary buttons
COLOR_SECONDARY = DARK_PURPLE                      # Secondary button color, passive element color
COLOR_ACCENT_POSITIVE = TEAL_GREEN                 # Positive action button (e.g., Continue)
COLOR_ACCENT_NEGATIVE = PINK_RASPBERRY             # Negative action button (e.g., Back, Exit), Game Over Background
COLOR_ACCENT_NEUTRAL = DARK_PURPLE                 # Neutral action or informational element color (Not used for expression background anymore)
COLOR_HIGHLIGHT = YELLOW_HIGHLIGHT                 # Highlight color for selected items (avatar, difficulty), High Score Message
COLOR_TEXT_LIGHT = WHITE_ISH                       # Light text color on dark background
COLOR_TEXT_DARK = DARK_TEXT_ON_LIGHT               # Dark text color on light background
COLOR_TEXT_INPUT = INPUT_TEXT_COLOR                # Text color in the player name input box

# --- Game Mechanics Settings ---
PLAYER_SPEED = 5                # Horizontal movement speed of the player (pixels/update)
PLAYER_AVATAR_SIZE = (100, 120) # On-screen size of the player avatar (width, height)
# Player Vertical Bobbing Settings
PLAYER_BOBBING_AMPLITUDE = 20   # Maximum vertical distance of bobbing (pixels)
PLAYER_BOBBING_FREQUENCY = 6.0  # Bobbing speed (cycles per second, higher is faster)

EXPRESSION_SPEED = 4            # Speed of falling mathematical expressions (pixels/update)
BACKGROUND_SCROLL_SPEED = 3     # General scrolling speed of the parallax background (base speed)
# DECORATION_SPEED_MULTIPLIER = 1.0 # Speed multiplier for decorations (if implemented)
TIME_LIMIT_SECONDS = 60         # Maximum duration of a game round (seconds)
GAME_OVER_SCORE_THRESHOLD = 10  # Game ends if the score falls below this value
STARTING_COINS = 25             # Initial amount of coins at the start of the game
NICKNAME_MAX_LENGTH = 12        # Maximum character length for the player name

# --- Sound Settings ---
GAME_MUSIC_VOLUME = 0.4         # Volume level for in-game background music (0.0 - 1.0)
MENU_MUSIC_VOLUME = 0.5         # Volume level for menu background music
WIN_SOUND_VOLUME = 0.7          # Volume level for win sound effect
LOSE_SOUND_VOLUME = 0.7         # Volume level for lose sound effect

# --- File and Folder Paths ---
# Define other paths relative to the base project folder (BASE_DIR)
ASSETS_FOLDER = os.path.join(BASE_DIR, 'assets')              # Main assets folder
DATA_FOLDER = os.path.join(ASSETS_FOLDER, 'data')             # Data files folder (scores, prefs)
IMAGE_FOLDER = os.path.join(ASSETS_FOLDER, 'images')          # Image files folder
AVATAR_FOLDER = os.path.join(IMAGE_FOLDER, 'avatars')         # Avatar images folder
SOUNDS_FOLDER = os.path.join(ASSETS_FOLDER, 'sounds')         # Sound files folder
FONT_FOLDER = os.path.join(ASSETS_FOLDER, 'fonts')            # Font files folder

# Data File Paths
HIGH_SCORES_FILE = os.path.join(DATA_FOLDER, 'high_scores.json') # High scores file
USER_PREFS_FILE = os.path.join(DATA_FOLDER, 'user_prefs.json')   # User preferences file

# Sound File Paths
BACKGROUND_MUSIC_FILE = os.path.join(SOUNDS_FOLDER, 'background_music.wav') # In-game music
MENU_MUSIC_FILE = os.path.join(SOUNDS_FOLDER, 'menu_music.wav')             # Menu music
WIN_SOUND_FILE = os.path.join(SOUNDS_FOLDER, 'win_sound.wav')               # Win sound
LOSE_SOUND_FILE = os.path.join(SOUNDS_FOLDER, 'lose.wav')                   # Lose sound

# --- Parallax Background Layers ---
# Make image paths relative using IMAGE_FOLDER
# IMPORTANT: Ensure these filenames exactly match the files in 'assets/images/'
BACKGROUND_LAYER_FAR_IMAGE = os.path.join(IMAGE_FOLDER, 'T_PurpleBackground_Version2_Layer1.png') 
BACKGROUND_LAYER_FAR_SPEED_MULTIPLIER = 0.2 # Slowest layer

BACKGROUND_LAYER_MID_IMAGE = os.path.join(IMAGE_FOLDER, 'T_PurpleBackground_Version1_Layer3.png') 
BACKGROUND_LAYER_MID_SPEED_MULTIPLIER = 0.5 # Medium speed layer

BACKGROUND_LAYER_NEAR_IMAGE = os.path.join(IMAGE_FOLDER, 'T_PurpleBackground_Version3_Layer4.png') 
BACKGROUND_LAYER_NEAR_SPEED_MULTIPLIER = 1.0 # Fastest layer (same as base scroll speed)

# --- Game States (Constants for State Machine) ---
# String constants representing different screens or modes of the game.
STATE_INTRO = "INTRO"                       # Intro screen / Main menu
STATE_GET_NICKNAME = "GET_NICKNAME"         # Player name input screen
STATE_AVATAR_SELECT = "AVATAR_SELECT"       # Avatar selection screen
STATE_DIFFICULTY_SELECT = "DIFFICULTY_SELECT" # Difficulty selection screen
STATE_PLAYING = "PLAYING"                   # Active gameplay state
# STATE_PAUSED = "PAUSED"                   # Paused state (managed within game.py)
STATE_GAME_OVER = "GAME_OVER"               # Game over screen
STATE_HIGH_SCORES = "HIGH_SCORES"           # High scores list screen
STATE_RULES = "RULES"                       # Game rules screen

# --- Action Constants ---
# Used to specify certain actions or game end reasons.
ACTION_RETURN_TO_MENU = "RETURN_MENU" # When the player chooses to return to the menu

# --- Level Definitions ---
# Defines the operators and operand range for each difficulty level.
LEVELS = {
    1: {
        'name': "Easy",                      # Name displayed on the screen (Translated)
        'operators': ['+', '-', '*', '/'],   # Operators to be used
        'operand_range': (1, 10)             # Range of operand values (min, max inclusive)
    },
    2: {
        'name': "Medium",                    
        'operators': ['+', '-', '*', '/', '**', 'sqrt'], # Added exponentiation and square root
        'operand_range': (1, 15)             # Slightly wider range
    },
    3: {
        'name': "Hard",                      
        'operators': ['+', '-', '*', '/', '**', 'sqrt', 'pow0.5'], # pow0.5 = sqrt
        'operand_range': (-5, 20)            # Negative numbers and a wider range
    }
}