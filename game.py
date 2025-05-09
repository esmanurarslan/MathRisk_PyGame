# game.py 

import pygame
import random
import time
import sys
import math # For sine function and square root
import os
import settings # For game settings
import expression_handler as eh # Expression generator
import ui # For UI drawing functions (like buttons and pause screen)

# --- Helper Functions ---
def darken_color(color, amount=30):
    """Darkens the given color by the specified amount (RGB)."""
    return tuple(max(0, c - amount) for c in color)

def calculate_polygon_vertices(shape_type, center_x, center_y, radius):
    """Calculates vertices for pentagons and stars."""
    vertices = []; num_sides = 0; angle_offset = -math.pi / 2
    if shape_type == 'pentagon': num_sides = 5
    elif shape_type == 'star': num_points = 5; inner_radius = radius * 0.5
    if shape_type == 'pentagon':
        for i in range(num_sides): angle = angle_offset + (2 * math.pi * i / num_sides); x = center_x + radius * math.cos(angle); y = center_y + radius * math.sin(angle); vertices.append((int(x), int(y)))
    elif shape_type == 'star':
        for i in range(num_points * 2): current_radius = radius if i % 2 == 0 else inner_radius; angle = angle_offset + (math.pi * i / num_points); x = center_x + current_radius * math.cos(angle); y = center_y + current_radius * math.sin(angle); vertices.append((int(x), int(y)))
    return vertices

# --- Player Class ---
class Player(pygame.sprite.Sprite):
    """Represents the player character."""
    def __init__(self, avatar_img, start_x, start_y):
        super().__init__()
        if not isinstance(avatar_img, pygame.Surface):
            print("Error: Invalid avatar image passed to Player. Using fallback."); self.image_original = pygame.Surface(settings.PLAYER_AVATAR_SIZE); self.image_original.fill(settings.COLOR_ACCENT_NEGATIVE)
        else:
            try: self.image_original = pygame.transform.scale(avatar_img.convert_alpha(), settings.PLAYER_AVATAR_SIZE)
            except Exception as e: print(f"Error: Player avatar scaling failed: {e}. Using fallback."); self.image_original = pygame.Surface(settings.PLAYER_AVATAR_SIZE); self.image_original.fill(settings.COLOR_ACCENT_NEGATIVE)
        self.image = self.image_original.copy(); self.rect = self.image.get_rect(center=(start_x, start_y)); self.speed = settings.PLAYER_SPEED; self.base_y = start_y; self.bobbing_timer = 0.0

    def update(self, keys, dt):
        """Updates player position based on keys and applies bobbing."""
        is_moving_horizontally = False
        if keys[pygame.K_LEFT] and self.rect.left > 0: self.rect.x -= self.speed; is_moving_horizontally = True
        if keys[pygame.K_RIGHT] and self.rect.right < settings.SCREEN_WIDTH: self.rect.x += self.speed; is_moving_horizontally = True
        if is_moving_horizontally:
            self.bobbing_timer += dt; y_offset = settings.PLAYER_BOBBING_AMPLITUDE * math.sin(self.bobbing_timer * settings.PLAYER_BOBBING_FREQUENCY); self.rect.centery = self.base_y + int(y_offset)
        else: self.rect.centery = self.base_y
        # Boundary checks
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > settings.SCREEN_WIDTH: self.rect.right = settings.SCREEN_WIDTH

