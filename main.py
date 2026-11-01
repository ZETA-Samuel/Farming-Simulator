# /// script
# dependencies = [
#     "pytmx",
# ]
# ///

import asyncio
import pygame
from settings import *
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()
        pygame.display.set_caption("Farming Sim")

    async def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                self.level.input(event)

            dt = self.clock.tick(60) / 1000
            self.level.run(dt)
            pygame.display.flip()
            await asyncio.sleep(0)


async def main():
    game = Game()
    await game.run()


if __name__ == '__main__':
    asyncio.run(main())
