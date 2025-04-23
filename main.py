import glfw
from OpenGL.GL import *
from PIL import Image
import numpy as np
import random
import time
import pygame

pygame.init()
pygame.font.init()

class WoodyWoodpeckerGame:
    def __init__(self):
        # Inicialização do GLFW
        if not glfw.init():
            return

        # Criação da janela
        self.window = glfw.create_window(800, 600, "Woody Woodpecker Game", None, None)
        if not self.window:
            glfw.terminate()
            return

        # Configurações de contexto e teclado
        glfw.make_context_current(self.window)
        glfw.set_key_callback(self.window, self.key_callback)

        # Parâmetros do Pica-Pau
        self.woody_y = 300
        self.woody_velocity = 0
        self.gravity = -0.5
        self.jump_strength = 10
        self.lives = 3
        self.invulnerable_timer = 0
        self.visible = True
        self.woody_texture, self.woody_width, self.woody_height = self.load_texture("woody.png")

        # Lista de obstáculos (troncos)
        self.obstacles = []
        self.obstacle_width = 50
        self.obstacle_gap = 200
        self.spawn_obstacle_timer = 0
        self.obstacles_passed = 0

        # Lista de objetos aleatórios (vida, urubu e invencibilidade)
        self.power_ups = []
        self.spawn_random_timer = 0
        self.random_objects = []
        self.lives_texture, self.lives_width, self.lives_height = self.load_texture("lives.png")
        self.buzzard_texture, self.buzzard_width, self.buzzard_height = self.load_texture("buzzard.png")
        self.invincible_texture, self.invincible_width, self.invincible_height = self.load_texture("invincible.png")

    # Carrega e retorna uma textura a partir de um arquivo de imagem
    def load_texture(self, path):
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        image = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
        image = image.resize((56, int((56 / image.width) * image.height)))
        img_data = np.array(image.convert("RGBA"))

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return texture_id, image.width, image.height

    # Desenha uma textura na tela nas coordenadas especificadas
    def draw_texture(self, texture_id, x, y, width, height):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(x, y)
        glTexCoord2f(1, 0); glVertex2f(x + width, y)
        glTexCoord2f(1, 1); glVertex2f(x + width, y + height)
        glTexCoord2f(0, 1); glVertex2f(x, y + height)
        glEnd()
        glDisable(GL_TEXTURE_2D)

    # Renderiza texto na tela
    def draw_text(self, text, x, y, size=32, color=(255, 255, 255)):
        font = pygame.font.SysFont("Arial", size, bold=True)
        text_surface = font.render(text, True, color, (0, 0, 0))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_surface.get_width(), text_surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        self.draw_texture(texture_id, x, y, text_surface.get_width(), text_surface.get_height())
        glDeleteTextures([texture_id])

    # Desenha o personagem Pica-Pau
    def draw_woody(self):
        if self.visible:
            self.draw_texture(self.woody_texture, 100, self.woody_y, self.woody_width, self.woody_height)

    # Desenha os obstáculos na tela (troncos)
    def draw_obstacles(self):
        glColor3f(0.5, 0.35, 0.05)
        for o in self.obstacles:
            # Parte superior
            glBegin(GL_QUADS)
            glVertex2f(o['x'], o['top_height'])
            glVertex2f(o['x'] + self.obstacle_width, o['top_height'])
            glVertex2f(o['x'] + self.obstacle_width, 600)
            glVertex2f(o['x'], 600)
            glEnd()
            # Parte inferior
            glBegin(GL_QUADS)
            glVertex2f(o['x'], 0)
            glVertex2f(o['x'] + self.obstacle_width, 0)
            glVertex2f(o['x'] + self.obstacle_width, o['bottom_height'])
            glVertex2f(o['x'], o['bottom_height'])
            glEnd()

    # Desenha os indicadores de vida
    def draw_lives(self):
        glColor3f(1, 0, 0)
        for i in range(self.lives):
            x = 10 + i * 30
            y = 560
            glBegin(GL_QUADS)
            glVertex2f(x, y)
            glVertex2f(x + 20, y)
            glVertex2f(x + 20, y + 20)
            glVertex2f(x, y + 20)
            glEnd()

    # Atualiza a física e lógica do jogo
    def update_game_state(self):
        # Timer de invulnerabilidade e efeito de piscar
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
            self.visible = (self.invulnerable_timer // 5) % 2 == 0
        else:
            self.visible = True

        # Aplicação da gravidade
        self.woody_velocity += self.gravity
        self.woody_y += self.woody_velocity

        # Geração de novos obstáculos
        self.spawn_obstacle_timer += 1
        if self.spawn_obstacle_timer > 120:
            gap_y = random.randint(100, 500)
            self.obstacles.append({
                'x': 800,
                'top_height': gap_y + self.obstacle_gap // 2,
                'bottom_height': gap_y - self.obstacle_gap // 2,
                'passed': False
            })
            self.spawn_obstacle_timer = 0

        # Movimento e contagem de obstáculos
        for o in self.obstacles:
            o['x'] -= 3
            if not o['passed'] and o['x'] + self.obstacle_width < 100:
                o['passed'] = True
                self.obstacles_passed += 1
        self.obstacles = [o for o in self.obstacles if o['x'] > -50]

        # Geração de objetos aleatórios (vida, urubu e invencibilidade)
        self.spawn_random_timer += 1
        if self.spawn_random_timer > 100:
            obj_y = random.randint(100, 500)
            obj_size = random.randint(10, 30)
            if random.random() < 0.35:
                self.random_objects.append({'x': 800, 'y': obj_y, 'size': obj_size, 'type': 'lives'})
            elif random.random() < 0.35:
                self.random_objects.append({'x': 800, 'y': obj_y, 'size': obj_size, 'type': 'buzzard'})
            elif random.random() < 0.30:
                self.random_objects.append({'x': 800, 'y': obj_y, 'size': obj_size, 'type': 'invincible'})
            self.spawn_random_timer = 0

        # Movimento e remoção dos objetos aleatórios
        for obj in self.random_objects:
            obj['x'] -= 6
        self.random_objects = [o for o in self.random_objects if o['x'] > -50]

    # Verifica colisões entre o Pica-Pau e obstáculos ou objetos
    def check_collisions(self):
        if self.invulnerable_timer > 0:
            return

        margem = 10

        # Colisão com o chão ou teto
        if self.woody_y <= 0 or self.woody_y + self.woody_height >= 600:
            self.register_hit()
            return

        # Colisão com obstáculos
        for o in self.obstacles:
            if 100 + self.woody_width > o['x'] and 100 < o['x'] + self.obstacle_width:
                if self.woody_y + self.woody_height - margem >= o['top_height'] or self.woody_y + margem <= o['bottom_height']:
                    self.register_hit()
                    return

        # Colisão com objetos aleatórios
        for rdm_obstacle in self.random_objects:
            if 100 + self.woody_width > rdm_obstacle['x'] and 100 < rdm_obstacle['x'] + rdm_obstacle['size']:
                if self.woody_y + self.woody_height > rdm_obstacle['y'] and self.woody_y < rdm_obstacle['y'] + rdm_obstacle['size']:
                    if rdm_obstacle['type'] == 'buzzard':
                        self.register_hit()
                    elif rdm_obstacle['type'] == 'invincible':
                        self.invulnerable_timer = 240
                    elif rdm_obstacle['type'] == 'lives' and self.lives < 7:
                        self.lives += 1
                    self.random_objects.remove(rdm_obstacle)
                    return

    # Registra um hit no Pica-Pau
    def register_hit(self):
        self.lives -= 1
        self.invulnerable_timer = 60

    # Callback do teclado - espaço para pular
    def key_callback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_SPACE and action == glfw.PRESS:
            self.woody_velocity = self.jump_strength

    def draw_object(self, texture, x, y, width, height):
        self.draw_texture(texture, x, y, width, height)

    # Desenha os objetos aleatórios com base no tipo
    def draw_random_objects(self):
        for obj in self.random_objects:
            if obj['type'] == 'buzzard':
                self.draw_object(self.buzzard_texture, obj['x'], obj['y'], self.buzzard_width, self.buzzard_height)
            elif obj['type'] == 'lives':
                self.draw_object(self.lives_texture, obj['x'], obj['y'], self.lives_width, self.lives_height)
            elif obj['type'] == 'invincible':
                self.draw_object(self.invincible_texture, obj['x'], obj['y'], self.invincible_width, self.invincible_height)

    # Loop principal do jogo
    def run(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT)
            glLoadIdentity()
            glOrtho(0, 800, 0, 600, -1, 1)

            self.update_game_state()
            self.check_collisions()

            self.draw_woody()
            self.draw_obstacles()
            self.draw_random_objects()
            self.draw_lives()
            self.draw_text(f"SCORE: {self.obstacles_passed}", 650, 560, 28, (255, 0, 0))

            glfw.swap_buffers(self.window)

            if self.lives <= 0:
                self.show_game_over()
                break

            time.sleep(0.016)

        glfw.terminate()

    # Exibe a tela de game over com score
    def show_game_over(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glOrtho(0, 800, 0, 600, -1, 1)
        glColor3f(0, 0, 0)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(800, 0)
        glVertex2f(800, 600)
        glVertex2f(0, 600)
        glEnd()
        self.draw_text("GAME OVER", 220, 300, 64, (255, 0, 0))
        self.draw_text(f"SCORE: {self.obstacles_passed}", 300, 220, 48, (255, 0, 0))
        glfw.swap_buffers(self.window)
        time.sleep(2)

def main():
    game = WoodyWoodpeckerGame()
    game.run()

if __name__ == "__main__":
    main()