import pygame, os
from pytmx import load_pygame, TiledTileLayer
from player import Player

class Level:
    def __init__(self, tmx_data):
        # getting the display surface
        self.display_surface = pygame.display.get_surface()
        self.window_w = self.display_surface.get_width()
        self.window_h = self.display_surface.get_height()
       
        #loading the map into my Game
        base_path = os.path.dirname(__file__)
        tmx_path = os.path.abspath(os.path.join(base_path, "..", "map", f"{tmx_data}.tmx"))
        self.tmx_data = load_pygame(tmx_path)

        # pre-load the map
        self.foreground, self.background,  = self.setup_map()
        self.foreground = pygame.transform.scale_by(self.foreground, 1.5)
        self.background = pygame.transform.scale_by(self.background, 1.5)
        
        # Camera-position
        self.spawnpoint_x, self.spawnpoint_y = self.spawnpoint()
        self.offset_x = (1280 / 2) - self.spawnpoint_x
        self.offset_y = (720 / 2) - self.spawnpoint_y
        self.offset = pygame.math.Vector2(self.offset_x, self.offset_y)
        self.move_speed = 300
        map_pixel_width = self.tmx_data.width * self.tmx_data.tilewidth * 1.5
        map_pixel_height = self.tmx_data.height * self.tmx_data.tileheight * 1.5
        self.max_x = -(map_pixel_width - self.window_w)
        self.max_y = -(map_pixel_height - self.window_h)

        # Player instance
        self.player = Player()
        self.is_walking = False
        self.target_offset = pygame.math.Vector2()
        self.start_offset = pygame.math.Vector2()
        self.move_timer = 0

        # Collision on static hidden objects
        self.static_collision_rects = []
        self.collision_setup()

        # Collision on dynamic objects with pygame.sprite.Sprite

    def update(self, dt):
            self.input()
            
            if self.is_walking: 
                self.move_timer += dt #counts the time
                fraction = self.move_timer / 0.2
                
                if fraction >= 1:
                    self.offset = self.target_offset.copy()
                    self.is_walking = False
                else:
                    self.offset = self.start_offset.lerp(self.target_offset, fraction)

            self.display_surface.blit(self.background, self.offset)
            self.display_surface.blit(self.player.scaled_image, self.player.rect)
            self.display_surface.blit(self.foreground, self.offset)

    def input(self):
        keys = pygame.key.get_pressed()
        if self.is_walking:
            return 
        
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.offset.y < 0:
            self.is_walking = True
            self.move_timer = 0
            self.start_offset = self.offset.copy()
            self.target_offset = self.offset + pygame.math.Vector2(0, 48)
        elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.offset.y > self.max_y:
            self.is_walking = True
            self.move_timer = 0
            self.start_offset = self.offset.copy()
            self.target_offset = self.offset + pygame.math.Vector2(0, -48)
        elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.offset.y < 0:
            self.is_walking = True
            self.move_timer = 0
            self.start_offset = self.offset.copy()
            self.target_offset = self.offset + pygame.math.Vector2(48, 0)
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.offset.x > self.max_x:
            self.is_walking = True
            self.move_timer = 0
            self.start_offset = self.offset.copy()
            self.target_offset = self.offset + pygame.math.Vector2(-48, 0)
    
    def spawnpoint(self):
        scaled_x, scaled_y = 0, 0  # if he doesnt find the spawnpoint
        objectsgroup = self.tmx_data.objectgroups
        for group in objectsgroup:
            if group.name == "spawnpoint":
                for obj in group:
                    if obj.name == "sp_test":
                        scaled_x = obj.x * 1.5
                        scaled_y = obj.y * 1.5

        return scaled_x, scaled_y

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

    
  
    
    