# ui.py 

import pygame
import json # To save/load high scores and preferences
import os   # To manage file paths
import sys  # To exit the game
import random # Can be used for random UI elements if needed
import time # For short delays after button clicks
import settings # For settings like colors, dimensions, and state names

# --- Helper UI Functions ---

def draw_gradient_background(screen, top_color, bottom_color):
    """Fills the screen with a vertical color gradient from top to bottom."""
    height = settings.SCREEN_HEIGHT
    width = settings.SCREEN_WIDTH
    for y in range(height):
        ratio = y / height
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (width, y))

def draw_text(screen, text, font, color, center_pos, antialias=True):
    """Draws text centered at a specific position."""
    try:
        text_surface = font.render(text, antialias, color)
        text_rect = text_surface.get_rect(center=center_pos)
        screen.blit(text_surface, text_rect)
    except Exception as e:
        print(f"Error: Failed to draw text ('{text}') - {e}")

def draw_button(screen, text, rect, idle_color, hover_color, font, action=None, text_color=settings.COLOR_TEXT_LIGHT, border_radius=8, border_color=None, border_width=2):
    """Draws a button and returns True if the mouse is hovering over it."""
    mouse_pos = pygame.mouse.get_pos()
    is_hovering = rect.collidepoint(mouse_pos)
    current_color = hover_color if is_hovering else idle_color
    try:
        pygame.draw.rect(screen, current_color, rect, border_radius=border_radius)
        if border_color:
            pygame.draw.rect(screen, border_color, rect, border_width, border_radius=border_radius)
        draw_text(screen, text, font, text_color, rect.center)
    except Exception as e:
        print(f"Error: Failed to draw button ('{text}') - {e}")
    return is_hovering

# --- TextInputBox Class ---
class TextInputBox:
    """A simple text input box for Pygame."""
    def __init__(self, x, y, w, h, font, max_len=12, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = settings.COLOR_SECONDARY
        self.color_active = settings.COLOR_TEXT_LIGHT
        self.border_color_active = settings.COLOR_PRIMARY
        self.border_color_inactive = settings.COLOR_SECONDARY
        self.text_color = settings.COLOR_TEXT_INPUT
        self.color = self.color_inactive
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, self.text_color)
        self.active = False
        self.max_length = max_len
        self.cursor_visible = True
        self.cursor_timer = 0
        self.padding = 10

    def handle_event(self, event):
        """Handles user input events for the text box."""
        action = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
            self.cursor_visible = self.active
            self.cursor_timer = 0
        if event.type == pygame.KEYDOWN and self.active:
            self.cursor_visible = True
            self.cursor_timer = 0
            if event.key == pygame.K_RETURN:
                if self.text.strip():
                    action = "submit"
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < self.max_length:
                # Consider allowing only ASCII or basic Latin characters if Turkish is not needed
                # allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
                allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-ğüşıöçĞÜŞİÖÇ " # Keeping Turkish for now
                if event.unicode in allowed:
                    self.text += event.unicode
            try:
                self.txt_surface = self.font.render(self.text, True, self.text_color)
            except Exception as e:
                print(f"Error: Could not render textbox text: {e}")
                self.txt_surface = self.font.render("?", True, settings.COLOR_ACCENT_NEGATIVE)
        return action

    def update(self, dt):
        """Updates the cursor blinking."""
        if self.active:
            self.cursor_timer += dt
            if self.cursor_timer >= 0.5:
                self.cursor_timer = 0
                self.cursor_visible = not self.cursor_visible

    def draw(self, screen):
        """Draws the text box on the screen."""
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        text_y = self.rect.y + (self.rect.height - self.txt_surface.get_height()) // 2
        screen.blit(self.txt_surface, (self.rect.x + self.padding, text_y))
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + self.padding + self.txt_surface.get_width()
            if cursor_x < self.rect.right - self.padding // 2:
                cursor_y_start = self.rect.y + self.padding // 2
                cursor_y_end = self.rect.y + self.rect.height - self.padding // 2
                pygame.draw.line(screen, self.text_color, (cursor_x + 1, cursor_y_start), (cursor_x + 1, cursor_y_end), 2)
        border_c = self.border_color_active if self.active else self.border_color_inactive
        pygame.draw.rect(screen, border_c, self.rect, 2, border_radius=5)

