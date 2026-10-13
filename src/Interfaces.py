from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from uuid import UUID, uuid1

from pygame import Rect, Vector2

from consts import AlignUI, CollisionType, Signal

if TYPE_CHECKING:
    from pygame import Surface

    from structs import World


@dataclass(slots=True, kw_only=True)
class IMovable(ABC):
    position: Vector2 = field(default_factory=Vector2)

    @abstractmethod
    def onMove(self, world) -> tuple[int, int]:
        raise NotImplementedError(
            "onMove method must be implemented by subclasses.")


@dataclass(slots=True, kw_only=True)
class IInteractable(ABC):

    @abstractmethod
    def onInteract(self, world):
        raise NotImplementedError(
            "onInteract method must be implemented by subclasses.")


@dataclass(slots=True, kw_only=True)
class IRenderable(ABC):
    blitOffset: Vector2 = field(default_factory=Vector2)

    @abstractmethod
    def onRender(self, screen, position, sprite_pos) -> None:
        raise NotImplementedError(
            "onRender method must be implemented by subclasses.")


@dataclass(slots=True, kw_only=True)
class ICommandable(ABC):
    emitted: bool = field(default=False)
    signal: Signal = field(default=Signal.OK)

    def emit(self, world: World) -> Signal:
        if self.emitted:
            self.refresh(world)
            return Signal.OK
        self.emitted = self.init(world)
        return self.signal

    @abstractmethod
    def init(self, world: World) -> bool:
        return True

    @abstractmethod
    def refresh(self, world: World) -> None:
        pass

    def reset(self) -> None:
        self.emitted = False


@dataclass(slots=True, kw_only=True)
class ICollidable(ABC):
    collideReturn: CollisionType
    rect: Rect = field(default_factory=Rect)

    @abstractmethod
    def onCollide(self, point: Vector2) -> CollisionType:
        pass


@dataclass(slots=True, kw_only=True)
class UI(ABC):
    rect: Rect = field(default_factory=Rect)
    children: list[UI] = field(default_factory=list)
    align: tuple[AlignUI, AlignUI] = (AlignUI.START, AlignUI.START)
    id: UUID = field(default_factory=uuid1)
    z: int = 0

    @abstractmethod
    def draw(self, screen: Surface) -> None:
        pass

    def update(self) -> None:
        pass

    def onHover(self, world: World) -> bool:
        return False
