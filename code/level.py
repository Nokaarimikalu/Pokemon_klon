import pygame, os
from pytmx import load_pygame, TiledTileLayer, TiledObjectGroup
from player import Player

class Level:
    def __init__(self, tmx_data):
        # 1. getting the display surface
        self.display_surface = pygame.display.get_surface()
        self.window_w = self.display_surface.get_width()
        self.window_h = self.display_surface.get_height()

        # 2. loading the map into my Game
        base_path = os.path.dirname(__file__)
        tmx_path = os.path.abspath(os.path.join(base_path, "..", "map", f"{tmx_data}.tmx"))
        self.tmx_data = load_pygame(tmx_path)

        # 3. pre-load the map
        self.foreground, self.background,  = self.setup_map()
        self.foreground = pygame.transform.scale_by(self.foreground, 1.5)
        self.background = pygame.transform.scale_by(self.background, 1.5)
        
        # 4. Camera-position
        self.offset = pygame.math.Vector2(0, 0)
        self.move_speed = 300

        # 5. Player instance
        self.player = Player()

        # 6. Collision on static hidden objects
        self.static_collision_rects = []
        self.collision_setup()

        # 7. Collision on dynamic objects with pygame.sprite.Sprite


    def run(self, dt):
        self.input(dt)
        # drawing the backround player and foreground
        self.display_surface.blit(self.background, self.offset)
        self.display_surface.blit(self.player.scaled_image, self.player.rect)
        self.display_surface.blit(self.foreground, self.offset)
        
    def input(self, dt):
        keys = pygame.key.get_pressed()
        
        map_pixel_width = self.tmx_data.width * self.tmx_data.tilewidth * 1.5
        map_pixel_height = self.tmx_data.height * self.tmx_data.tileheight * 1.5
        max_x = -(map_pixel_width - self.window_w)
        max_y = -(map_pixel_height - self.window_h)


        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.offset.y < 0:
            self.offset.y += self.move_speed * dt
        elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.offset.y > max_y:
            self.offset.y -= self.move_speed * dt
        elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.offset.x < 0:
            self.offset.x += self.move_speed * dt
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.offset.x > max_x:
            self.offset.x -= self.move_speed * dt

    def collision_setup(self):
        objectsgroup = self.tmx_data.objectgroups
        for group in objectsgroup: 
            if group.name == "collision":
                for obj in group:
                    scaled_x = obj.x * 1.5
                    scaled_y = obj.y * 1.5
                    scaled_w = obj.width * 1.5
                    scaled_h = obj.height * 1.5

                    new_rect = pygame.Rect(scaled_x, scaled_y, scaled_w, scaled_h)
                    self.static_collision_rects.append(new_rect)
                  
                    
    def setup_map(self):
       
        w = self.tmx_data.width * self.tmx_data.tilewidth
        h = self.tmx_data.height * self.tmx_data.tileheight
        foreground_surf = pygame.Surface((w, h)).convert_alpha()
        foreground_surf.fill((0,0,0,0))
        background_surf = pygame.Surface((w, h)).convert_alpha()
        background_surf.fill((0,0,0,0))
       

        for layer in self.tmx_data.visible_layers: # tmx_data.visible_layers means each visible activated layer
            if isinstance(layer, TiledTileLayer):  # checking if its a tiledtilelayer and not a object
                # seperating background and foreground to draw player between them
                if layer.name == "foreground":     
                    for x, y, gid in layer:
                        tile = self.tmx_data.get_tile_image_by_gid(gid)
                        if tile:
                            foreground_surf.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))
                
                if layer.name == "ground"  or layer.name == "details"  or layer.name == "obstacle":
                    for x, y, gid in layer:
                        tile = self.tmx_data.get_tile_image_by_gid(gid)
                        if tile:
                            background_surf.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))
        
        return foreground_surf,background_surf

    
  
    
    