# --- Screen Drawing Functions ---

def draw_intro_screen(screen, font_title, font_button, events): # Takes events now
    """Draws the intro screen (Main Menu) and handles button clicks."""
    draw_gradient_background(screen, settings.COLOR_BACKGROUND_MENU_TOP, settings.COLOR_BACKGROUND_MENU_BOTTOM)
    draw_text(screen, "MathRisk", font_title, settings.COLOR_TEXT_DARK, (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 4))
    bw, bh = 260, 55; center_x = settings.SCREEN_WIDTH // 2
    play_rect = pygame.Rect(0, 0, bw, bh); play_rect.center = (center_x, settings.SCREEN_HEIGHT // 2)
    rules_rect = pygame.Rect(0, 0, bw, bh); rules_rect.center = (center_x, settings.SCREEN_HEIGHT // 2 + 75)
    scores_rect = pygame.Rect(0, 0, bw, bh); scores_rect.center = (center_x, settings.SCREEN_HEIGHT // 2 + 150)
    quit_rect = pygame.Rect(0, 0, bw, bh); quit_rect.center = (center_x, settings.SCREEN_HEIGHT // 2 + 225)
    # Get hover state for drawing
    mouse_pos = pygame.mouse.get_pos()
    hover_play = play_rect.collidepoint(mouse_pos)
    hover_rules = rules_rect.collidepoint(mouse_pos)
    hover_scores = scores_rect.collidepoint(mouse_pos)
    hover_quit = quit_rect.collidepoint(mouse_pos)
    # Draw buttons
    draw_button(screen, "Start", play_rect, settings.COLOR_PRIMARY, settings.COLOR_PRIMARY_HOVER, font_button)  
    draw_button(screen, "Rules", rules_rect, settings.COLOR_PRIMARY, settings.COLOR_PRIMARY_HOVER, font_button)  
    draw_button(screen, "High Scores", scores_rect, settings.COLOR_PRIMARY, settings.COLOR_PRIMARY_HOVER, font_button)  
    draw_button(screen, "Exit", quit_rect, settings.COLOR_ACCENT_NEGATIVE, settings.COLOR_PRIMARY_HOVER, font_button)  
    # Handle clicks using events
    action = None
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if hover_play and play_rect.collidepoint(event.pos): action = settings.STATE_GET_NICKNAME
            elif hover_rules and rules_rect.collidepoint(event.pos): action = settings.STATE_RULES
            elif hover_scores and scores_rect.collidepoint(event.pos): action = settings.STATE_HIGH_SCORES
            elif hover_quit and quit_rect.collidepoint(event.pos): pygame.quit(); sys.exit()
            if action: pygame.time.delay(150); break
    return action

def draw_nickname_screen(screen, font_title,font_small_title, font_normal, nickname_box, events): # Takes events now
    """Draws the nickname input screen and handles button clicks."""
    draw_gradient_background(screen, settings.COLOR_BACKGROUND_MENU_TOP, settings.COLOR_BACKGROUND_MENU_BOTTOM)
    text_line1 = "Enter your nickname"
    text_line2 = "and press Enter" # Metni uygun bir yerden böldük

    center_x = settings.SCREEN_WIDTH // 2
    base_y = settings.SCREEN_HEIGHT // 4 # İki satırın ortalanacağı temel Y noktası
    line_height = font_title.get_height() # Kullanılan fontun yüksekliği
    spacing = 10 # İki satır arasındaki boşluk (piksel)

    # İlk satırın Y merkezini hesapla (base_y'nin biraz üzeri)
    y1 = base_y - line_height // 2 - spacing // 2
    # İkinci satırın Y merkezini hesapla (base_y'nin biraz altı)
    y2 = base_y + line_height // 2 + spacing // 2

    # İki satırı ayrı ayrı çiz
    draw_text(screen, text_line1, font_small_title, settings.COLOR_TEXT_DARK, (center_x, y1))
    draw_text(screen, text_line2, font_small_title, settings.COLOR_TEXT_DARK, (center_x, y2))    
    nickname_box.draw(screen); nickname_box.update(1/settings.FPS)
    bw, bh = 200, 50; bbw, bbh = 120, 45
    cont_rect = pygame.Rect(0, 0, bw, bh); cont_rect.center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 120)
    back_rect = pygame.Rect(30, settings.SCREEN_HEIGHT - 70, bbw, bbh)
    can_continue = bool(nickname_box.text.strip())
    continue_idle_color = settings.COLOR_PRIMARY if can_continue else settings.COLOR_SECONDARY
    continue_hover_color = settings.COLOR_PRIMARY_HOVER if can_continue else settings.COLOR_SECONDARY
    # Get hover state for drawing
    mouse_pos = pygame.mouse.get_pos()
    hover_cont = cont_rect.collidepoint(mouse_pos)
    hover_back = back_rect.collidepoint(mouse_pos)
    # Draw buttons
    #draw_button(screen, "Continue", cont_rect, continue_idle_color, continue_hover_color, font_normal)  
    draw_button(screen, "Back", back_rect, settings.COLOR_ACCENT_NEGATIVE, settings.COLOR_PRIMARY_HOVER, font_normal) 
    # Handle clicks using events
    action = None
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if hover_cont and can_continue and cont_rect.collidepoint(event.pos): action = settings.STATE_AVATAR_SELECT
            elif hover_back and back_rect.collidepoint(event.pos): action = settings.STATE_INTRO
            if action: pygame.time.delay(150); break
    return action

def draw_avatar_screen(screen, font_title, font_normal, font_button, avatars, selected_avatar_index, events): # Takes events now
    """Draws the avatar selection screen and handles clicks using events."""
    draw_gradient_background(screen, settings.COLOR_BACKGROUND_MENU_TOP, settings.COLOR_BACKGROUND_MENU_BOTTOM)
    draw_text(screen, "Select Avatar", font_title, settings.COLOR_TEXT_DARK, (settings.SCREEN_WIDTH // 2, 80)) 

    action = None
    new_selection = selected_avatar_index
    mouse_pos = pygame.mouse.get_pos() # For hover

    if not avatars:
        draw_text(screen, "No static avatars found!", font_normal, settings.COLOR_ACCENT_NEGATIVE, (settings.SCREEN_WIDTH // 2, 200))
        draw_text(screen, f"Check the 'assets/images/avatars' folder.", font_normal, settings.COLOR_TEXT_DARK, (settings.SCREEN_WIDTH // 2, 250))  
        bbw, bbh = 120, 45; back_rect = pygame.Rect(30, settings.SCREEN_HEIGHT - 70, bbw, bbh)
        hover_back = draw_button(screen, "Back", back_rect, settings.COLOR_ACCENT_NEGATIVE, settings.COLOR_PRIMARY_HOVER, font_button) 
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                 if hover_back and back_rect.collidepoint(event.pos):
                      action = settings.STATE_GET_NICKNAME; pygame.time.delay(150); break
        return action, new_selection

    avatar_width = settings.PLAYER_AVATAR_SIZE[0]; avatar_height = settings.PLAYER_AVATAR_SIZE[1]
    padding = 25; cols = 4
    total_w = cols * (avatar_width + padding) - padding; start_x = max(50, (settings.SCREEN_WIDTH - total_w) // 2); start_y = 160
    avatar_clickable_rects = {}

    # Draw Avatars and calculate clickable rects
    col_count, row_count = 0, 0
    for i, img in enumerate(avatars):
         x = start_x + col_count * (avatar_width + padding); y = start_y + row_count * (avatar_height + padding + 15)
         draw_rect = pygame.Rect(x, y, avatar_width, avatar_height)
         avatar_clickable_rects[i] = draw_rect # Store rect for click detection
         try:
             scaled_img = pygame.transform.scale(img, settings.PLAYER_AVATAR_SIZE)
             is_selected = (i == selected_avatar_index)
             alpha = 255 if is_selected else 180
             scaled_img.set_alpha(alpha); screen.blit(scaled_img, draw_rect)
             if is_selected: pygame.draw.rect(screen, settings.COLOR_HIGHLIGHT, draw_rect, 5, border_radius=10)
         except Exception as e: print(f"Error: Static avatar {i} rendering failed: {e}")
         col_count += 1;
         if col_count >= cols: col_count = 0; row_count += 1

    # Draw Buttons
    bw, bh = 200, 50; bbw, bbh = 120, 45
    cont_rect = pygame.Rect(settings.SCREEN_WIDTH - bw - 30, settings.SCREEN_HEIGHT - 70, bw, bh)
    back_rect = pygame.Rect(30, settings.SCREEN_HEIGHT - 70, bbw, bbh)
    hover_cont = draw_button(screen, "Continue", cont_rect, settings.COLOR_PRIMARY, settings.COLOR_PRIMARY_HOVER, font_button)  
    hover_back = draw_button(screen, "Back", back_rect, settings.COLOR_ACCENT_NEGATIVE, settings.COLOR_PRIMARY_HOVER, font_button)  

    # Handle Clicks using events
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_pos = event.pos
            clicked_on_item = False
            # 1. Check Avatar Clicks
            for index, click_rect in avatar_clickable_rects.items():
                if click_rect.collidepoint(click_pos):
                    new_selection = index
                    clicked_on_item = True
                    # print(f"DEBUG: Avatar {index} clicked (event), new selection: {new_selection}") # Debug
                    break
            # 2. Check Button Clicks (if avatar wasn't clicked)
            if not clicked_on_item:
                if hover_cont and cont_rect.collidepoint(click_pos):
                    action = settings.STATE_DIFFICULTY_SELECT
                    clicked_on_item = True
                elif hover_back and back_rect.collidepoint(click_pos):
                    action = settings.STATE_GET_NICKNAME
                    clicked_on_item = True
            # Delay only if a button was clicked (action is set)
            if action:
                pygame.time.delay(150)
                break # Exit event loop for this frame if a button was clicked

    return action, new_selection

def draw_difficulty_screen(screen, font_title, font_button, levels_dict, current_selection, events): # Takes events now
    """Draws the difficulty selection screen and handles clicks."""
    draw_gradient_background(screen, settings.COLOR_BACKGROUND_MENU_TOP, settings.COLOR_BACKGROUND_MENU_BOTTOM)
    draw_text(screen, "Select Difficulty", font_title, settings.COLOR_TEXT_DARK, (settings.SCREEN_WIDTH // 2, 120))  
    bw, bh = 250, 60; start_y = 220; spacing = 90; center_x = settings.SCREEN_WIDTH // 2
    level_buttons = {}; hover_levels = {}
    mouse_pos = pygame.mouse.get_pos() # For hover
    for num, config in levels_dict.items():
        rect = pygame.Rect(0, 0, bw, bh); rect.center = (center_x, start_y + (num - 1) * spacing); level_buttons[num] = rect
        idle = settings.COLOR_PRIMARY if num == current_selection else settings.COLOR_SECONDARY; hover = settings.COLOR_PRIMARY_HOVER; text = settings.COLOR_TEXT_LIGHT; border = settings.COLOR_HIGHLIGHT if num == current_selection else None
        # Use config['name'] which should be translated in settings.py
        hover_levels[num] = draw_button(screen, config['name'], rect, idle, hover, font_button, text_color=text, border_color=border, border_width=3)
    bbw, bbh = 120, 45; back_rect = pygame.Rect(30, settings.SCREEN_HEIGHT - 70, bbw, bbh)
    hover_back = draw_button(screen, "Back", back_rect, settings.COLOR_ACCENT_NEGATIVE, settings.COLOR_PRIMARY_HOVER, font_button)  
    # Handle clicks using events
    action = None
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked_on_level = False
            for num, rect in level_buttons.items():
                # Check collision with event.pos, not mouse_pos for click reliability
                if hover_levels[num] and rect.collidepoint(event.pos):
                    action = num; clicked_on_level = True; break
            if not clicked_on_level:
                # Check collision with event.pos
                if hover_back and back_rect.collidepoint(event.pos):
                    action = settings.STATE_AVATAR_SELECT
            if action is not None: pygame.time.delay(150); break
    return action

def draw_game_over_screen(screen, font_title, font_normal, font_button, final_score, reason, is_new_high_score, events): # Takes events now
    """Draws the Game Over screen."""
    screen.fill(settings.COLOR_ACCENT_NEGATIVE);
    draw_text(screen, "Game Over!", font_title, settings.COLOR_TEXT_LIGHT, (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 4))  
    reason_text = reason
    # Translate specific reasons if needed
    if reason == settings.ACTION_RETURN_TO_MENU: reason_text = "Returned to Menu"  
    elif reason == "Süre Doldu": reason_text = "Time Up" # Example translation
    elif "Coin Yetersiz" in reason: reason_text = "Insufficient Coins" # Example translation
    draw_text(screen, f"Reason: {reason_text}", font_normal, settings.COLOR_TEXT_LIGHT, (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 - 40)) 
    draw_text(screen, f"Final Score: {final_score}", font_normal, settings.COLOR_TEXT_LIGHT, (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 10)) 
    message_y_offset = 60
    if is_new_high_score:
        msg_font = font_normal; msg_color = settings.COLOR_HIGHLIGHT; msg_pos = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + message_y_offset);
        draw_text(screen, "NEW HIGH SCORE!", msg_font, msg_color, msg_pos);  
        message_y_offset += 40
    button_y_base = settings.SCREEN_HEIGHT * 3 // 4 + message_y_offset // 2; bw, bh = 280, 45
    menu_rect = pygame.Rect(0, 0, bw, bh); menu_rect.center = (settings.SCREEN_WIDTH // 2, button_y_base)
    scores_rect = pygame.Rect(0, 0, bw, bh); scores_rect.center = (settings.SCREEN_WIDTH // 2, button_y_base + 75)
    # Get hover state
    mouse_pos = pygame.mouse.get_pos()
    hover_menu = menu_rect.collidepoint(mouse_pos)
    hover_scores = scores_rect.collidepoint(mouse_pos)
    # Draw buttons
    draw_button(screen, "Main Menu", menu_rect, settings.COLOR_PRIMARY, settings.COLOR_PRIMARY_HOVER, font_button)  
    draw_button(screen, "High Scores", scores_rect, settings.COLOR_PRIMARY, settings.COLOR_PRIMARY_HOVER, font_button)  
    # Handle clicks
    action = None
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
             if hover_menu and menu_rect.collidepoint(event.pos): action = settings.STATE_INTRO
             elif hover_scores and scores_rect.collidepoint(event.pos): action = settings.STATE_HIGH_SCORES
             if action: pygame.time.delay(150); break
    return action

def draw_high_scores_screen(screen, font_title, font_normal, font_button, high_scores, events):
    """Draws the high scores screen (top 5, aligned left/right)."""
    draw_gradient_background(screen, settings.COLOR_BACKGROUND_MENU_TOP, settings.COLOR_BACKGROUND_MENU_BOTTOM)
    draw_text(screen, "High Scores", font_title, settings.COLOR_TEXT_DARK, (settings.SCREEN_WIDTH // 2, 100))

    if not high_scores:
        draw_text(screen, "No scores recorded yet.", font_normal, settings.COLOR_TEXT_DARK, (settings.SCREEN_WIDTH // 2, 250))
    else:
        y = 180
        line_height = 45

        # --- HİZALAMA İÇİN X KOORDİNATLARI (Ayarlanabilir) ---
        # Ekranın solundan ne kadar içeride başlayacağı (padding)
        left_margin = 150
        # Ekranın sağından ne kadar içeride biteceği (padding)
        right_margin = 150

        # Sıra numarasının SAĞ kenarı için X koordinatı
        rank_align_x = left_margin + 40 # Sol marjinden biraz içeride

        # İsmin SOL kenarı için X koordinatı
        name_align_x = rank_align_x + 20 # Sıradan biraz sağda

        # Skorun SAĞ kenarı için X koordinatı
        score_align_x = settings.SCREEN_WIDTH - right_margin # Sağ marjinin hizası
        # --- Bitti: X Koordinatları ---

        for i, entry in enumerate(high_scores[:5]):
           nick = entry.get('nickname', '?')
           score = entry.get('score', 0)
           color = settings.COLOR_PRIMARY if i == 0 else settings.COLOR_TEXT_DARK

           # --- Ayrı Render ve Hizalı Blit ---
           try:
              # 1. Sıra (Sağa Hizalı)
              rank_surf = font_normal.render(f"{i+1}.", True, color)
              rank_rect = rank_surf.get_rect()
              # topright özelliği ile sağ kenarı hizala
              rank_rect.topright = (rank_align_x, y)
              # Y ekseninde dikeyde ortalamak için manuel ayar (opsiyonel ama daha iyi görünür)
              rank_rect.centery = y # Satırın dikey merkezi
              screen.blit(rank_surf, rank_rect)

              # 2. İsim (Sola Hizalı)
              # Uzun isim kısaltma (aynı kalabilir)
              max_name_width = score_align_x - name_align_x - 30 # Skorla çakışmaması için
              name_surf = font_normal.render(nick, True, color)
              name_rect = name_surf.get_rect()
              if name_rect.width > max_name_width:
                 temp_nick = nick;
                 while font_normal.size(temp_nick + '..')[0] > max_name_width and len(temp_nick) > 1: temp_nick = temp_nick[:-1];
                 nick_display = temp_nick + '..' if len(temp_nick) < len(nick) else nick;
                 name_surf = font_normal.render(nick_display, True, color);
                 name_rect = name_surf.get_rect()
              # topleft özelliği ile sol kenarı hizala
              name_rect.topleft = (name_align_x, y)
              name_rect.centery = y # Dikeyde ortala
              screen.blit(name_surf, name_rect)

              # 3. Skor (Sağa Hizalı)
              score_surf = font_normal.render(str(score), True, color)
              score_rect = score_surf.get_rect()
              # topright özelliği ile sağ kenarı hizala
              score_rect.topright = (score_align_x, y)
              score_rect.centery = y # Dikeyde ortala
              screen.blit(score_surf, score_rect)

           except Exception as e:
              print(f"Error: High score row rendering failed: {e}")
              text = f"{i+1}. {nick} - {score}" # Hata durumunda eski yöntem
              draw_text(screen, text, font_normal, settings.COLOR_ACCENT_NEGATIVE, (settings.SCREEN_WIDTH // 2, y))
           # --- Bitti: Ayrı Render ve Hizalı Blit ---

           y += line_height # Sonraki satıra geç

    # Ana Menü Butonu (Aynı)
    bw, bh = 200, 50; menu_rect = pygame.Rect(0, 0, bw, bh); menu_rect.center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 80)
    mouse_pos = pygame.mouse.get_pos(); hover_menu = draw_button(screen, "Main Menu", menu_rect, settings.COLOR_PRIMARY, settings.COLOR_PRIMARY_HOVER, font_button)
    action = None
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
          if hover_menu and menu_rect.collidepoint(event.pos): action = settings.STATE_INTRO; pygame.time.delay(150); break
    return action



def draw_rules_screen(screen, font_title, font_normal, font_button, events): # Takes events now
    """Draws the game rules screen."""
    draw_gradient_background(screen, settings.COLOR_BACKGROUND_MENU_TOP, settings.COLOR_BACKGROUND_DARK)
    draw_text(screen, "How to Play?", font_title, settings.COLOR_TEXT_DARK, (settings.SCREEN_WIDTH // 2, 80))  

   
    rules = [
       "Catch the falling mathematical expressions",
       "in colored shapes to maximize your score!",
       "Move the character using",
        "LEFT and RIGHT arrow keys.",
       "The character floats up and down while moving!",
       "(+) Addition, (-) Subtraction, (*) Multiplication",
       "(/) Division, (^) Exponentiation, (√) Square Root",
       f"The game ends when time runs out or",
       f"your score falls below {settings.GAME_OVER_SCORE_THRESHOLD}.",
       "Press 'P' to pause/resume the game.",
       "Press 'ESC' while paused to",
        "return to the main menu.",
       "Have Fun!"
    ]

    rule_y_start = 160; line_height = 27
    current_y = rule_y_start;
    for rule in rules:
        if not rule: current_y += line_height * 0.5; continue
        draw_text(screen, rule, font_normal, settings.COLOR_TEXT_LIGHT, (settings.SCREEN_WIDTH // 2, current_y)); current_y += line_height
    bbw, bbh = 200, 45; back_rect = pygame.Rect(0, 0, bbw, bbh); back_rect.center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 70)
    # Get hover state
    mouse_pos = pygame.mouse.get_pos()
    hover_back = draw_button(screen, "Main Menu", back_rect, settings.COLOR_PRIMARY, settings.COLOR_PRIMARY_HOVER, font_button)  
    # Handle clicks
    action = None
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if hover_back and back_rect.collidepoint(event.pos): action = settings.STATE_INTRO; pygame.time.delay(150); break
    return action

# --- Data Management ---

def load_json_data(filepath, default_value):
    """Reads a JSON file, returns default value on error."""
    if not os.path.exists(filepath):
        # print(f"Info: JSON file not found: {filepath}. Using default.") # Less verbose
        return default_value
    try:
        with open(filepath, 'r', encoding='utf-8') as f: return json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        print(f"Error: Reading JSON {os.path.basename(filepath)}: {e}")  
        return default_value

def save_json_data(filepath, data):
    """Writes data to a JSON file."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error: Writing JSON {os.path.basename(filepath)}: {e}")  

def load_high_scores():
    """Loads high scores from file."""
    # print("DEBUG: Loading high scores...") # Keep debug optional
    return load_json_data(settings.HIGH_SCORES_FILE, [])

def save_high_scores(scores):
    """Saves high scores to file."""
    # print("DEBUG: Saving high scores...") # Keep debug optional
    save_json_data(settings.HIGH_SCORES_FILE, scores)

def add_high_score(nickname, score, scores_list, max_scores=5): # Keep limit 5
    """Adds a score to the list, sorts, and trims it."""
    try: current_score = int(score);
    except ValueError: print(f"Warning: Invalid score '{score}' not added."); return scores_list 
    if current_score <= 0: return scores_list
    current_nickname = str(nickname).strip();
    if not current_nickname: current_nickname = "Unknown"  
    scores_list.append({'nickname': current_nickname, 'score': current_score})
    scores_list.sort(key=lambda x: x.get('score', 0), reverse=True)
    return scores_list[:max_scores]

def load_user_prefs():
    """Loads user preferences from file."""
    # print("DEBUG: Loading user preferences...") # Keep debug optional
    defaults = {'nickname': '', 'avatar_index': 0, 'difficulty': 1}
    prefs = load_json_data(settings.USER_PREFS_FILE, defaults.copy())
    updated = False
    for key, value in defaults.items():
        if key not in prefs: prefs[key] = value; updated = True
    try: prefs['avatar_index'] = int(prefs.get('avatar_index', 0))
    except (ValueError, TypeError): prefs['avatar_index'] = 0; updated = True
    try: prefs['difficulty'] = int(prefs.get('difficulty', 1))
    except (ValueError, TypeError): prefs['difficulty'] = 1; updated = True
    # if updated: save_user_prefs(prefs) # Optionally save if defaults were added
    return prefs

def save_user_prefs(prefs):
    """Saves user preferences to file."""
    # print("DEBUG: Saving user preferences...") # Keep debug optional
    to_save = {
        'nickname': str(prefs.get('nickname', '')).strip()[:settings.NICKNAME_MAX_LENGTH],
        'avatar_index': int(prefs.get('avatar_index', 0)),
        'difficulty': int(prefs.get('difficulty', 1))
    }
    save_json_data(settings.USER_PREFS_FILE, to_save)

# --- Pause Screen Specific Functions (Moved from game.py for better organization) ---

def draw_pause_screen(screen, font_large, font_medium):
    """Draws the pause screen overlay and buttons."""
    # Draw dimming overlay
    pause_surface = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
    pause_surface.fill(settings.PAUSE_OVERLAY_COLOR)
    screen.blit(pause_surface, (0, 0))
    # Draw "PAUSED" text
    draw_text(screen, "PAUSED", font_large, settings.COLOR_TEXT_LIGHT,
              (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 3))
    # Define button rects
    resume_rect = pygame.Rect(0, 0, 250, 50)
    resume_rect.center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)
    menu_rect = pygame.Rect(0, 0, 250, 50)
    menu_rect.center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 70)
    # Draw buttons and return their rects (needed for click handling)
    draw_button(screen, "Resume (P)", resume_rect, settings.COLOR_ACCENT_POSITIVE, settings.COLOR_PRIMARY_HOVER, font_medium)  
    draw_button(screen, "Main Menu (ESC)", menu_rect, settings.COLOR_ACCENT_NEGATIVE, settings.COLOR_PRIMARY_HOVER, font_medium)  
    # Return the rects for click detection in the main game loop
    return resume_rect, menu_rect

def handle_pause_click(click_pos, resume_rect, menu_rect):
    """Checks if the click position hits the pause screen buttons."""
    if resume_rect.collidepoint(click_pos):
        return "resume"
    elif menu_rect.collidepoint(click_pos):
        return "menu"
    return None # Clicked elsewhere on the pause screen