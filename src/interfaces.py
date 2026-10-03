from pygame import Vector2


class Movement:
    position: Vector2
    def onMove(self, world, entities, keys) -> tuple[int, int]:
    # def onMove(self, player_vars, room, keys, tick, wall, entertime, ysort, offset):
    # def onMove(self, scale, room, ysort, tick) -> int:
        """
        Handle movement in the specified direction.
        """
        raise NotImplementedError("onMove method must be implemented by subclasses.")

class Interact:
    def onInteract(self, screen, surface, font_medium, player_vars, Inventory, b_togg, text_scroll, y_position):
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
    def onRender(self, screen, position):
        """
        Handle rendering of the object.
        
        :param screen: The game screen where the object is rendered.
        :param position: The position on the screen where the object should be drawn.
        """
        raise NotImplementedError("onRender method must be implemented by subclasses.")
