# functions here are for finishing a dialog with an npc and should return 2 functions
# first func: to check if the npc can go to the next dialog
# second func: runs after finishing dialog
from collections.abc import Callable
from numba import jit

def npc_give_items(items_given: dict[tuple[str, int], int]) -> (Callable, Callable):
    def giveable(inventory: dict[tuple[str, int], int]) -> bool:
        return all([item_count + inventory.get(item, 0) >= 0 for item, item_count in items_given.items()])

    def give(inventory: dict[tuple[str, int]: int]):
        for item in items_given:
            if inventory.get(item, 0) + items_given[item] > 0:
                inventory[item] = inventory.get(item, 0) + items_given[item]
            else:
                del inventory[item]
    return giveable, give

@jit
def npc_do_nothing() -> (Callable, Callable):
    def placeholder_1(*args):
        return True 

    def placeholder_2(*args):
        pass
    return placeholder_1, placeholder_2
