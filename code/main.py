import pygame, sys
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Pokemon Clone")
        self.clock = pygame.time.Clock()
        
        # Das Level-Objekt erstellen
        self.level = Level()

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            
            # Das Level updaten und zeichnen
            self.level.run(dt)
            
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()