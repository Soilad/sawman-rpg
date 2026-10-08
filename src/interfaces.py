from dataclasses import dataclass
from typing import TYPE_CHECKING

from pygame import Surface, Vector2

from consts import CollisionType, Signal
from func import lerp

if TYPE_CHECKING:
    from structs import World


class Movement:
    position: Vector2 = Vector2(0, 0)
    def onMove(self, world, entities, keys) -> tuple[int, int]:
        """
        Handle movement in the specified direction.
        """
        raise NotImplementedError("onMove method must be implemented by subclasses.")

class Interact:
    def onInteract(self, world):
        """
        Handle interaction with the object.
        
        :param screen: The game screen where the interaction occurs.
        :param surface: The surface to render the interaction on.
        :param font_medium: The font used for rendering text.
        :param player_vars: Player-related variables and states.
        :param Inventory: The player's inventory.
        :param b_togg: A toggle for interaction state.
        :param text_scroll: The current scroll position of the text.
        :param y_position: The vertical position for rendering text.
        """
        raise NotImplementedError("onInteract method must be implemented by subclasses.")

class Render:
    def onRender(self, screen, position, sprite_pos) -> None:
        """
        Handle rendering of the object.
        
        :param screen: The game screen where the object is rendered.
        :param position: The position on the screen where the object should be drawn.
        """
        raise NotImplementedError("onRender method must be implemented by subclasses.")

@dataclass(slots=True)
class Command:
    emitted = False
    signal  = Signal.OK
    def emit(self, world: World) -> Signal:
        if self.emitted:
            self.refresh(world)
            return Signal.OK
        self.init(world)
        self.emitted = True
        return self.signal


    def init(self, world: World) -> None:
        pass

    def refresh(self, world: World) -> None:
        pass

    def reset(self) -> None:
        self.emitted = False

class UI:
    z: int
    def draw(self, screen: Surface) -> None:
        pass

    def onHover(self, world: World) -> bool:
        pass

class Collision:
    def onCollide(self, point: Vector2) -> CollisionType:
        pass
