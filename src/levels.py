# from classes import Room, Obj, Portal, Chaser, cwd, Trader
# import custom_funcs
from collections.abc import Callable
from queue import Queue

import pygame
from pygame import Color, Rect, Vector2

from components import (
    BoxUI,
    ButtonUI,
    Chaser,
    CollisionType,
    Commands,
    DialogueCommand,
    Immovable,
    Invisible,
    NoInteract,
    Obstacle,
    PlayerMovement,
    RectOverlay,
    Room,
    RoomMovement,
    SignalCommand,
    Sprite,
    Spritesheet,
    SurfaceOverlay,
    Wall,
)
from components.command import MoveRoomCommand
from consts import (
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_TERTIARY,
    FONT_ALIASED,
    AlignUI,
    DirectionUI,
    EntityType,
    Signal,
    font_medium,
)
from structs import (
    BorderRadius,
    Entity,
    InitialTicks,
    Item,
    Overlays,
    PlayerData,
    World,
)

# levels = [
#     Room(
#         "soi",
#         "I_forgor_my_wallet",
#         0,
#         [
#             Obj(
#                 f"{cwd}/sprites/npc/contractman.png",
#                 (480, 280),
#                 [
#                     (
#                         (
#                             (("sawman", "ono"), "NO WAY?!?!?!?"),
#                             (("zweistein", "sad"), "wtf"),
#                             (0, "im gonna steal your balls"),
#                             (
#                                 ("sawman", "woe"),
#                                 "YOU CANT JUST STEAL THE PLOT OF DANDADAN CONTRACT",
#                             ),
#                         ),
#                         custom_funcs.npc_give_items({("Okaruns balls", 0): 2})
#                     ),
#                     (
#                         (
#                             (("zweistein", "sad"), "why tf did u give us okarun's balls"),
#                             (
#                                 0,
#                                 "its gonna take me years to castrate someone with no balls so take this and leave",
#                             ),
#                             (("sawman", "ono"), "..."),
#                             (("sawman", "sad"), "jesus"),
#                         ),
#                         custom_funcs.npc_do_nothing()
#                     ),
#                 ],
#             ),
#             Obj(
#                 f"{cwd}/sprites/npc/contractman.png",
#                 (800, 300),
#                 [
#                     (
#                         (
#                             (("sawman", "ono"), "NO WAY?!?!?!?"),
#                             (("zweistein", "sad"), "wtf"),
#                             (0, "im gonna steal your balls"),
#                             (
#                                 ("sawman", "woe"),
#                                 "YOU CANT JUST STEAL THE PLOT OF DANDADAN CONTRACT",
#                             ),
#                         ),
#                         custom_funcs.npc_give_items({("Okaruns balls", 0): -2})
#                     ),
#                     (
#                         (
#                             (("zweistein", "sad"), "why tf did u give us okarun's balls"),
#                             (
#                                 0,
#                                 "its gonna take me years to castrate someone with no balls so take this and leave",
#                             ),
#                             (("sawman", "ono"), "..."),
#                             (("sawman", "sad"), "jesus"),
#                         ),
#                         custom_funcs.npc_do_nothing()
#                     ),
#                 ],
#             ),
#         ],
#         [Portal((1230, 570), (100, 200), 1, (274, 208))],
#         "",
#     ),
#     Room(
#         "field1",
#         "I_stole_a_new_one",
#         1,
#         [
#             Obj(
#                 f"{cwd}/rooms/field1/objects/power.png",
#                 (0, 0),
#                 [
#                     (
#                         (
#                             (("zweistein", "sus"), "its like a great man once said"),
#                             (("zweistein", "woe"), "with great power"),
#                             (("sawman", "hapi"), "comes great electricity bill"),
#                         ),
#                         custom_funcs.npc_do_nothing()
#                     )
#                 ],
#             ),
#             Obj(
#                 f"{cwd}/rooms/field1/objects/anna.png",
#                 (650, 240),
#                 [
#                     (
#                         (
#                             (("sawman", "hapi"), "I"),
#                             (
#                                 ("sawman", "sad"),
#                                 "dont remember this college being here before",
#                             ),
#                             (("zweistein", "ono"), "i guess itsa new one"),
#                             (("sawman", "hapi"), "hell yea, im old"),
#                         ),
#                         custom_funcs.npc_do_nothing()
#                     )
#                 ],
#             ),
#             Obj(
#                 f"{cwd}/rooms/field1/objects/acab.png",
#                 (920, 310),
#                 [
#                     (
#                         (
#                             (("sawman", "woe"), "why is there a police car outside us"),
#                             (("zweistein", "sad"), "i mean"),
#                             (("zweistein", "woe"), "atleast its empty"),
#                             (("sawman", "angy"), "true"),
#                             (("sawman", "sad"), "hopefully it isnt here because of us"),
#                         ),
#                         custom_funcs.npc_do_nothing()
#                     )
#                 ],
#             ),
#         ],
#         [
#             Portal((1230, 570), (100, 200), 2, (100, 450)),
#             Portal((274, 428), (200, 100), 0, (1230, 450)),
#         ],
#         "",
#     ),
#     Room(
#         "crossway1",
#         0,
#         1,
#         [
#             Obj(
#                 f"{cwd}/sprites/npc/wamen1.png",
#                 (210, 280),
#                 [
#                     (
#                         (
#                             (("sawman", "hapi"), "..."),
#                             (("npc", "wamen1"), "..."),
#                             (("sawman", "angy"), "..."),
#                             (
#                                 ("zweistein", "sad"),
#                                 "do you seriously walk up to people and expect them to talk first?",
#                             ),
#                             (("sawman", "sad"), "let me handle this"),
#                             (("sawman", "angy"), "ok sawman"),
#                             (("sawman", "ono"), "you can overcome your fears this time"),
#                             (("npc", "wamen1"), "..."),
#                             (("sawman", "hapi"), "Hi im-"),
#                             (("npc", "wamen1"), "i have a boyfriend."),
#                             (("sawman", "sad"), "..."),
#                             (("zweistein", "hapi"), "that couldve gotten wayy worse"),
#                             (0, "*You got gynophobia *"),
#                         ),
#                         custom_funcs.npc_give_items({("Fear Of Women", 0): 1})
#                     ),
#                     (
#                         (
#                             (
#                                 ("zweistein", "angy"),
#                                 "alright, can you tell us what year it is",
#                             ),
#                             (("npc", "wamen1"), "uhhhh, its 1446"),
#                             (("zweistein", "ono"), "My god, we have gone back in time-"),
#                             (("sawman", "angy"), "its in the hijri calendar, probably"),
#                             (("npc", "wamen1"), "how did you-"),
#                             (("sawman", "sus"), "so its probably like 2024 ish"),
#                             (("npc", "wamen1"), "2025, but how did you know that?"),
#                             (("sawman", "hapi"), "i know some muslims"),
#                             (("sawman", "sad"), "or rather, i knew some muslims"),
#                             (
#                                 ("npc", "wamen1"),
#                                 "oh yea, right. considering the entire government collapsed and all",
#                             ),
#                             (("zweistein", "ono"), "..."),
#                             (("sawman", "ono"), "..."),
#                             (("zweistein", "woe"), "..."),
#                             (("sawman", "woe"), "AHHH SCARY WOMAN"),
#                         ),
#                         custom_funcs.npc_do_nothing()
#                     ),
#                 ],
#             )
#         ],
#         [
#             Portal((50, 570), (100, 500), 1, (1000, 570)),
#             Portal((1230, 370), (100, 500), 3, (50, 570)),
#             Portal((640, 470), (300, 100), 4, (50, 380)),
#         ],
#         "",
#     ),
#     Room(
#         "deadend1",
#         0,
#         1,
#         [
#             Obj(
#                 f"{cwd}/rooms/deadend1/horse.png",
#                 (403, 250),
#                 [
#                     (
#                         (
#                             (("zweistein", "hapi"), "horsie!!"),
#                             (("zweistein", "ono"), "OHGOD WHAT IS THAT"),
#                             (("cutscene", "dark"), "..."),
#                             (
#                                 ("cutscene", "horseman"),
#                                 "எ-என் வாழ்க்கையை மு-மு-முடித்துக்கொள்.",
#                             ),
#                             (
#                                 ("sawman", "ono"),
#                                 "UHHHHH, CAN I HELP YOU??????????????????????????",
#                             ),
#                             (("zweistein", "sad"), "..."),
#                             (
#                                 ("zweistein", "angy"),
#                                 "i dont think we can help him given the state hes in",
#                             ),
#                             (("sawman", "sus"), "..."),
#                         ),
#                         custom_funcs.npc_do_nothing()
#                     ),
#                 ],
#             )
#         ],
#         [Portal((50, 570), (100, 200), 2, (1130, 370))],
#         "",
#     ),
#     Room(
#         "field2",
#         0,
#         1,
#         [
#             Obj(
#                 f"{cwd}/rooms/field2/objects/foliage.png",
#                 (806, 353),
#                 [
#                     (
#                         (
#                             (("sawman", "woe"), "NO WAY, FOILIAGE"),
#                             (("zweistein", "sus"), "wait why is there vodka next to it?"),
#                             (0, "*you got vodka*"),
#                         ),
#                         custom_funcs.npc_give_items({("Vodka", 0.5): 1})
#                     ),
#                     (
#                         (
#                             (("zweistein", "sus"), "gopnik plant?"),
#                             (("sawman", "hapi"), "gopnik plant."),
#                             (("zweistein", "woe"), "gopnik plant!"),
#                         ),
#                         custom_funcs.npc_do_nothing()
#                     ),
#                 ],
#                 False,
#             )
#         ],
#         [
#             Portal((150, 830), (400, 100), 2, (640, 250)),
#             Portal((1200, 500), (200, 100), 5, (70, 650)),
#         ],
#         [
#             (("sawman", "sad"), "..."),
#             (("sawman", "sus"), "we were stuck there for a whole 5 years huh"),
#             (
#                 ("zweistein", "sus"),
#                 "yea, huh. seems like alot seems to have changed since then and now",
#             ),
#             (("sawman", "sad"), "i should be happy rn, but i just feel exhausted..."),
#         ],
#     ),
#     Room(
#         "field3",
#         0,
#         1,
#         [
#             Chaser(
#                 f"{cwd}/battle/enemies/Amalgam Type C.png",
#                 (590, 210),
#                 1,
#                 10,
#                 ["Amalgam Type C", 40],
#             )
#         ],
#         [
#             Portal((50, 570), (100, 200), 4, (800, 350)),
#             Portal((1200, 550), (200, 300), 6, (70, 450)),
#         ],
#         [
#             (("sawman", "woe"), "OH DEAR GOD WHAT IS THAT"),
#             (
#                 ("zweistein", "woe"),
#                 "ok whatever this dog thing is it definitely wants to kill us",
#             ),
#             (0, "WASD or arrow keys with enter should make u choose"),
#             (0, "and space should execute it"),
#             (0, "the inventory is still accessible if u need to reload or-"),
#             (("zweistein", "ono"), "AHHHHHH MY KNEEEEE"),
#             (0, "heal..."),
#         ],
#     ),
#     Room(
#         "shop1",
#         0,
#         1,
#         [],
#         [
#             Portal((50, 470), (100, 300), 5, (1000, 350)),
#             Portal((350, 550), (300, 100), 7, (777, 270)),
#         ],
#         [
#             (("goro", "goro1"), "HEY YOU"),
#             (("zweistein", "ono"), "..."),
#             (("sawman", "ono"), "hes not talking about us right???"),
#             (("goro", "goro2"), "MOTHERFUCKER YOU ARE THE ONLY 2 PEOPLE THERE"),
#             (("zweistein", "sad"), "maybe hes has double vision"),
#             (("zweistein", "sus"), "and is also schitzophrenic"),
#             (("goro", "goro1"), "I SAW WHAT YOU DID TO THAT DOG!"),
#             (("sawman", "sus"), "that was a dog?"),
#             (
#                 ("goro", "goro3"),
#                 "anyways. you have chainsaw hands, do you want to work here?",
#             ),
#             (("zweistein", "sad"), "i mean..."),
#             (("zweistein", "woe"), "we gotta get money somehow"),
#             (("sawman", "angy"), "uhhh"),
#             (("sawman", "sus"), "sure??"),
#             (("goro", "goro2"), "alright, get in here then"),
#         ],
#     ),
#     Room(
#         "chainsawshawarma",
#         "I_wanna_kms",
#         0,
#         [
#             Trader(
#                 f"{cwd}/rooms/chainsawshawarma/objects/goro.png",
#                 (852, 186),
#                 f"{cwd}/rooms/chainsawshawarma/shop.png",
#                 {("Shawarma", 20): 90, ("Kebab", 40): 100, ("Falafel Roll", 20): 90},
#             ),
#             Chaser(
#                 f"{cwd}/battle/enemies/Shawarma.png",
#                 (200, 100),
#                 0,
#                 0,
#                 ["Shawarma", 1000],
#             ),
#         ],
#         [Portal((777, 270), (88, 82), 6, (350, 550))],
#         [
#             (("goro", "goro1"), "HEY YOU"),
#             (("zweistein", "ono"), "..."),
#             (("sawman", "ono"), "hes not talking about us right???"),
#             (("goro", "goro2"), "MOTHERFUCKER YOU ARE THE ONLY 2 PEOPLE THERE"),
#             (("zweistein", "sad"), "maybe hes has double vision"),
#             (("zweistein", "sus"), "and is also schitzophrenic"),
#             (("goro", "goro1"), "I SAW WHAT YOU DID TO THAT DOG!"),
#             (("sawman", "sus"), "that was a dog?"),
#             (
#                 ("goro", "goro3"),
#                 "anyways. you have chainsaw hands, do you want to work here?",
#             ),
#             (("zweistein", "sad"), "i mean..."),
#             (("zweistein", "woe"), "we gotta get money somehow"),
#             (("sawman", "angy"), "uhhh"),
#             (("sawman", "sus"), "sure??"),
#             (("goro", "goro2"), "alright, get in here then"),
#         ],
#     ),
# ]

