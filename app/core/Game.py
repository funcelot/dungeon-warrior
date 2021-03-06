import os
from typing import List

import pygame
from core.DebugProcessor import Debug
from core.Globals import Caption, CellSize, Fps, TerminalSize
from core.interfaces import IGameEventProcessor, IGameProcessor
from core.KeyboardProcessor import Keyboard
from core.MouseProcessor import Mouse
from core.TextPainter import TextPainter
from core.Utils import debugger
from pygame import Surface

pygame.init()
pygame.font.init()


class Game:
    Icon = pygame.image.load(os.path.join("images", "dungeon.png"))
    Font = pygame.font.Font(
        os.path.join("fonts", "SourceCodePro-Regular.ttf"), CellSize[1] - 10
    )

    def __init__(
        self,
        size: tuple[
            int, int
        ],  # = (TerminalSize[0]*CellSize[0], TerminalSize[1]*CellSize[1]),
        processors: List[IGameProcessor],
        event_processors: List[IGameEventProcessor],
        exit_processor: IGameEventProcessor,
    ):
        self.exit_processor: IGameEventProcessor = exit_processor
        self.event_processors: List[IGameEventProcessor] = event_processors
        self.processors: List[IGameProcessor] = processors
        self.surface: Surface = pygame.display.set_mode(
            size, flags=pygame.NOFRAME, vsync=0
        )
        self.painter: TextPainter = TextPainter(Game.Font)

    def init(self) -> None:
        pygame.display.set_caption(Caption)
        pygame.display.set_icon(Game.Icon)
        self.clock = pygame.time.Clock()
        print("Game started!")

    def quit(self) -> None:
        pygame.quit()
        print("Game exited!")

    @debugger(raise_exception=True)
    def draw(self) -> None:
        while True:
            for event in pygame.event.get():
                if self.exit_processor.process(event):
                    return
                for event_processor in self.event_processors:
                    event_processor.process(event)

            for processor in self.processors:
                processor.process()

            self.surface.fill((0, 0, 0))
            self.painter.paint(Debug.text, self.surface)

            self.clock.tick(Fps)

            pygame.display.flip()
