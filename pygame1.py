import pygame

# Define classes
class Display:
    def __init__(self):
        self.screen = pygame.display.set_mode((300, 300))
        pygame.display.set_caption("Runner Game")
        self.sky_surface = pygame.image.load('Graphics/sky.png').convert_alpha()
        self.grass_surface = pygame.image.load('Graphics/grass.png').convert_alpha()
        self.font = pygame.font.Font(None, 30)
        self.game_name = self.font.render("Pixel Runner", False, (111, 196, 169))
        self.game_name_rect = self.game_name.get_rect(center=(150, 75))
        self.game_message = self.font.render('Press space to run', False, (11, 196, 169))
        self.game_message_rect = self.game_message.get_rect(center=(150, 225))
    
    def display_score(self, start_time):
        current_time = int(pygame.time.get_ticks() / 1000) - start_time
        score_surf = self.font.render(f'Score: {current_time}', False, (64, 64, 64))
        score_rect = score_surf.get_rect(center=(150, 15))
        self.screen.blit(score_surf, score_rect)
        return current_time
    
    def draw_intro_screen(self, player_stand, player_stand_rect, score, score_message):
        self.screen.fill((94, 129, 162))
        self.screen.blit(player_stand, player_stand_rect)
        self.screen.blit(self.game_name, self.game_name_rect)
        if score == 0:
            self.screen.blit(self.game_message, self.game_message_rect)
        else:
            self.screen.blit(score_message, score_message.get_rect(center=(150, 225)))

    def draw_game_elements(self, player_surface, player_rect, snail_surface, snail_rect):
        # Draw sky and grass
        self.screen.blit(self.sky_surface, (0, 0))
        self.screen.blit(self.grass_surface, (0, 230))
        # Draw the player and the snail
        self.screen.blit(player_surface, player_rect)
        self.screen.blit(snail_surface, snail_rect)

class Snail:
    def __init__(self):
        self.snail_frames = [
            pygame.transform.scale(pygame.image.load('Graphics/snail/snail1.png').convert_alpha(), (47, 17)),
            pygame.transform.scale(pygame.image.load('Graphics/snail/snail2.png').convert_alpha(), (47, 17))
        ]
        self.snail_index = 0
        self.snail_surface = self.snail_frames[self.snail_index]
        self.snail_rect = self.snail_surface.get_rect(midbottom=(275, 230))
        self.speed = 3.2
        self.snail_animation_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.snail_animation_timer, 290)
    
    def update_position(self):
        self.snail_rect.x -= self.speed
        if self.snail_rect.right <= 0:
            self.snail_rect.left = 300
            self.speed += 0.2
    
    def update_animation(self):
        self.snail_index = (self.snail_index + 1) % len(self.snail_frames)
        self.snail_surface = self.snail_frames[self.snail_index]

class Player:
    def __init__(self):
        self.player_surface = pygame.transform.scale(pygame.image.load('Graphics/player/player_walk_1.png').convert_alpha(), (30, 30))
        self.player_rect = self.player_surface.get_rect(midbottom=(30, 230))
        self.player_gravity = 0
        self.player_stand = pygame.image.load('Graphics/player/player_stand.png').convert_alpha()
        self.player_stand_rect = self.player_stand.get_rect(center=(150, 150))

    def update_gravity(self):
        self.player_gravity += 1
        self.player_rect.y += self.player_gravity
        if self.player_rect.bottom >= 230:
            self.player_rect.bottom = 230

class Game:
    def __init__(self):
        # Initialize pygame and other components
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display = Display()
        self.snail = Snail()
        self.player = Player()
        self.game_active = False
        self.run = True
        self.start_time = 0
        self.score = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if self.game_active:
                if event.type == pygame.KEYDOWN and self.player.player_rect.bottom >= 230:
                    if event.key == pygame.K_SPACE:
                        self.player.player_gravity = -22
                if event.type == pygame.MOUSEBUTTONDOWN and self.player.player_rect.bottom >= 230:
                    if self.player.player_rect.collidepoint(event.pos):
                        self.player.player_gravity = -22
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.game_active = True
                    self.snail.snail_rect.left = 300
                    self.start_time = int(pygame.time.get_ticks() / 1000)
            
            if event.type == self.snail.snail_animation_timer:
                self.snail.update_animation()

    def game_loop(self):
        while self.run:
            self.handle_events()

            if self.game_active:
                # Update positions and draw game elements
                self.score = self.display.display_score(self.start_time)
                self.snail.update_position()
                self.player.update_gravity()
                self.display.draw_game_elements(
                    self.player.player_surface,
                    self.player.player_rect,
                    self.snail.snail_surface,
                    self.snail.snail_rect
                )
                
                # Check for collision
                if self.snail.snail_rect.colliderect(self.player.player_rect):
                    self.game_active = False
                    # Reset the speed when the game ends
                    self.snail.speed = 3.2
            else:
                # Draw the intro screen
                score_message = self.display.font.render(f'Your score: {self.score}', False, (11, 196, 169))
                self.display.draw_intro_screen(self.player.player_stand, self.player.player_stand_rect, self.score, score_message)

            # Update display and tick the clock
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

# Run the game
game = Game()
game.game_loop()
