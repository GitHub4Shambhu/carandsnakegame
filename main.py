import pygame
import os
import math
import random  # Add missing random import

class Game:
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GRAY = (128, 128, 128)
    DARK_GRAY = (50, 50, 50)
    
    # Screen dimensions
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()  # Initialize sound
        
        # Set up display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Car and Snake Game")
        
        # Set game icon
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.game_icon = pygame.image.load(os.path.join(current_dir, 'gamelogo.png'))
        pygame.display.set_icon(self.game_icon)
        
        # Load background
        self.bg_img = self.create_background()
        
        # Load fonts
        self.title_font = pygame.font.Font(None, 60)
        self.large_font = pygame.font.Font(None, 48)
        self.medium_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Load sound effects
        # self.collect_sound = pygame.mixer.Sound(os.path.join(current_dir, 'sounds', 'collect.wav'))
        # self.crash_sound = pygame.mixer.Sound(os.path.join(current_dir, 'sounds', 'crash.wav'))
        
        # Game state variables
        self.clock = pygame.time.Clock()
        self.is_running = True
        
        # Game states
        self.MENU = 0
        self.PLAYING = 1
        self.PAUSED = 2
        self.GAME_OVER = 3
        self.state = self.MENU

        # Difficulty settings
        self.DIFFICULTIES = {
            'easy': {'car_count': 20, 'snake_count': 20, 'human_count': 8, 'snake_speed': 1},
            'medium': {'car_count': 30, 'snake_count': 30, 'human_count': 6, 'snake_speed': 2},
            'hard': {'car_count': 40, 'snake_count': 40, 'human_count': 4, 'snake_speed': 3}
        }
        self.difficulty = 'medium'
    
    def create_background(self):
        # Create a patterned background (grass-like)
        bg = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        bg.fill((100, 180, 100))  # Base green
        
        # Add some random darker patches for texture
        for _ in range(500):
            x = random.randint(0, self.SCREEN_WIDTH)
            y = random.randint(0, self.SCREEN_HEIGHT)
            size = random.randint(10, 30)
            alpha = random.randint(30, 100)
            
            # Create a surface with per-pixel alpha
            s = pygame.Surface((size, size), pygame.SRCALPHA)
            s.fill((50, 120, 50, alpha))  # Semi-transparent darker green
            bg.blit(s, (x, y))
            
        return bg
    
    def draw_text(self, text, font, color, x, y, align="center"):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        
        if align == "center":
            text_rect.center = (x, y)
        elif align == "left":
            text_rect.left = x
            text_rect.centery = y
        elif align == "right":
            text_rect.right = x
            text_rect.centery = y
            
        self.screen.blit(text_surface, text_rect)
        return text_rect
    
    def draw_button(self, rect, text, font, active=False):
        # Button colors
        bg_color = self.GRAY if not active else self.DARK_GRAY
        text_color = self.WHITE
        border_color = self.BLACK
        
        # Draw button
        pygame.draw.rect(self.screen, bg_color, rect)
        pygame.draw.rect(self.screen, border_color, rect, 2)
        
        # Center text on button
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)
        
        return rect
    
    def is_button_clicked(self, rect, pos):
        return rect.collidepoint(pos)
    
    def init_game_objects(self):
        from car import Car
        from snake import Snake
        from human import Human
        from powerup import PowerUp
        
        settings = self.DIFFICULTIES[self.difficulty]
        
        # Create game objects
        self.cars = [Car(random.randint(50, self.SCREEN_WIDTH-100), 
                      random.randint(50, self.SCREEN_HEIGHT-100)) 
                   for _ in range(settings['car_count'])]
        
        self.snakes = [Snake(random.randint(50, self.SCREEN_WIDTH-100),
                          random.randint(50, self.SCREEN_HEIGHT-100))
                     for _ in range(settings['snake_count'])]
        
        # Set snake speed based on difficulty
        for snake in self.snakes:
            snake.set_speed(self.difficulty)
        
        self.humans = [Human(random.randint(50, self.SCREEN_WIDTH-100),
                          random.randint(50, self.SCREEN_HEIGHT-100))
                     for _ in range(settings['human_count'])]
        
        self.powerups = []
        self.car_angles = [random.uniform(0, 2 * math.pi) for _ in range(len(self.cars))]
        self.car_move_counters = [0 for _ in range(len(self.cars))]
        self.selected_car_index = 0
        self.car_score = 0
        self.snake_score = 0
        self.powerup_spawn_timer = 0
    
    def run(self):
        self.is_running = True
        
        while self.is_running:
            if self.state == self.MENU:
                self.handle_menu()
            elif self.state == self.PLAYING:
                self.handle_playing()
            elif self.state == self.PAUSED:
                self.handle_pause()
            elif self.state == self.GAME_OVER:
                self.handle_game_over()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
    
    def handle_menu(self):
        self.screen.blit(self.bg_img, (0, 0))
        
        # Draw title and menu items
        title_y = 100
        self.draw_text("Car and Snake Game", self.title_font, self.BLACK, self.SCREEN_WIDTH // 2, title_y)
        
        # Draw difficulty buttons
        diff_y = 250
        diff_spacing = 60
        self.draw_text("Select Difficulty:", self.medium_font, self.BLACK, self.SCREEN_WIDTH // 2, diff_y - 50)
        
        easy_rect = pygame.Rect(self.SCREEN_WIDTH // 2 - 100, diff_y, 200, 50)
        medium_rect = pygame.Rect(self.SCREEN_WIDTH // 2 - 100, diff_y + diff_spacing, 200, 50)
        hard_rect = pygame.Rect(self.SCREEN_WIDTH // 2 - 100, diff_y + 2 * diff_spacing, 200, 50)
        
        self.draw_button(easy_rect, "Easy", self.medium_font, self.difficulty == 'easy')
        self.draw_button(medium_rect, "Medium", self.medium_font, self.difficulty == 'medium')
        self.draw_button(hard_rect, "Hard", self.medium_font, self.difficulty == 'hard')
        
        # Draw start button
        start_rect = pygame.Rect(self.SCREEN_WIDTH // 2 - 120, diff_y + 3 * diff_spacing + 20, 240, 60)
        self.draw_button(start_rect, "Start Game", self.large_font)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.is_button_clicked(easy_rect, mouse_pos):
                    self.difficulty = 'easy'
                elif self.is_button_clicked(medium_rect, mouse_pos):
                    self.difficulty = 'medium'
                elif self.is_button_clicked(hard_rect, mouse_pos):
                    self.difficulty = 'hard'
                elif self.is_button_clicked(start_rect, mouse_pos):
                    self.init_game_objects()
                    self.state = self.PLAYING
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.init_game_objects()
                    self.state = self.PLAYING
                elif event.key == pygame.K_1:
                    self.difficulty = 'easy'
                elif event.key == pygame.K_2:
                    self.difficulty = 'medium'
                elif event.key == pygame.K_3:
                    self.difficulty = 'hard'
    
    def handle_playing(self):
        from powerup import PowerUp
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.state = self.PAUSED
                elif event.key == pygame.K_TAB:
                    self.selected_car_index = (self.selected_car_index + 1) % len(self.cars)
                    # Skip dead cars when cycling
                    while self.cars[self.selected_car_index].health <= 0 and any(car.health > 0 for car in self.cars):
                        self.selected_car_index = (self.selected_car_index + 1) % len(self.cars)
        
        # Handle power-up spawning
        self.powerup_spawn_timer += 1
        if self.powerup_spawn_timer >= 180:  # Spawn every 3 seconds (60 FPS * 3)
            self.powerup_spawn_timer = 0
            if len(self.powerups) < 5:  # Max 5 power-ups at once
                self.powerups.append(PowerUp.spawn_random(self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        # Handle user input for selected car
        keys = pygame.key.get_pressed()
        if self.cars[self.selected_car_index].health > 0:
            if keys[pygame.K_LEFT]: self.cars[self.selected_car_index].move(-1, 0)
            if keys[pygame.K_RIGHT]: self.cars[self.selected_car_index].move(1, 0)
            if keys[pygame.K_UP]: self.cars[self.selected_car_index].move(0, -1)
            if keys[pygame.K_DOWN]: self.cars[self.selected_car_index].move(0, 1)
        
        # Update game objects
        self.update_game_objects()
        
        # Handle collisions
        self.handle_collisions()
        
        # Draw game
        self.draw_game()
        
        # Check game over condition
        if self.cars[self.selected_car_index].health <= 0:
            self.state = self.GAME_OVER
    
    def update_game_objects(self):
        # Move cars
        for i, car in enumerate(self.cars):
            if i != self.selected_car_index and car.health > 0:
                self.car_move_counters[i] += 1
                if self.car_move_counters[i] >= 120:
                    self.car_move_counters[i] = 0
                    self.car_angles[i] = random.uniform(0, 2 * math.pi)
                dx = math.cos(self.car_angles[i])
                dy = math.sin(self.car_angles[i])
                car.move(dx, dy)
        
        # Move humans with awareness of snakes
        for human in self.humans:
            human.move(self.snakes)
        
        # Move snakes towards nearest human
        for snake in self.snakes:
            if self.humans:  # Only move if there are humans left
                nearest_human = min(self.humans, 
                                  key=lambda h: ((h.rect.x - snake.rect.x) ** 2 + 
                                              (h.rect.y - snake.rect.y) ** 2))
                snake.move_towards(nearest_human.rect.x, nearest_human.rect.y)
    
    def handle_collisions(self):
        from car import Car
        from snake import Snake
        from human import Human
        from powerup import PowerUp
        
        # Car-Snake collisions
        for i, car in enumerate(self.cars):
            if car.health <= 0:
                continue
            for snake in self.snakes:
                if car.rect.colliderect(snake.rect):
                    if car.take_damage(10):  # Only take damage if not shielded
                        # if i == self.selected_car_index and self.crash_sound:
                        #     self.crash_sound.play()
                        self.car_score += 1
                    # Respawn snake
                    snake.rect.topleft = (random.randint(0, self.SCREEN_WIDTH - snake.rect.width),
                                        random.randint(0, self.SCREEN_HEIGHT - snake.rect.height))
        
        # Snake-Human collisions
        for snake in self.snakes:
            for human in list(self.humans):  # Create a copy to safely modify
                if snake.rect.colliderect(human.rect):
                    self.snake_score += 1
                    self.humans.remove(human)
                    if not self.humans:  # If no humans left, respawn some
                        self.humans = [Human(random.randint(50, self.SCREEN_WIDTH-100),
                                          random.randint(50, self.SCREEN_HEIGHT-100))
                                    for _ in range(self.DIFFICULTIES[self.difficulty]['human_count'])]
        
        # Car-PowerUp collisions
        for powerup in list(self.powerups):
            if powerup.active and self.cars[self.selected_car_index].rect.colliderect(powerup.rect):
                self.cars[self.selected_car_index].apply_powerup(powerup.power_type)
                # if self.collect_sound:
                #     self.collect_sound.play()
                self.powerups.remove(powerup)
    
    def draw_game(self):
        # Draw background
        self.screen.blit(self.bg_img, (0, 0))
        
        # Draw HUD (scores, health, etc.)
        self.draw_hud()
        
        # Draw power-ups
        for powerup in self.powerups:
            powerup.draw(self.screen)
        
        # Draw humans
        for human in self.humans:
            human.draw(self.screen)
        
        # Draw snakes
        for snake in self.snakes:
            snake.draw(self.screen)
        
        # Draw cars
        for i, car in enumerate(self.cars):
            car.draw(self.screen)
            if i == self.selected_car_index and car.health > 0:
                # Highlight selected car
                pygame.draw.rect(self.screen, self.RED, car.rect, 2)
    
    def draw_hud(self):
        # Draw a semi-transparent HUD panel
        hud_height = 80
        s = pygame.Surface((self.SCREEN_WIDTH, hud_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(s, (0, 0))
        
        # Draw scores
        self.draw_text(f"Car Score: {self.car_score}", self.medium_font, self.WHITE, 120, 20, "left")
        self.draw_text(f"Snake Score: {self.snake_score}", self.medium_font, self.WHITE, 120, 50, "left")
        
        # Draw difficulty
        self.draw_text(f"Difficulty: {self.difficulty.upper()}", self.medium_font, self.WHITE, 
                     self.SCREEN_WIDTH // 2, 20, "center")
        
        # Draw humans left
        humans_text = f"Humans: {len(self.humans)}"
        self.draw_text(humans_text, self.medium_font, self.WHITE, self.SCREEN_WIDTH - 120, 20, "right")
        
        # Draw selected car health
        health = self.cars[self.selected_car_index].health
        health_color = self.GREEN if health > 60 else self.YELLOW if health > 30 else self.RED
        self.draw_text(f"Car Health: {health}", self.medium_font, health_color, 
                     self.SCREEN_WIDTH - 120, 50, "right")
    
    def handle_pause(self):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Draw pause menu
        self.draw_text("PAUSED", self.title_font, self.WHITE, self.SCREEN_WIDTH // 2, 150)
        
        # Create buttons
        resume_rect = pygame.Rect(self.SCREEN_WIDTH // 2 - 100, 250, 200, 50)
        restart_rect = pygame.Rect(self.SCREEN_WIDTH // 2 - 100, 320, 200, 50)
        menu_rect = pygame.Rect(self.SCREEN_WIDTH // 2 - 100, 390, 200, 50)
        
        self.draw_button(resume_rect, "Resume (P)", self.medium_font)
        self.draw_button(restart_rect, "Restart (R)", self.medium_font)
        self.draw_button(menu_rect, "Main Menu (M)", self.medium_font)
        
        # Draw keyboard shortcuts
        self.draw_text("ESC: Quit Game", self.small_font, self.WHITE, self.SCREEN_WIDTH // 2, 470)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.is_button_clicked(resume_rect, mouse_pos):
                    self.state = self.PLAYING
                elif self.is_button_clicked(restart_rect, mouse_pos):
                    self.init_game_objects()
                    self.state = self.PLAYING
                elif self.is_button_clicked(menu_rect, mouse_pos):
                    self.state = self.MENU
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.state = self.PLAYING
                elif event.key == pygame.K_r:
                    self.init_game_objects()
                    self.state = self.PLAYING
                elif event.key == pygame.K_m:
                    self.state = self.MENU
                elif event.key == pygame.K_ESCAPE:
                    self.is_running = False
    
    def handle_game_over(self):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Darker semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over message
        self.draw_text("GAME OVER", self.title_font, self.RED, self.SCREEN_WIDTH // 2, 150)
        
        # Draw scores
        score_y = 230
        self.draw_text(f"Final Car Score: {self.car_score}", self.medium_font, self.WHITE, 
                     self.SCREEN_WIDTH // 2, score_y)
        self.draw_text(f"Final Snake Score: {self.snake_score}", self.medium_font, self.WHITE, 
                     self.SCREEN_WIDTH // 2, score_y + 40)
        
        # Create buttons
        restart_rect = pygame.Rect(self.SCREEN_WIDTH // 2 - 100, 330, 200, 50)
        menu_rect = pygame.Rect(self.SCREEN_WIDTH // 2 - 100, 400, 200, 50)
        
        self.draw_button(restart_rect, "Play Again (R)", self.medium_font)
        self.draw_button(menu_rect, "Main Menu (M)", self.medium_font)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.is_button_clicked(restart_rect, mouse_pos):
                    self.init_game_objects()
                    self.state = self.PLAYING
                elif self.is_button_clicked(menu_rect, mouse_pos):
                    self.state = self.MENU
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.init_game_objects()
                    self.state = self.PLAYING
                elif event.key == pygame.K_m:
                    self.state = self.MENU
                elif event.key == pygame.K_ESCAPE:
                    self.is_running = False

# Start the game
if __name__ == "__main__":
    import random
    game = Game()
    game.run()