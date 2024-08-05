from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
import pygame

# Definir algumas cores
PACMAN_COLOR = (255, 255, 0)  # Amarelo
GHOST_COLOR = (255, 0, 0)     # Vermelho
BACKGROUND_COLOR = (0, 0, 0)  # Preto

class PacmanAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.direction = (0, 0)  # Direção inicial (sem movimento)

    def step(self):
        # Movimenta o Pacman na direção definida
        next_position = (self.pos[0] + self.direction[0], self.pos[1] + self.direction[1])
        if self.model.grid.is_cell_empty(next_position):
            self.model.grid.move_agent(self, next_position)

    def set_direction(self, direction):
        self.direction = direction

class GhostAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Movimenta o fantasma em direção ao Pacman
        pacman_position = self.model.pacman.pos
        x, y = self.pos
        target_x, target_y = pacman_position
        
        # Simples lógica de perseguição: mova um passo na direção do Pacman
        if x < target_x:
            new_position = (x + 1, y)
        elif x > target_x:
            new_position = (x - 1, y)
        elif y < target_y:
            new_position = (x, y + 1)
        else:  # y > target_y
            new_position = (x, y - 1)

        # Move o fantasma se a célula estiver vazia
        if self.model.grid.is_cell_empty(new_position):
            self.model.grid.move_agent(self, new_position)

class PacmanModel(Model):
    def __init__(self, width, height):
        super().__init__()  # Inicializa a classe pai Model
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)
        
        # Adicionar Pac-Man e Fantasmas
        self.pacman = PacmanAgent(1, self)
        self.grid.place_agent(self.pacman, (1, 1))
        self.schedule.add(self.pacman)
        
        self.ghosts = []
        ghost = GhostAgent(2, self)
        self.grid.place_agent(ghost, (5, 5))
        self.schedule.add(ghost)
        self.ghosts.append(ghost)

    def step(self):
        self.schedule.step()

# Exemplo de loop de visualização com Pygame
def run_game():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    model = PacmanModel(10, 10)
    
    cell_width = screen.get_width() / model.grid.width
    cell_height = screen.get_height() / model.grid.height
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    model.pacman.set_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    model.pacman.set_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    model.pacman.set_direction((-1, 0))
                elif event.key == pygame.K_RIGHT):
                    model.pacman.set_direction((1, 0))
        
        model.step()
        
        screen.fill(BACKGROUND_COLOR)
        
        # Desenhar os agentes na tela
        for (x, y), cell_contents in model.grid.coord_iter():
            for agent in cell_contents:
                if isinstance(agent, PacmanAgent):
                    pygame.draw.circle(screen, PACMAN_COLOR, 
                                       (int(x * cell_width + cell_width / 2),
                                        int(y * cell_height + cell_height / 2)),
                                       int(min(cell_width, cell_height) / 2) - 2)
                elif isinstance(agent, GhostAgent):
                    pygame.draw.rect(screen, GHOST_COLOR, 
                                     (x * cell_width, y * cell_height, cell_width, cell_height))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    run_game()
