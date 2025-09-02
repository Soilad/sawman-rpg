from classes import Room, Obj, Portal, Chaser, cwd, Trader

levels = [
    Room(
        "soi",
        "I_forgor_my_wallet",
        0,
        [
            # Obj(
            #     f"{cwd}/sprites/npc/contractman.png",
            #     (480, 280),
            #     [{("Okaruns balls", 0): 3}],
            #     [
            #         [
            #             (("sawman", "ono"), "NO WAY?!?!?!?"),
            #             (("zweistein", "sad"), "wtf"),
            #             (0, "im gonna steal your balls"),
            #             (
            #                 ("sawman", "woe"),
            #                 "YOU CANT JUST STEAL THE PLOT OF DANDADAN CONTRACT",
            #             ),
            #         ],
            #         [
            #             (("zweistein", "sad"), "why tf did u give us okarun's balls"),
            #             (
            #                 0,
            #                 "its gonna take me years to castrate someone with no balls so take this and leave",
            #             ),
            #             (("sawman", "ono"), "..."),
            #             (("sawman", "sad"), "jesus"),
            #         ],
            #     ],
            # ),
            # Obj(
            #     f"{cwd}/sprites/npc/contractman.png",
            #     (800, 300),
            #     [{("Okaruns balls", 0): -2}],
            #     [
            #         [
            #             (("sawman", "ono"), "NO WAY?!?!?!?"),
            #             (("zweistein", "sad"), "wtf"),
            #             (0, "im gonna steal your balls"),
            #             (
            #                 ("sawman", "woe"),
            #                 "YOU CANT JUST STEAL THE PLOT OF DANDADAN CONTRACT",
            #             ),
            #         ],
            #         [
            #             (("zweistein", "sad"), "why tf did u give us okarun's balls"),
            #             (
            #                 0,
            #                 "its gonna take me years to castrate someone with no balls so take this and leave",
            #             ),
            #             (("sawman", "ono"), "..."),
            #             (("sawman", "sad"), "jesus"),
            #         ],
            #     ],
            # ),
        ],
        [Portal((1230 + 1280, 570 + 720), (100, 200), 1, (274, 208))],
        "",
    ),
    Room(
        "field1",
        "I_stole_a_new_one",
        1,
        [
            Obj(
                f"{cwd}/rooms/field1/objects/power.png",
                (0, 0),
                [],
                [
                    [
                        (("zweistein", "sus"), "its like a great man once said"),
                        (("zweistein", "woe"), "with great power"),
                        (("sawman", "hapi"), "comes great electricity bill"),
                    ]
                ],
            ),
            Obj(
                f"{cwd}/rooms/field1/objects/anna.png",
                (650, 240),
                [],
                [
                    [
                        (("sawman", "hapi"), "I"),
                        (
                            ("sawman", "sad"),
                            "dont remember this college being here before",
                        ),
                        (("zweistein", "ono"), "i guess itsa new one"),
                        (("sawman", "hapi"), "hell yea, im old"),
                    ]
                ],
            ),
            Obj(
                f"{cwd}/rooms/field1/objects/acab.png",
                (920, 310),
                [],
                [
                    [
                        (("sawman", "woe"), "why is there a police car outside us"),
                        (("zweistein", "sad"), "i mean"),
                        (("zweistein", "woe"), "atleast its empty"),
                        (("sawman", "angy"), "true"),
                        (("sawman", "sad"), "hopefully it isnt here because of us"),
                    ]
                ],
            ),
        ],
        [
            Portal((1230, 570), (100, 200), 2, (100, 450)),
            Portal((274, 428), (200, 100), 0, (1230, 450)),
        ],
        "",
    ),
    Room(
        "crossway1",
        0,
        1,
        [
            Obj(
                f"{cwd}/sprites/npc/wamen1.png",
                (210, 280),
                [{("Fear Of Women", 0): 1}],
                [
                    [
                        (("sawman", "hapi"), "..."),
                        (("npc", "wamen1"), "..."),
                        (("sawman", "angy"), "..."),
                        (
                            ("zweistein", "sad"),
                            "do you seriously walk up to people and expect them to talk first?",
                        ),
                        (("sawman", "sad"), "let me handle this"),
                        (("sawman", "angy"), "ok sawman"),
                        (("sawman", "ono"), "you can overcome your fears this time"),
                        (("npc", "wamen1"), "..."),
                        (("sawman", "hapi"), "Hi im-"),
                        (("npc", "wamen1"), "i have a boyfriend."),
                        (("sawman", "sad"), "..."),
                        (("zweistein", "hapi"), "that couldve gotten wayy worse"),
                        (0, "*You got gynophobia *"),
                    ],
                    [
                        (
                            ("zweistein", "angy"),
                            "alright, can you tell us what year it is",
                        ),
                        (("npc", "wamen1"), "uhhhh, its 1446"),
                        (("zweistein", "ono"), "My god, we have gone back in time-"),
                        (("sawman", "angy"), "its in the hijri calendar, probably"),
                        (("npc", "wamen1"), "how did you-"),
                        (("sawman", "sus"), "so its probably like 2024 ish"),
                        (("npc", "wamen1"), "2025, but how did you know that?"),
                        (("sawman", "hapi"), "i know some muslims"),
                        (("sawman", "sad"), "or rather, i knew some muslims"),
                        (
                            ("npc", "wamen1"),
                            "oh yea, right. considering the entire government collapsed and all",
                        ),
                        (("zweistein", "ono"), "..."),
                        (("sawman", "ono"), "..."),
                        (("zweistein", "woe"), "..."),
                        (("sawman", "woe"), "AHHH SCARY WOMAN"),
                    ],
                ],
            )
        ],
        [
            Portal((50, 570), (100, 500), 1, (1000, 570)),
            Portal((1230, 370), (100, 500), 3, (50, 570)),
            Portal((640, 470), (300, 100), 4, (50, 380)),
        ],
        "",
    ),
    Room(
        "deadend1",
        0,
        1,
        [
            Obj(
                f"{cwd}/rooms/deadend1/horse.png",
                (403, 250),
                [],
                [
                    [
                        (("zweistein", "hapi"), "horsie!!"),
                        (("zweistein", "ono"), "OHGOD WHAT IS THAT"),
                        (("cutscene", "dark"), "..."),
                        (
                            ("cutscene", "horseman"),
                            "எ-என் வாழ்க்கையை மு-மு-முடித்துக்கொள்.",
                        ),
                        (
                            ("sawman", "ono"),
                            "UHHHHH, CAN I HELP YOU??????????????????????????",
                        ),
                        (("zweistein", "sad"), "..."),
                        (
                            ("zweistein", "angy"),
                            "i dont think we can help him given the state hes in",
                        ),
                        (("sawman", "sus"), "..."),
                    ]
                ],
            )
        ],
        [Portal((50, 570), (100, 200), 2, (1130, 370))],
        "",
    ),
    Room(
        "field2",
        0,
        1,
        [
            Obj(
                f"{cwd}/rooms/field2/objects/foliage.png",
                (806, 353),
                [{("Vodka", 0.5): 1}],
                [
                    [
                        (("sawman", "woe"), "NO WAY, FOILIAGE"),
                        (("zweistein", "sus"), "wait why is there vodka next to it?"),
                        (0, "*you got vodka*"),
                    ],
                    [
                        (("zweistein", "sus"), "gopnik plant?"),
                        (("sawman", "hapi"), "gopnik plant."),
                        (("zweistein", "woe"), "gopnik plant!"),
                    ],
                ],
                False,
            )
        ],
        [
            Portal((150, 830), (400, 100), 2, (640, 250)),
            Portal((1200, 500), (200, 100), 5, (70, 650)),
        ],
        [
            (("sawman", "sad"), "..."),
            (("sawman", "sus"), "we were stuck there for a whole 5 years huh"),
            (
                ("zweistein", "sus"),
                "yea, huh. seems like alot seems to have changed since then and now",
            ),
            (("sawman", "sad"), "i should be happy rn, but i just feel exhausted..."),
        ],
    ),
    Room(
        "field3",
        0,
        1,
        [
            Chaser(
                f"{cwd}/battle/enemies/Amalgam Type C.png",
                (590, 210),
                1,
                10,
                ["Amalgam Type C", 40],
            )
        ],
        [
            Portal((50, 570), (100, 200), 4, (800, 350)),
            Portal((1200, 550), (200, 300), 6, (70, 450)),
        ],
        [
            (("sawman", "woe"), "OH DEAR GOD WHAT IS THAT"),
            (
                ("zweistein", "woe"),
                "ok whatever this dog thing is it definitely wants to kill us",
            ),
            (0, "WASD or arrow keys with enter should make u choose"),
            (0, "and space should execute it"),
            (0, "the inventory is still accessible if u need to reload or-"),
            (("zweistein", "ono"), "AHHHHHH MY KNEEEEE"),
            (0, "heal..."),
        ],
    ),
    Room(
        "shop1",
        0,
        1,
        [],
        [
            Portal((50, 470), (100, 300), 5, (1000, 350)),
            Portal((350, 550), (300, 100), 7, (777, 270)),
        ],
        [
            (("goro", "goro1"), "HEY YOU"),
            (("zweistein", "ono"), "..."),
            (("sawman", "ono"), "hes not talking about us right???"),
            (("goro", "goro2"), "MOTHERFUCKER YOU ARE THE ONLY 2 PEOPLE THERE"),
            (("zweistein", "sad"), "maybe hes has double vision"),
            (("zweistein", "sus"), "and is also schitzophrenic"),
            (("goro", "goro1"), "I SAW WHAT YOU DID TO THAT DOG!"),
            (("sawman", "sus"), "that was a dog?"),
            (
                ("goro", "goro3"),
                "anyways. you have chainsaw hands, do you want to work here?",
            ),
            (("zweistein", "sad"), "i mean..."),
            (("zweistein", "woe"), "we gotta get money somehow"),
            (("sawman", "angy"), "uhhh"),
            (("sawman", "sus"), "sure??"),
            (("goro", "goro2"), "alright, get in here then"),
        ],
    ),
    Room(
        "chainsawshawarma",
        "I_wanna_kms",
        0,
        [
            Trader(
                f"{cwd}/rooms/chainsawshawarma/objects/goro.png",
                (852, 186),
                f"{cwd}/rooms/chainsawshawarma/shop.png",
                {("Shawarma", 20): 90, ("Kebab", 40): 100, ("Falafel Roll", 20): 90},
            ),
            Chaser(
                f"{cwd}/battle/enemies/Shawarma.png",
                (200, 100),
                0,
                0,
                ["Shawarma", 1000],
            ),
        ],
        [Portal((777, 270), (88, 82), 6, (350, 550))],
        [
            (("goro", "goro1"), "HEY YOU"),
            (("zweistein", "ono"), "..."),
            (("sawman", "ono"), "hes not talking about us right???"),
            (("goro", "goro2"), "MOTHERFUCKER YOU ARE THE ONLY 2 PEOPLE THERE"),
            (("zweistein", "sad"), "maybe hes has double vision"),
            (("zweistein", "sus"), "and is also schitzophrenic"),
            (("goro", "goro1"), "I SAW WHAT YOU DID TO THAT DOG!"),
            (("sawman", "sus"), "that was a dog?"),
            (
                ("goro", "goro3"),
                "anyways. you have chainsaw hands, do you want to work here?",
            ),
            (("zweistein", "sad"), "i mean..."),
            (("zweistein", "woe"), "we gotta get money somehow"),
            (("sawman", "angy"), "uhhh"),
            (("sawman", "sus"), "sure??"),
            (("goro", "goro2"), "alright, get in here then"),
        ],
    ),
]
