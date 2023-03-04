from typing import *
import pygame
from config import (POLICY_FONT, POLICY_FONT_SIZE, POLICY_OFFSET, UTILITY_FONT,
                    UTILITY_FONT_SIZE, UTILITY_OFFSET, block_size)

pygame.init()


class DisplayManager(object):

    GREEN = (100, 200, 100)
    RED = (200, 100, 100)
    WHITE = (200, 200, 200)
    GREY = (50, 50, 50)
    SCREEN_COLOR = (0, 0, 0)

    RATIO = 1

    def __init__(self, height: int, width: int, output: str) -> None:
        super().__init__()
        self.block_size = block_size
        self.width = block_size * width
        self.height = block_size * height
        self.screen_dimensions = (self.width, self.height)
        self.output = output

    def get_colors_for_grid(self, grid):
        colors = []
        for row in grid:
            color = []
            for cell in row:
                if cell == 'W':
                    color.append(DisplayManager.GREY)
                elif cell == 'G':
                    color.append(DisplayManager.GREEN)
                elif cell == 'R':
                    color.append(DisplayManager.RED)
                else:
                    color.append(DisplayManager.WHITE)
            colors.append(color)
        return colors

    def display(self, result: dict):
        algorithm = result['algorithm']

        # Display utilities
        utilities = [["{:.3f}".format(cell) for cell in row] for row in result['utilities']]
        self.generate(array=utilities, grid=result["grid"], offset=UTILITY_OFFSET, font=pygame.font.SysFont(UTILITY_FONT, UTILITY_FONT_SIZE),
                      title=f'{algorithm} Utilities', save=True, file_name=f'docs/{algorithm}_utilities_{self.output}.png')

        # Display policies
        CONVERT_POLICY_TUPLE = {(1, 0): '↓', (-1, 0): '↑', (0, 1): '→', (0, -1): '←'}
        directions = [[CONVERT_POLICY_TUPLE[cell.value] if cell else cell 
                        for cell in row] for row in result['policy']]
        self.generate(array=directions, grid=result["grid"], offset=POLICY_OFFSET, font=pygame.font.SysFont(POLICY_FONT, POLICY_FONT_SIZE),
                      title=f'{algorithm} Policy', save=True, file_name=f'docs/{algorithm}_policy_{self.output}.png')

    def generate(self, array, grid, offset: Tuple, font: pygame.font.Font, title: str = 'Plot', 
                    save: bool = False, file_name: str = 'image.png'):
        screen = pygame.display.set_mode(self.screen_dimensions)
        pygame.display.set_caption(title)

        colors = self.get_colors_for_grid(grid=grid)
        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            rect = pygame.Rect(0, 0, self.width, self.height)
            pygame.draw.rect(screen, DisplayManager.SCREEN_COLOR, rect)

            for row in range(len(grid)):
                for col in range(len(grid[0])):
                    rect = pygame.Rect(col * self.block_size, row * self.block_size, self.block_size, self.block_size)
                    pygame.draw.rect(screen, colors[row][col], rect)
                    pygame.draw.rect(screen, (0, 0, 0), rect, 1)

                    if grid[row][col] == 'W':
                        continue
                    message = font.render(array[row][col], True, (0, 0, 0))
                    screen.blit(message, (col * self.block_size + offset[0] * DisplayManager.RATIO, 
                                    row * self.block_size + offset[1] * DisplayManager.RATIO))

            pygame.display.update()

            if save:
                pygame.image.save(screen, file_name)
