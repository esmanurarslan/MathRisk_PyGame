# MathRisk

MathRisk is a 2D arcade-style educational action game built with Python and Pygame. The player controls a character at the bottom of the screen, dodging and collecting falling shapes containing mathematical expressions. Each collected shape modifies the player's "Coin" score based on the operation inside (+, -, *, /, ^, √). The goal is to achieve the highest score possible before the time runs out or the Coin count drops below a certain threshold.

## Features

*   **Fast-Paced Gameplay:** Dodge and collect falling mathematical expressions.
*   **Score Management:** Apply collected operations to your Coin score strategically.
*   **Multiple Difficulty Levels:** Choose from Easy, Medium, and Hard, affecting the complexity and speed of expressions.
*   **Parallax Background:** Visually engaging multi-layered scrolling background.
*   **Selectable Avatars:** Choose your character from available options.
*   **High Score System:** Compete against yourself and others by saving top scores.
*   **Basic Animations:** Player character bobbing animation during movement.
*   **Sound Integration:** Background music for menus and gameplay, plus win/lose sound effects.
*   **User-Friendly UI:** Clear interface for score, time, and game menus.

## Technology Used

*   **Python 3**
*   **Pygame** library

## Setup and Installation

1.  **Ensure Python is Installed:** You need Python 3 installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
2.  **Install Pygame:** Open your terminal or command prompt and install the Pygame library using pip:
    ```bash
    pip install pygame
    ```
    *(If `pip` is not recognized, try `python -m pip install pygame` or `py -m pip install pygame`)*
3.  **Get the Project Files:** Make sure you have all the project files (`.py` files and the `assets` folder) in the same directory, maintaining the original folder structure. The `assets` folder (containing `images`, `sounds`, `fonts`, `data`) must be in the same directory as `main.py`.

## How to Run the Game

1.  Navigate to the project directory in your terminal or command prompt.
2.  Run the main game file using Python:
    ```bash
    python main.py
    ```
    *(Or `py main.py`)*

The game window should open, starting with the main menu.

## How to Play

*   **Movement:** Use the **Left Arrow Key** and **Right Arrow Key** to move your character horizontally.
*   **Objective:** Collect the falling shapes containing mathematical expressions to increase (or decrease) your "Coin" score. Aim for the highest score within the time limit (e.g., 90 seconds).
*   **Game Over:** The game ends when the timer reaches zero OR your Coin score drops below the minimum threshold (e.g., 0).
*   **Pause:** Press the **P Key** to pause and unpause the game.
*   **Menu Navigation:** Use the **Mouse (Left Click)** to interact with buttons in the menus (Start, Rules, High Scores, Select Avatar, Select Difficulty, Back, Continue, etc.).
*   **Quit Pause Menu:** While paused, press the **ESC Key** to return to the main menu.
*   **Nickname Entry:** Use your keyboard to type your nickname and press **Enter** to confirm. Use **Backspace** to delete characters.

## Project Structure (Brief)

*   `main.py`: Main application entry point, game state manager, asset loading.
*   `game.py`: Contains the main game loop (`run_game`), `Player` and `Expression` sprite classes, game logic.
*   `ui.py`: Handles drawing all UI screens (menus, game over, etc.), `TextInputBox` class, data saving/loading (JSON).
*   `settings.py`: Stores all game constants (colors, speeds, paths, levels, etc.).
*   `expression_handler.py`: Generates random mathematical expressions based on difficulty.
*   `assets/`: Folder containing all game assets (images, sounds, fonts, saved data).


<img width="925" alt="Ekran Resmi 2025-05-10 00 18 56" src="https://github.com/user-attachments/assets/db006fb0-0349-42e6-a59f-e6b8718134d9" />

---

Enjoy playing MathRisk!
