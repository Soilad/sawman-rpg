# u gotta arrange the key items alphabetically by names for it to work
# make the most important value item first so it shows up
recipies = {
    (("Nitric Acid", -1), ("Silver", -1)): ("Silver Nitrate", -1),
    (("Paper", -1), ("Silver Nitrate", -1)): ("Film", -1),
    (("Camera", 0), ("Film", -1)): [("Exposed Film", -1), ("Camera", 0)],
    (("Exposed Film", -1), ("Water", 1)): [("Photograph", -1), ("Silver Nitrate", -1)],
    (("Alcohol", -1), ("Water", 1)): ("Vodka", 0.5),
    (("Sodium Hydroxide", -1), ("Water", 1)): ("NaOH Solution", -1),
    (("Electrolysis Setup", 0), ("NaOH Solution", -1)): [
        ("Hydrogen", -1),
        ("Oxygen", -1),
        ("Electrolysis Setup", 0),
    ],
    (("Hydrogen", -1), ("Oxygen", -1)): ("Oxyhydrogen Gas", -5),
    (("Alcohol", -1), ("Sodium Hydroxide", -1)): ("Alcoholic NaOH", -1),
    (("Alcoholic NaOH", -1), ("Oil", 1)): [("Glycerin", -1), ("Biodiesel", -1)],
    (("Nitric Acid", -1), ("Sulphuric Acid", -1)): ("Nitration Bath", -1),
    (("Glycerin", -1), ("Nitration Bath", -1)): ("Nitroglycerin", -200),
}
