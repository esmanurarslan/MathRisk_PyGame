# main.py 

import pygame
import sys
import os
import settings # Game settings and constants
import ui # User interface functions and classes
import game # Main game loop function

def main():
    """
    Main entry point of the game. Initializes Pygame, loads assets,
    manages game states, and transitions between menu/game screens.
    """
    try:
        # Initialize Pygame modules
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        print("DEBUG: Pygame and its modules initialized successfully.")
    except Exception as e:
        print(f"Error: Pygame or its modules could not be initialized: {e}")
        sys.exit()

    # Fonts
    try:
        # Use relative path based on BASE_DIR from settings
        font_path = os.path.join(settings.FONT_FOLDER, 'ScreenMatrix.ttf') 
        font_title = pygame.font.Font(font_path, 70)
        font_small_title = pygame.font.Font(font_path, 50)
        font_normal = pygame.font.Font(font_path, 30)
        font_button = pygame.font.Font(font_path, 30)
        font_small = pygame.font.Font(font_path, 20)
        print(f"DEBUG: Fonts loaded from '{font_path}'.")
    except Exception as e:
        print(f"Font could not be loaded ({font_path}): {e}. Using default fonts.")
        font_title = pygame.font.Font(None, 74); 
        font_normal = pygame.font.Font(None, 48); 
        font_button = pygame.font.Font(None, 30); 
        font_small = pygame.font.Font(None, 30)

    # Screen and Clock Objects
    try:
        screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("MathRisk")  
        clock = pygame.time.Clock()
    except Exception as e: 
        print(f"Error: Screen could not be created: {e}"); 
        pygame.quit(); 
        sys.exit()

    # Data Loading
    os.makedirs(settings.DATA_FOLDER, exist_ok=True)
    user_preferences = ui.load_user_prefs();
    high_scores = ui.load_high_scores()
    current_nickname = user_preferences.get('nickname', '');
    selected_avatar_index = user_preferences.get('avatar_index', 0);
    selected_difficulty = user_preferences.get('difficulty', 1)

    # Load Static Avatars
    avatars = []
    if not os.path.exists(settings.AVATAR_FOLDER): print(f"Warning: Avatar folder not found: {settings.AVATAR_FOLDER}")
    else:
        try:
            avatar_files = sorted([f for f in os.listdir(settings.AVATAR_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
            if not avatar_files: 
                print(f"Warning: No images found in the avatar folder ('{settings.AVATAR_FOLDER}').")
            else:
                print(f"DEBUG: Found static avatar files: {avatar_files}")
                for fname in avatar_files:
                    img_path = os.path.join(settings.AVATAR_FOLDER, fname)
                    try: 
                        avatars.append(pygame.image.load(img_path).convert_alpha())
                    except pygame.error as img_err: 
                        print(f"Error: Static avatar could not be loaded: {img_path} - {img_err}")
            if not avatars: selected_avatar_index = -1
            elif not (0 <= selected_avatar_index < len(avatars)):
                 print(f"Warning: Saved avatar index ({selected_avatar_index}) is invalid. Resetting to 0."); selected_avatar_index = 0; user_preferences['avatar_index'] = 0; ui.save_user_prefs(user_preferences)
        except Exception as e: print(f"Error: Loading static avatars failed: {e}"); avatars = []; selected_avatar_index = -1

    # --- LOAD SOUND FILES ---
    menu_music_loaded = os.path.exists(settings.MENU_MUSIC_FILE); win_sound = None; lose_sound = None
    if os.path.exists(settings.WIN_SOUND_FILE):
        try: win_sound = pygame.mixer.Sound(settings.WIN_SOUND_FILE); win_sound.set_volume(settings.WIN_SOUND_VOLUME); print(f"DEBUG: Win sound loaded: {os.path.basename(settings.WIN_SOUND_FILE)}")
        except pygame.error as e: print(f"ERROR: Loading win sound failed ({settings.WIN_SOUND_FILE}): {e}")
    if os.path.exists(settings.LOSE_SOUND_FILE):
        try: lose_sound = pygame.mixer.Sound(settings.LOSE_SOUND_FILE); lose_sound.set_volume(settings.LOSE_SOUND_VOLUME); print(f"DEBUG: Lose sound loaded: {os.path.basename(settings.LOSE_SOUND_FILE)}")
        except pygame.error as e: print(f"ERROR: Loading lose sound failed ({settings.LOSE_SOUND_FILE}): {e}")
    # Add warnings if files not found
    if not os.path.exists(settings.WIN_SOUND_FILE): print(f"WARNING: Win sound file not found: {settings.WIN_SOUND_FILE}")
    if not os.path.exists(settings.LOSE_SOUND_FILE): print(f"WARNING: Lose sound file not found: {settings.LOSE_SOUND_FILE}")

    # Initial Game State
    game_state = settings.STATE_INTRO
    if not current_nickname: game_state = settings.STATE_GET_NICKNAME
    elif not avatars or selected_avatar_index == -1:
         if current_nickname: game_state = settings.STATE_AVATAR_SELECT # Go to avatar select if name exists but avatar doesn't

    # UI Elements
    nickname_input = ui.TextInputBox(settings.SCREEN_WIDTH // 2 - 175, settings.SCREEN_HEIGHT // 2 - 30, 350, 60, font_normal, max_len=settings.NICKNAME_MAX_LENGTH, text=current_nickname)

    # Game End Variables
    last_score = 0; last_game_over_reason = ""; current_music_playing = None; show_new_high_score_message = False

    # Main Game Loop
    running = True
    while running:
        # --- MUSIC CONTROL ---
        menu_states = [settings.STATE_INTRO, settings.STATE_GET_NICKNAME, settings.STATE_AVATAR_SELECT, settings.STATE_DIFFICULTY_SELECT, settings.STATE_GAME_OVER, settings.STATE_HIGH_SCORES, settings.STATE_RULES]
        if menu_music_loaded and game_state in menu_states and current_music_playing != 'menu':
            try:
                if pygame.mixer.music.get_busy(): pygame.mixer.music.stop(); pygame.time.delay(50)
                pygame.mixer.music.load(settings.MENU_MUSIC_FILE); pygame.mixer.music.set_volume(settings.MENU_MUSIC_VOLUME); pygame.mixer.music.play(loops=-1)
                current_music_playing = 'menu'; print("DEBUG [Menu]: Menu music started.")
            except Exception as e: print(f"ERROR [Menu]: Could not start menu music: {e}"); current_music_playing = None
        elif game_state == settings.STATE_PLAYING and current_music_playing == 'menu':
             if menu_music_loaded and pygame.mixer.music.get_busy(): pygame.mixer.music.fadeout(500)
             current_music_playing = 'game'

        # --- Event Handling ---
        events = pygame.event.get() # Get events ONCE per frame
        for event in events:
            if event.type == pygame.QUIT: running = False

            # --- State-Specific Event Handling ---
            if game_state == settings.STATE_GET_NICKNAME:
                result = nickname_input.handle_event(event) # Let the input box handle its events
                if result == "submit":
                    current_nickname = nickname_input.text.strip()
                    if current_nickname: # Only proceed if name is not empty
                        user_preferences['nickname'] = current_nickname
                        user_preferences['avatar_index'] = selected_avatar_index # Save current avatar index too
                        user_preferences['difficulty'] = selected_difficulty # Save current difficulty
                        ui.save_user_prefs(user_preferences)
                        # Decide next state based on avatar availability
                        game_state = settings.STATE_AVATAR_SELECT if avatars and selected_avatar_index != -1 else settings.STATE_DIFFICULTY_SELECT
                        pygame.time.delay(100) # Short delay prevents accidental double processing
                    else:
                        print("DEBUG: Empty nickname submitted.") # Or show an on-screen message

            # Let the UI functions handle their own events by passing the 'events' list
            # This is handled inside the state machine below

        # --- State Machine ---
        if game_state == settings.STATE_INTRO:
            show_new_high_score_message = False
            next_state = ui.draw_intro_screen(screen, font_title, font_button, events) # Pass events
            if next_state:
                if next_state == settings.STATE_GET_NICKNAME and current_nickname:
                     # Skip nickname input if name exists, decide based on avatar
                     game_state = settings.STATE_AVATAR_SELECT if avatars and 0 <= selected_avatar_index < len(avatars) else settings.STATE_DIFFICULTY_SELECT
                else: game_state = next_state

        elif game_state == settings.STATE_GET_NICKNAME:
             # Nickname input box events handled above, draw handles button clicks
             next_state = ui.draw_nickname_screen(screen, font_title,font_small_title, font_normal, nickname_input, events) # Pass events
             if next_state:
                 # If "Continue" was clicked (STATE_AVATAR_SELECT is returned)
                 if next_state == settings.STATE_AVATAR_SELECT:
                     # Nickname is already saved from handle_event, decide next state
                     game_state = settings.STATE_AVATAR_SELECT if avatars and selected_avatar_index != -1 else settings.STATE_DIFFICULTY_SELECT
                 else: # If "Back" was clicked
                     game_state = settings.STATE_INTRO

        elif game_state == settings.STATE_AVATAR_SELECT:
             # Avatar screen handles its clicks internally using events
             next_state, new_selection = ui.draw_avatar_screen(screen, font_title, font_normal, font_button, avatars, selected_avatar_index, events) # Pass events
             selected_avatar_index = new_selection # Update selection immediately
             if next_state: # If "Continue" or "Back" was clicked
                 if next_state == settings.STATE_DIFFICULTY_SELECT: # If "Continue"
                     user_preferences['avatar_index'] = selected_avatar_index # Save selection
                     user_preferences['difficulty'] = selected_difficulty # Keep current difficulty
                     ui.save_user_prefs(user_preferences)
                 game_state = next_state # Go to next state

        elif game_state == settings.STATE_DIFFICULTY_SELECT:
            # Difficulty screen handles its clicks internally using events
            chosen_level_or_action = ui.draw_difficulty_screen(screen, font_title, font_button, settings.LEVELS, selected_difficulty, events) # Pass events
            if chosen_level_or_action is not None:
                if isinstance(chosen_level_or_action, int): # Level selected
                    selected_difficulty = chosen_level_or_action
                    user_preferences['difficulty'] = selected_difficulty;
                    user_preferences['avatar_index'] = selected_avatar_index; # Save current avatar too
                    ui.save_user_prefs(user_preferences);
                    game_state = settings.STATE_PLAYING
                else: # "Back" selected
                    game_state = settings.STATE_AVATAR_SELECT if avatars and selected_avatar_index != -1 else settings.STATE_GET_NICKNAME

        elif game_state == settings.STATE_RULES:
            # Rules screen handles its click internally using events
            next_state = ui.draw_rules_screen(screen, font_title, font_normal, font_button, events) # Pass events
            if next_state: game_state = next_state # Go back to Intro

        elif game_state == settings.STATE_PLAYING:
            # Pre-game checks
            if not current_nickname: game_state = settings.STATE_GET_NICKNAME; continue
            if not avatars or not (0 <= selected_avatar_index < len(avatars)): game_state = settings.STATE_AVATAR_SELECT; continue
            if selected_difficulty not in settings.LEVELS: selected_difficulty = 1; user_preferences['difficulty'] = 1; ui.save_user_prefs(user_preferences)
            chosen_avatar_img = avatars[selected_avatar_index]
            # Start the game
            print(f"\n--- Starting Game ---"); print(f" Player: {current_nickname}, Avatar: {selected_avatar_index}, Difficulty: {selected_difficulty}")
            final_score, reason = game.run_game(screen, clock, selected_difficulty, chosen_avatar_img, current_nickname)
            print(f"--- Game Over ---")
            current_music_playing = None # Allow menu music to restart
            # Handle game outcome
            if reason == settings.ACTION_RETURN_TO_MENU:
                game_state = settings.STATE_INTRO; show_new_high_score_message = False
            else:
                last_score = final_score; last_game_over_reason = reason;
                is_new_high_score = False; show_new_high_score_message = False

                # --- YÜKSEK SKOR KONTROLÜ---

                if final_score < settings.GAME_OVER_SCORE_THRESHOLD:
                    print(f"DEBUG: Score ({final_score}) below threshold. Playing lose sound."); pygame.mixer.music.stop()
                    if lose_sound: lose_sound.play(); print("DEBUG: Lose sound played (score low).")
                    else: print("Warning: Lose sound not loaded.")
                elif final_score > 0: # Sadece pozitif skorları işle
                    current_high = 0 # Varsayılan en yüksek skor 0
                    try:
                        # 1. Liste boş mu?
                        if high_scores:
                            # 2. İlk eleman sözlük mü ve 'score' anahtarı var mı?
                            if isinstance(high_scores[0], dict) and 'score' in high_scores[0]:
                                current_high = int(high_scores[0]['score']) # Skoru al ve int yap
                            else:
                                print("Warning: High scores list item 0 is not a valid dictionary with 'score'.")
                             

                    except (ValueError, TypeError, IndexError) as e:
                        # int'e çevirme hatası, index hatası veya başka bir sorun olursa
                        print(f"Warning: Could not reliably get current high score: {e}. Assuming 0.")
                        current_high = 0
                    except Exception as e: # Beklenmedik diğer hatalar
                         print(f"Unexpected error getting high score: {e}")
                         current_high = 0
                        # Şimdi güvenli current_high ile karşılaştır
                    if final_score > current_high:
                        is_new_high_score = True; show_new_high_score_message = True; print(f"DEBUG: New High Score! ({final_score} > {current_high})"); pygame.mixer.music.stop()
                        if win_sound: win_sound.play(); print("DEBUG: Win sound played.")
                        else: print("Warning: Win sound not loaded.")
                    else: # Yeni yüksek skor değil
                        print("DEBUG: High score not beaten."); pygame.mixer.music.stop()
                        if lose_sound: lose_sound.play(); print("DEBUG: Lose sound played (score > 0, no new high).")
                        else: print("Warning: Lose sound not loaded.")

                

                

                    # Skoru ekle ve kaydet
                high_scores = ui.add_high_score(current_nickname, final_score, high_scores);
                ui.save_high_scores(high_scores)

                

                # Her durumda Game Over ekranına geç
                game_state = settings.STATE_GAME_OVER
                print("DEBUG: Transitioning to Game Over state.") # Go to Game Over screen

        elif game_state == settings.STATE_GAME_OVER:
            # Game Over screen handles its clicks internally using events
            next_state = ui.draw_game_over_screen(screen, font_title, font_normal, font_button, last_score, last_game_over_reason, show_new_high_score_message, events) # Pass events
            if next_state: game_state = next_state

        elif game_state == settings.STATE_HIGH_SCORES:
             show_new_high_score_message = False
             # High Scores screen handles its clicks internally using events
             next_state = ui.draw_high_scores_screen(screen, font_title, font_normal, font_button, high_scores, events) # Pass events
             if next_state: game_state = next_state

        pygame.display.flip()
        clock.tick(settings.FPS)

    # --- After Main Loop ---
    print("DEBUG: Main loop ended, exiting..."); pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()