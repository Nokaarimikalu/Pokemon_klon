import pygame, os
from pytmx import load_pygame, TiledTileLayer
from player import Player

class Level:
    def __init__(self):
        # 1. Display Surface holen
        self.display_surface = pygame.display.get_surface()
        self.window_w = self.display_surface.get_width()
        self.window_h = self.display_surface.get_height()

        # 2. Map laden
        base_path = os.path.dirname(__file__)
        tmx_path = os.path.abspath(os.path.join(base_path, "..", "map", "Route_01.tmx"))
        self.tmx_data = load_pygame(tmx_path)

        # 3. Map vor-zeichnen
        self.map_surface = self.setup_map()
        self.scaled_map = pygame.transform.scale_by(self.map_surface, 1.5)
        
        # 4. Kamera-Position
        self.offset = pygame.math.Vector2(0, 0)
        self.move_speed = 400
        player = Player()

    def setup_map(self):
        # Erstellt eine Surface in Map-Größe und zeichnet alle Tiles darauf
        w = self.tmx_data.width * self.tmx_data.tilewidth
        h = self.tmx_data.height * self.tmx_data.tileheight
        surf = pygame.Surface((w, h))

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        surf.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))
        return surf

    def input(self, dt):
        keys = pygame.key.get_pressed()
        
        # Grenzwerte (Maximaler Versatz)
        max_x = -(self.scaled_map.get_width() - self.window_w)
        max_y = -(self.scaled_map.get_height() - self.window_h)

        if keys[pygame.K_w] and self.offset.y < 0:
            self.offset.y += self.move_speed * dt
        if keys[pygame.K_s] and self.offset.y > max_y:
            self.offset.y -= self.move_speed * dt
        if keys[pygame.K_a] and self.offset.x < 0:
            self.offset.x += self.move_speed * dt
        if keys[pygame.K_d] and self.offset.x > max_x:
            self.offset.x -= self.move_speed * dt

    def run(self, dt):
        self.input(dt)
        # Die Map an der aktuellen Kamera-Position zeichnen
        self.display_surface.blit(self.scaled_map, self.offset)