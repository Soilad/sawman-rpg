from dataclasses import dataclass

from pygame import Surface

from components import *


@dataclass
class Entity:
    collision: Collision
    movement: Movement
    render:   Render
    id:       int

@dataclass
class World:
    renderOverlays: Dict[int, Surface]
    dialogueIndex:  int
    enterTime:      int
    tick:           int