pygame.init()
pygame.mixer.init(22050, -16, 2, 1024)
screen = pygame.display.set_mode(
    (1280, 720),
    # pygame.FULLSCREEN |
    pygame.DOUBLEBUF | pygame.SCALED,
    vsync=1)
keys = pygame.key.get_pressed()

levels = [
    [
        Entity(
            collision=Wall("soi"),
            # movement  = Imovable(),
            movement=RoomMovement(Vector2(0, 0), Rect((0, 0), (1280, 720))),
            interact=NoInteract(),
            render=Room("soi"),
            type=EntityType.ROOM,
            id=1),
        Entity(
            collision=Obstacle(rect=pygame.Rect(10, 20, 100, 200),
                               collideReturn=CollisionType.INTERACT),
            movement=Chaser(0.0, 10, lambda x: x.type == EntityType.PLAYER,
                            Vector2(1200, 700)),
            # movement  = Immovable(position = Vector2(600, 720)),
            interact=Commands(MoveRoomCommand(1, Vector2(500, 520))),
            render=Invisible(),
            type=EntityType.ENTITY,
            id=5,
        ),
        Entity(
            collision=Obstacle(rect=pygame.Rect(10, 20, 50, 200),
                               collideReturn=CollisionType.INTERACT),
            movement=Chaser(0.0, 10, lambda x: x.type == EntityType.PLAYER,
                            Vector2(300, 720)),
            # movement  = Immovable(position = Vector2(600, 720)),
            interact=Commands(
                DialogueCommand(
                    "ono",
                    "zweistein",
                    "...",
                ),
                DialogueCommand(
                    "sus",
                    "sawman",
                    "this is a test of me rewriting this, i am writing more because i need to test multiple lines",
                ), SignalCommand(signal=Signal.OK)),
            render=Sprite("./sprites/npc/contractman.png"),
            type=EntityType.ENTITY,
            id=2,
        ),
    ],
    [
        Entity(collision=Obstacle(rect=pygame.Rect((640, 720), (100, 200)),
                                  collideReturn=CollisionType.NO_OBSTACLE),
               movement=PlayerMovement(position=Vector2(640, 720)),
               interact=NoInteract(),
               render=Spritesheet("./sprites/sawman.png", 100, 239),
               type=EntityType.PLAYER,
               id=0),
        Entity(
            collision=Wall("deadend1"),
            movement=Immovable(),
            # movement=RoomMovement(Vector2(0, 0), Rect((0, 0), (1280, 720))),
            interact=NoInteract(),
            render=Room("deadend1"),
            type=EntityType.ROOM,
            id=1),
        Entity(
            collision=Obstacle(rect=pygame.Rect(10, 20, 100, 200),
                               collideReturn=CollisionType.INTERACT),
            movement=Chaser(0.0, 10, lambda x: x.type == EntityType.PLAYER,
                            Vector2(500, 520)),
            # movement  = Immovable(position = Vector2(600, 720)),
            interact=Commands(MoveRoomCommand(0, Vector2(1200, 700))),
            render=Invisible(),
            type=EntityType.ENTITY,
            id=5,
        ),
        Entity(
            collision=Obstacle(rect=pygame.Rect(10, 20, 50, 200),
                               collideReturn=CollisionType.INTERACT),
            movement=Chaser(0.0, 10, lambda x: x.type == EntityType.PLAYER,
                            Vector2(300, 720)),
            # movement  = Immovable(position = Vector2(600, 720)),
            interact=Commands(
                DialogueCommand(
                    "ono",
                    "zweistein",
                    "...",
                ),
                DialogueCommand(
                    "sus",
                    "sawman",
                    "this is a test of me rewriting this, i am writing more because i need to test multiple lines",
                ), SignalCommand(signal=Signal.OK)),
            render=Sprite("./sprites/npc/contractman.png"),
            type=EntityType.ENTITY,
            id=2,
        ),
    ]
]