# --- Expression Class ---
class Expression(pygame.sprite.Sprite):
    """Represents a falling mathematical expression in a shape."""
    SHAPES = ['circle', 'square', 'pentagon', 'star', 'rounded_rect']; COLORS = [settings.LIGHT_PURPLE, settings.DARK_PURPLE, settings.PINK_RASPBERRY, settings.TEAL_GREEN, settings.COLOR_PRIMARY, settings.COLOR_SECONDARY, (100, 100, 200), (255, 165, 0)]
    def __init__(self, text, operator, operand, font, center_x):
        super().__init__(); self.text = text; self.operator = operator; self.operand = operand; self.font = font; self.speed = settings.EXPRESSION_SPEED
        try:
            self.shape_type = random.choice(self.SHAPES); self.fill_color = random.choice(self.COLORS); self.border_color = darken_color(self.fill_color, 40); self.text_color = settings.COLOR_TEXT_LIGHT
            text_surface = self.font.render(text, True, self.text_color); text_rect = text_surface.get_rect(); padding = 12 if self.shape_type not in ['star', 'pentagon'] else 18; min_dimension = max(text_rect.width, text_rect.height) + padding * 2; radius = min_dimension // 2; shape_size = (min_dimension, min_dimension)
            self.image = pygame.Surface(shape_size, pygame.SRCALPHA); surf_center_x = self.image.get_width() // 2; surf_center_y = self.image.get_height() // 2; shape_rect = pygame.Rect(0, 0, min_dimension, min_dimension); shape_rect.center = (surf_center_x, surf_center_y); border_width = 3
            if self.shape_type == 'circle': pygame.draw.circle(self.image, self.fill_color, (surf_center_x, surf_center_y), radius); pygame.draw.circle(self.image, self.border_color, (surf_center_x, surf_center_y), radius, border_width)
            elif self.shape_type == 'square': pygame.draw.rect(self.image, self.fill_color, shape_rect); pygame.draw.rect(self.image, self.border_color, shape_rect, border_width)
            elif self.shape_type == 'rounded_rect': border_radius = 8; pygame.draw.rect(self.image, self.fill_color, shape_rect, border_radius=border_radius); pygame.draw.rect(self.image, self.border_color, shape_rect, border_width, border_radius=border_radius)
            elif self.shape_type in ['pentagon', 'star']:
                 vertices = calculate_polygon_vertices(self.shape_type, surf_center_x, surf_center_y, radius);
                 if vertices: pygame.draw.polygon(self.image, self.fill_color, vertices); pygame.draw.polygon(self.image, self.border_color, vertices, border_width);
                 else: print(f"Warning: Could not calculate vertices for '{self.shape_type}', drawing square."); pygame.draw.rect(self.image, self.fill_color, shape_rect); pygame.draw.rect(self.image, self.border_color, shape_rect, border_width)
            text_draw_rect = text_surface.get_rect(center=(surf_center_x, surf_center_y)); self.image.blit(text_surface, text_draw_rect); self.rect = self.image.get_rect(center=(center_x, -self.image.get_height() // 2))
        except Exception as e:
            print(f"Error: Creating Expression visual failed: {e}"); self.image = pygame.Surface([40, 40]); self.image.fill(settings.COLOR_SECONDARY); pygame.draw.rect(self.image, settings.COLOR_ACCENT_NEGATIVE, self.image.get_rect(), 2); self.rect = self.image.get_rect(center=(center_x, -20))
            if not hasattr(self, 'text'): self.text = "?"; 
            if not hasattr(self, 'operator'): self.operator = '+'; 
            if not hasattr(self, 'operand'): self.operand = 1
    def update(self, *args):
        """Moves the expression down and removes it if it goes off-screen."""
        self.rect.y += self.speed
        if self.rect.top > settings.SCREEN_HEIGHT:
            self.kill() # Remove from all groups

# --- Main Game Function ---
def run_game(screen, clock, difficulty_level, avatar_image, nickname):
    """Runs the main game loop."""
    # Fonts
    font_path = os.path.join(settings.BASE_DIR, 'assets', 'fonts', 'ScreenMatrix.ttf')
    try: game_font_small = pygame.font.Font(font_path, 22); game_font_medium = pygame.font.Font(font_path, 28); game_font_large = pygame.font.Font(font_path, 45)
    except Exception as e: print(f"Game Font Error ({font_path}): {e}. Using default."); game_font_small=pygame.font.Font(None, 28); game_font_medium=pygame.font.Font(None, 36); game_font_large=pygame.font.Font(None, 55)

    # Load Background Images
    bg_far_img, bg_mid_img, bg_near_img = None, None, None
    bg_far_h, bg_mid_h, bg_near_h = 0, 0, 0
    bg_loaded_count = 0
    try: # Far
        if os.path.exists(settings.BACKGROUND_LAYER_FAR_IMAGE): 
            bg_far_img = pygame.image.load(settings.BACKGROUND_LAYER_FAR_IMAGE).convert(); bg_far_h = bg_far_img.get_height();
            if bg_far_h > 0: print(f"DEBUG: Far layer loaded: {os.path.basename(settings.BACKGROUND_LAYER_FAR_IMAGE)}"); bg_loaded_count += 1 
            else: print(f"Warning: Far layer ({os.path.basename(settings.BACKGROUND_LAYER_FAR_IMAGE)}) height is 0."); bg_far_img = None 
        else: print(f"Warning: Far layer image not found: {settings.BACKGROUND_LAYER_FAR_IMAGE}")
    except Exception as e: print(f"Error: Loading far layer failed: {e}")
    try: # Mid
        if os.path.exists(settings.BACKGROUND_LAYER_MID_IMAGE): 
            bg_mid_img = pygame.image.load(settings.BACKGROUND_LAYER_MID_IMAGE).convert_alpha(); bg_mid_h = bg_mid_img.get_height();
            if bg_mid_h > 0: print(f"DEBUG: Mid layer loaded: {os.path.basename(settings.BACKGROUND_LAYER_MID_IMAGE)}"); bg_loaded_count += 1 
            else: print(f"Warning: Mid layer ({os.path.basename(settings.BACKGROUND_LAYER_MID_IMAGE)}) height is 0."); bg_mid_img = None 
        else: print(f"Warning: Mid layer image not found: {settings.BACKGROUND_LAYER_MID_IMAGE}")
    except Exception as e: print(f"Error: Loading mid layer failed: {e}")
    try: # Near
        if os.path.exists(settings.BACKGROUND_LAYER_NEAR_IMAGE): 
            bg_near_img = pygame.image.load(settings.BACKGROUND_LAYER_NEAR_IMAGE).convert_alpha(); bg_near_h = bg_near_img.get_height();
            if bg_near_h > 0: print(f"DEBUG: Near layer loaded: {os.path.basename(settings.BACKGROUND_LAYER_NEAR_IMAGE)}"); bg_loaded_count += 1 
            else: print(f"Warning: Near layer ({os.path.basename(settings.BACKGROUND_LAYER_NEAR_IMAGE)}) height is 0."); bg_near_img = None 
        else: print(f"Warning: Near layer image not found: {settings.BACKGROUND_LAYER_NEAR_IMAGE}")
    except Exception as e: print(f"Error: Loading near layer failed: {e}")
    if bg_loaded_count == 0: print("Warning: No background layers were loaded!")
    # Background positions
    bg_far_y1 = 0; bg_far_y2 = -bg_far_h if bg_far_h > 0 else 0; bg_mid_y1 = 0; bg_mid_y2 = -bg_mid_h if bg_mid_h > 0 else 0; bg_near_y1 = 0; bg_near_y2 = -bg_near_h if bg_near_h > 0 else 0; bg_speed = settings.BACKGROUND_SCROLL_SPEED

    # Load Game Music
    game_music_playing = False; 
    try:
        game_music_path = settings.BACKGROUND_MUSIC_FILE
        if os.path.exists(game_music_path): 
            pygame.mixer.music.load(game_music_path); pygame.mixer.music.set_volume(settings.GAME_MUSIC_VOLUME); pygame.mixer.music.play(loops=-1)
            if pygame.mixer.music.get_busy(): game_music_playing = True; print("DEBUG [Game]: Game music started.") 
            else: print(">>> WARNING [Game]: Music play() returned False after get_busy()!") 
        else: print(f"WARNING [Game]: Game music file not found: {game_music_path}")
    except pygame.error as e: print(f"PYGAME ERROR [Game]: Music load/play failed: {os.path.basename(game_music_path)} - Error: {e}")
    except Exception as e: print(f"UNEXPECTED ERROR [Game]: Music loading/playing: {e}")

    # Game Variables
    current_score = settings.STARTING_COINS; start_time = time.time(); total_paused_time = 0; pause_start_time = 0; game_over = False; game_over_reason = ""; paused = False
    if difficulty_level not in settings.LEVELS: difficulty_level = 1;
    level_config = settings.LEVELS[difficulty_level]

    # Sprite Groups
    all_sprites = pygame.sprite.Group(); expressions_group = pygame.sprite.Group()

    # Create Player
    player_start_y = settings.SCREEN_HEIGHT - (settings.PLAYER_AVATAR_SIZE[1] // 2 + 20)
    player = Player(avatar_image, settings.SCREEN_WIDTH // 2, player_start_y)
    all_sprites.add(player)

    # Spawn Timers and other settings
    expression_spawn_timer = 0; expression_spawn_delay = max(25, 100 - (difficulty_level * 18)); expression_positions = [settings.SCREEN_WIDTH * i // 6 for i in range(1, 6)]; back_button_rect = pygame.Rect(20, settings.SCREEN_HEIGHT - 55, 100, 40)

    # --- Pause Screen Button Rects (defined once) ---
    # We need these rects available in the main loop to pass to handle_pause_click
    pause_resume_rect = pygame.Rect(0, 0, 200, 50)
    pause_resume_rect.center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)
    pause_menu_rect = pygame.Rect(0, 0, 200, 50)
    pause_menu_rect.center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 70)
    # --- End Pause Screen Button Rects ---


    # Main Game Loop
    running = True
    while running:
        dt = clock.tick(settings.FPS) / 1000.0 # Delta time

        # Time/Score Check
        if not paused:
            effective_elapsed_time = time.time() - start_time - total_paused_time
            time_left = settings.TIME_LIMIT_SECONDS - effective_elapsed_time
            if time_left <= 0: time_left = 0; game_over = True; game_over_reason = "Time Up"; running = False # Translated
            if not game_over and current_score < settings.GAME_OVER_SCORE_THRESHOLD: game_over = True; game_over_reason = f"Insufficient Coins ({settings.GAME_OVER_SCORE_THRESHOLD} required)"; running = False # Translated
        else: # Update time left display even when paused
            effective_elapsed_time = pause_start_time - start_time - total_paused_time
            time_left = settings.TIME_LIMIT_SECONDS - effective_elapsed_time
            if time_left < 0: time_left = 0


        # Event Handling
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

            # Keyboard Events
            if event.type == pygame.KEYDOWN:
                # Pause/Resume
                if event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        pause_start_time = time.time();
                        if game_music_playing and pygame.mixer.music.get_busy(): pygame.mixer.music.pause()
                        print("DEBUG: Game Paused.")
                    else:
                        if pause_start_time > 0: total_paused_time += time.time() - pause_start_time; pause_start_time = 0;
                        if game_music_playing: pygame.mixer.music.unpause()
                        print("DEBUG: Game Resumed.")
                # ESC in Pause Menu
                elif event.key == pygame.K_ESCAPE and paused: # Check if paused!
                    game_over_reason = settings.ACTION_RETURN_TO_MENU
                    running = False
                    print("DEBUG: ESC pressed in Pause Menu, returning.")

            # Mouse Click Events (In-Game Back Button Only)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not paused:
                 if back_button_rect.collidepoint(event.pos):
                     game_over_reason = settings.ACTION_RETURN_TO_MENU; running = False;
                     print("DEBUG: Back button clicked in game.")
                     pygame.time.delay(150)

        # Pause Screen Logic & Event Handling
        if paused:
            # Draw the pause screen visuals (overlay, text, buttons)
            # ui.draw_pause_screen now returns the button rects, but we defined them above
            ui.draw_pause_screen(screen, game_font_large, game_font_medium)

            # Handle events specific to the pause screen
            for event in events: # Use the already fetched events
                 if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                      # Pass click position and button rects to the handler function
                      action = ui.handle_pause_click(event.pos, pause_resume_rect, pause_menu_rect)
                      if action == "resume":
                           paused = False;
                           if pause_start_time > 0: total_paused_time += time.time() - pause_start_time; pause_start_time = 0;
                           if game_music_playing: pygame.mixer.music.unpause()
                           print("DEBUG: Resume button clicked.")
                           pygame.time.delay(150)
                           break # Handled this event
                      elif action == "menu":
                           game_over_reason = settings.ACTION_RETURN_TO_MENU; running = False;
                           print("DEBUG: Menu button clicked in pause.")
                           pygame.time.delay(150)
                           break # Handled this event
                 elif event.type == pygame.KEYDOWN: # Also check ESC key here
                      if event.key == pygame.K_ESCAPE:
                            game_over_reason = settings.ACTION_RETURN_TO_MENU; running = False;
                            print("DEBUG: ESC pressed in Pause Menu (handled in pause block).")
                            break # Handled this event

            pygame.display.flip(); continue # Show pause screen and skip rest of loop

        # --- Game Continues ---
        keys = pygame.key.get_pressed()

        # Scroll Background
        scroll_far = bg_speed * settings.BACKGROUND_LAYER_FAR_SPEED_MULTIPLIER; scroll_mid = bg_speed * settings.BACKGROUND_LAYER_MID_SPEED_MULTIPLIER; scroll_near = bg_speed * settings.BACKGROUND_LAYER_NEAR_SPEED_MULTIPLIER
        if bg_far_img and bg_far_h > 0: bg_far_y1 += scroll_far; bg_far_y2 += scroll_far; 
        if bg_far_y1 >= bg_far_h: bg_far_y1 = bg_far_y2 - bg_far_h; 
        if bg_far_y2 >= bg_far_h: bg_far_y2 = bg_far_y1 - bg_far_h
        if bg_mid_img and bg_mid_h > 0: bg_mid_y1 += scroll_mid; bg_mid_y2 += scroll_mid; 
        if bg_mid_y1 >= bg_mid_h: bg_mid_y1 = bg_mid_y2 - bg_mid_h; 
        if bg_mid_y2 >= bg_mid_h: bg_mid_y2 = bg_mid_y1 - bg_mid_h
        if bg_near_img and bg_near_h > 0: bg_near_y1 += scroll_near; bg_near_y2 += scroll_near; 
        if bg_near_y1 >= bg_near_h: bg_near_y1 = bg_near_y2 - bg_near_h; 
        if bg_near_y2 >= bg_near_h: bg_near_y2 = bg_near_y1 - bg_near_h

        # --- Drawing ---
        # 1. Background
        screen.fill(settings.INDIGO);
        if bg_far_img: screen.blit(bg_far_img, (0, int(bg_far_y1))); screen.blit(bg_far_img, (0, int(bg_far_y2)))
        if bg_mid_img: screen.blit(bg_mid_img, (0, int(bg_mid_y1))); screen.blit(bg_mid_img, (0, int(bg_mid_y2)))
        if bg_near_img: screen.blit(bg_near_img, (0, int(bg_near_y1))); screen.blit(bg_near_img, (0, int(bg_near_y2)))

        # 2. Spawn Expressions
        expression_spawn_timer += 1
        if expression_spawn_timer >= expression_spawn_delay:
             expression_spawn_timer = 0; num_to_spawn = random.randint(1, min(2, len(expression_positions))); current_positions = random.sample(expression_positions, num_to_spawn)
             for pos in current_positions:
                 expr_text, op, oper = eh.generate_expression(level_config)
                 if game_font_small: new_expression = Expression(expr_text, op, oper, game_font_small, pos); all_sprites.add(new_expression); expressions_group.add(new_expression)

        # 3. Update Sprites
        all_sprites.update(keys, dt)

        # 4. Collision Detection
        collided_expressions = pygame.sprite.spritecollide(player, expressions_group, True)
        for expr in collided_expressions:
            op = expr.operator; val = expr.operand; old_score = current_score
            try: # Score calculation... (Improved safety)
                if op == '+': current_score += val
                elif op == '-': current_score -= val
                elif op == '*': current_score *= val
                elif op == '/':
                    if val is not None and val != 0: current_score = int(current_score / val)
                    else: print(f"Warning: Division by zero/None attempted. Score kept."); current_score = old_score
                elif op == '**':
                    
                    current_score = current_score ** val # More reasonable limit
                            
                elif op == 'sqrt':
                    if current_score >= 0: current_score = int(math.sqrt(current_score))
                    else: print("Warning: Cannot take sqrt of negative. Score set to 0."); current_score = 0
            except Exception as e: print(f"Error: Score calculation failed ('{expr.text}'): {e}"); current_score = old_score

        # 5. Draw Sprites & UI
        expressions_group.draw(screen)
        screen.blit(player.image, player.rect)
        score_surf = game_font_medium.render(f"Coins: {current_score}", True, settings.COLOR_TEXT_LIGHT); screen.blit(score_surf, (20, 15)) # "Coins"
        time_surf = game_font_medium.render(f"Time: {int(time_left)}s", True, settings.COLOR_TEXT_LIGHT); time_rect = time_surf.get_rect(topright=(settings.SCREEN_WIDTH - 20, 15)); screen.blit(time_surf, time_rect) # "Time"
        hover_back = ui.draw_button(screen, "Back", back_button_rect, settings.COLOR_ACCENT_NEGATIVE, settings.COLOR_PRIMARY_HOVER, game_font_small) # "Back"

        # 6. Flip Display
        pygame.display.flip()

    # --- After Game Loop Ends ---
    if game_music_playing and pygame.mixer.music.get_busy(): pygame.mixer.music.fadeout(500)
    print(f"DEBUG: Game loop ended. Reason: {game_over_reason}, Score: {current_score}")
    pygame.time.wait(200)
    return current_score, game_over_reason