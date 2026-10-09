from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pygame import Rect, Vector2

from consts import AlignUI, Signal

if TYPE_CHECKING:
    from pygame import Surface

    from consts import CollisionType
    from structs import World


@dataclass
class IMovable(ABC):
    position: Vector2 = field(default_factory=Vector2)

    @abstractmethod
    def onMove(self, world) -> tuple[int, int]:
        """
        Handle movement in the specified direction.
        """
        raise NotImplementedError("onMove method must be implemented by subclasses.")

@dataclass
class IInteractable(ABC):
    @abstractmethod
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

@dataclass
class IRenderable(ABC):
    @abstractmethod
    def onRender(self, screen, position, sprite_pos) -> None:
        """
        Handle rendering of the object.
        
        :param screen: The game screen where the object is rendered.
        :param position: The position on the screen where the object should be drawn.
        """
        raise NotImplementedError("onRender method must be implemented by subclasses.")

@dataclass
class ICommandable(ABC):
    emitted = False
    signal  = Signal.OK
    def emit(self, world: World) -> Signal:
        if self.emitted:
            self.refresh(world)
            return Signal.OK
        self.init(world)
        self.emitted = True
        return self.signal


    @abstractmethod
    def init(self, world: World) -> None:
        pass

    @abstractmethod
    def refresh(self, world: World) -> None:
        pass

    def reset(self) -> None:
        self.emitted = False

@dataclass
class ICollidable(ABC):
    align: tuple[AlignUI, AlignUI]
    rect:  Rect = field(default_factory=Rect)
    @abstractmethod
    def onCollide(self, point: Vector2) -> CollisionType:
        pass

class UI(ABC):
    z    : int                     = 0
    rect : Rect                    = Rect()
    align: tuple[AlignUI, AlignUI] = (AlignUI.START, AlignUI.START)

    @abstractmethod
    def draw(self, screen: Surface) -> None:
        pass

    def update(self) -> None:
        pass

    def onHover(self, world: World) -> bool:
        return False