world = World(
    tick=0,
    keys=None,
    mouse=None,
    nextLevel=None,
    level=1,
    levels=levels,
    clicked=False,
    animator={},
    commandIndex=0,
    initialTicks=InitialTicks(),
    inDoor=False,
    showInventory=False,
    ui=Overlays(
        {
            "textbox":
            BoxUI(
                COLOR_TERTIARY,
                COLOR_SECONDARY,
                (1, 4),
                BorderRadius(50),
                Rect((20, 20), (0, 0)),
                DirectionUI.VERTICAL,
                rect=Rect((0, 720), (1280, 200)),
                z=4,
                children=[],
            ),
            "name":
            ButtonUI(COLOR_TERTIARY,
                     COLOR_SECONDARY, (0, 2),
                     BorderRadius(40),
                     z=5,
                     rect=Rect((640, 720), (240, 60)),
                     onClick=lambda _: None,
                     children=[]),
            "stats":
            BoxUI(COLOR_TERTIARY,
                  COLOR_SECONDARY, (1, 4),
                  BorderRadius(50, 10, 10, 50),
                  Rect((20, 20), (1, 10)),
                  DirectionUI.VERTICAL,
                  rect=Rect((20, 20), (280, 680)),
                  z=6,
                  children=[]),
            "inventory":
            BoxUI(COLOR_TERTIARY,
                  COLOR_SECONDARY, (1, 10),
                  BorderRadius(10, 50, 50, 10),
                  Rect((20, 20),
                       (1, 10)),
                  DirectionUI.VERTICAL,
                  rect=Rect((320, 20), (940, 680)),
                  z=6,
                  children=[
                      ButtonUI(
                          COLOR_TERTIARY,
                          COLOR_SECONDARY,
                          (1, 4),
                          BorderRadius(10, 50, 50, 10),
                          lambda x: print(f"fish{x}"),
                          children=[
                              SurfaceOverlay(
                                  font_medium.render(f"{x}", FONT_ALIASED,
                                                     COLOR_PRIMARY)),
                              SurfaceOverlay(
                                  font_medium.render(
                                      f"{x}",
                                      FONT_ALIASED,
                                      COLOR_PRIMARY,
                                  ),
                                  align=(AlignUI.CENTER, AlignUI.CENTER),
                              ),
                          ],
                          rect=Rect((0, 0), (1280, 80)),
                      ) for x in range(200)
                  ])
        }, ),
    playerData=PlayerData(
        interactionPoint=Vector2(0, 0),
        deltaPosition=Vector2(0,
                              0),
        positions=Queue(maxsize=16),
        stop=False,
        items={
            "fish":
            Item("fish", 20,
                 lambda world: print(world.ui.overlays["textbox"])),
            "egg":
            Item("egg", 20, lambda world: print(world.ui.overlays["textbox"]))
        }))
