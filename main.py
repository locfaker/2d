#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Game Phù Thủy Lửa - Fire Mage Adventure
Game 2D Pixel hành động với nhân vật phù thủy lửa
"""
import pygame
import sys
import os
import time
import random
from src.config import *
from src.game_manager import GameManager

class Game:
    """Class chính điều khiển game"""
    def __init__(self):
        # Khởi tạo pygame
        pygame.init()
        pygame.display.set_caption("Phù Thủy Lửa - Fire Mage Adventure")
        pygame.display.set_icon(self.create_icon())
        
        # Tạo cửa sổ game
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Khởi tạo clock
        self.clock = pygame.time.Clock()
        
        # Kiểm tra và tạo thư mục cần thiết
        self.check_directories()
        
        # Tải tài nguyên
        self.load_resources()
        
        # Khởi tạo GameManager
        self.game_manager = GameManager(self.screen)
        
        # Cờ debug
        self.debug_mode = False
    
    def create_icon(self):
        """Tạo icon cho cửa sổ game"""
        icon = pygame.Surface((32, 32))
        icon.fill((200, 50, 50))
        pygame.draw.circle(icon, (255, 150, 50), (16, 16), 10)
        pygame.draw.circle(icon, (255, 220, 100), (16, 16), 5)
        return icon
    
    def check_directories(self):
        """Kiểm tra và tạo các thư mục cần thiết"""
        directories = [
            IMAGES_DIR,
            os.path.join(IMAGES_DIR, "characters"),
            os.path.join(IMAGES_DIR, "effects"),
            os.path.join(IMAGES_DIR, "ui"),
            os.path.join(IMAGES_DIR, "tiles"),
            SOUNDS_DIR,
            os.path.join(SOUNDS_DIR, "music"),
            os.path.join(SOUNDS_DIR, "sfx"),
            FONTS_DIR,
            os.path.join(ROOT_DIR, "maps"),
            os.path.join(ROOT_DIR, "saves")
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def load_resources(self):
        """Tải các tài nguyên cần thiết cho game"""
        # Thông báo tải
        self.screen.fill(BLACK)
        font = pygame.font.SysFont('Arial', 20)
        text_surf = font.render("Đang tải game...", True, WHITE)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text_surf, text_rect)
        pygame.display.flip()
        
        # Tạo placeholder sprites
        self.create_placeholder_sprites()
    
    def create_placeholder_sprites(self):
        """Tạo các sprite sheet placeholder cần thiết"""
        # Tạo file placeholder cho sprite sheet nếu chưa có
        player_sprite_path = os.path.join(IMAGES_DIR, "characters", "fire_mage_spritesheet.png")
        fireball_sprite_path = os.path.join(IMAGES_DIR, "effects", "fireball_spritesheet.png")
        enemy_types = ["slime", "skeleton", "golem"]
        
        # Di chuyển file sprite sheet hiện tại nếu có
        existing_player_sprite = os.path.join(IMAGES_DIR, "player_spritesheet.png")
        existing_fireball_sprite = os.path.join(IMAGES_DIR, "fireball_spritesheet.png")
        
        if os.path.exists(existing_player_sprite) and not os.path.exists(player_sprite_path):
            import shutil
            shutil.copy2(existing_player_sprite, player_sprite_path)
        
        if os.path.exists(existing_fireball_sprite) and not os.path.exists(fireball_sprite_path):
            import shutil
            shutil.copy2(existing_fireball_sprite, fireball_sprite_path)
        
        # Tạo sprite placeholder nếu không có
        if not os.path.exists(player_sprite_path):
            self.create_placeholder_sprite(player_sprite_path, 192, 144, (255, 0, 0))
        
        if not os.path.exists(fireball_sprite_path):
            self.create_placeholder_sprite(fireball_sprite_path, 192, 48, (255, 128, 0))
        
        # Tạo sprite placeholder cho kẻ địch
        for enemy_type in enemy_types:
            enemy_sprite_path = os.path.join(IMAGES_DIR, "characters", f"{enemy_type}_spritesheet.png")
            if not os.path.exists(enemy_sprite_path):
                if enemy_type == "slime":
                    color = (255, 0, 0)  # Đỏ
                elif enemy_type == "skeleton":
                    color = (200, 200, 200)  # Xám
                else:  # golem
                    color = (150, 75, 0)  # Nâu
                self.create_placeholder_sprite(enemy_sprite_path, 192, 48, color)
        
        # Tạo thêm placeholder cho UI và các hiệu ứng mới
        self.create_ui_placeholders()
        self.create_tiles_placeholders()
    
    def create_ui_placeholders(self):
        """Tạo placeholder cho các thành phần UI"""
        ui_elements = {
            'button': (200, 60, (80, 80, 100)),
            'panel': (300, 200, (60, 60, 80)),
            'frame': (100, 100, (100, 100, 120)),
            'icon_health': (48, 48, (220, 50, 50)),
            'icon_mana': (48, 48, (50, 100, 220)),
            'icon_exp': (48, 48, (50, 200, 50))
        }
        
        for name, (width, height, color) in ui_elements.items():
            path = os.path.join(IMAGES_DIR, "ui", f"{name}.png")
            if not os.path.exists(path):
                self.create_placeholder_ui(path, width, height, color)
    
    def create_tiles_placeholders(self):
        """Tạo placeholder cho các tile"""
        tileset_path = os.path.join(IMAGES_DIR, "tiles", "tileset.png")
        
        if not os.path.exists(tileset_path):
            # Tạo một tileset 4x4 với các tile 48x48
            tileset_width, tileset_height = 192, 192
            surface = pygame.Surface((tileset_width, tileset_height), pygame.SRCALPHA)
            
            # Danh sách màu cho các loại tile
            colors = [
                (50, 50, 50),    # floor
                (100, 100, 100),  # wall
                (0, 100, 200),    # water
                (0, 150, 0),      # grass
                (200, 200, 0),    # decoration
                (150, 75, 0),     # dirt
                (150, 150, 150),  # stone
                (100, 0, 0),      # lava
                (200, 100, 0),    # sand
                (100, 50, 0),     # wood
                (50, 150, 200),   # ice
                (150, 0, 150),    # magic
                (50, 50, 150),    # crystal
                (200, 150, 100),  # brick
                (0, 100, 0),      # bush
                (100, 100, 50)    # path
            ]
            
            # Tạo các tile
            tile_size = 48
            for y in range(4):
                for x in range(4):
                    idx = y * 4 + x
                    if idx < len(colors):
                        color = colors[idx]
                    else:
                        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    
                    rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                    pygame.draw.rect(surface, color, rect)
                    pygame.draw.rect(surface, (0, 0, 0), rect, 1)  # viền đen
                    
                    # Vẽ chi tiết
                    detail_color = (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50))
                    if idx == 0:  # floor
                        for _ in range(5):
                            dx = random.randint(5, tile_size - 10)
                            dy = random.randint(5, tile_size - 10)
                            pygame.draw.circle(surface, detail_color, (x * tile_size + dx, y * tile_size + dy), 2)
                    elif idx == 1:  # wall
                        for i in range(3):
                            pygame.draw.line(
                                surface, 
                                detail_color,
                                (x * tile_size + 5, y * tile_size + 10 + i * 12),
                                (x * tile_size + tile_size - 5, y * tile_size + 10 + i * 12),
                                2
                            )
            
            # Tạo thư mục nếu chưa tồn tại
            os.makedirs(os.path.dirname(tileset_path), exist_ok=True)
            
            # Lưu tileset
            pygame.image.save(surface, tileset_path)

    def create_placeholder_sprite(self, path, width, height, color):
        """Tạo sprite placeholder"""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Tạo nhiều sprite trong một sheet
        cols = width // 48
        rows = height // 48
        
        for row in range(rows):
            for col in range(cols):
                sprite_rect = pygame.Rect(col * 48, row * 48, 48, 48)
                pygame.draw.rect(surface, color, sprite_rect.inflate(-10, -10))
                # Vẽ đường viền
                pygame.draw.rect(surface, (255, 255, 255), sprite_rect.inflate(-10, -10), 1)
                # Tạo đặc điểm nhận dạng
                pygame.draw.circle(surface, (255, 255, 255), sprite_rect.center, 10)
        
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Lưu sprite sheet
        pygame.image.save(surface, path)
    
    def create_placeholder_ui(self, path, width, height, color):
        """Tạo placeholder cho UI"""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Vẽ nền có viền bo tròn
        rect = pygame.Rect(0, 0, width, height)
        pygame.draw.rect(surface, color, rect, border_radius=8)
        pygame.draw.rect(surface, (255, 255, 255), rect, 2, border_radius=8)
        
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Lưu ảnh
        pygame.image.save(surface, path)
    
    def run(self):
        """Vòng lặp chính của game"""
        previous_time = time.time()
        running = True
        
        while running:
            # Tính toán delta time
            current_time = time.time()
            dt = current_time - previous_time
            previous_time = current_time
            
            # Xử lý các sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Bật/tắt chế độ debug
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        self.debug_mode = not self.debug_mode
            
            # Xử lý input
            self.game_manager.handle_input()
            
            # Cập nhật game
            self.game_manager.update(dt)
            
            # Vẽ game
            self.game_manager.draw()
            
            # Hiển thị FPS nếu đang ở chế độ debug
            if self.debug_mode:
                fps = self.clock.get_fps()
                fps_text = f"FPS: {fps:.1f}"
                font = pygame.font.SysFont('Arial', 16)
                fps_surf = font.render(fps_text, True, WHITE)
                self.screen.blit(fps_surf, (10, SCREEN_HEIGHT - 30))
            
            # Cập nhật màn hình
            pygame.display.flip()
            
            # Giới hạn FPS
            self.clock.tick(FPS)
        
        # Thoát game
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
