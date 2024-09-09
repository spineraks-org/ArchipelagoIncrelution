import typing

from BaseClasses import Item, ItemClassification


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification


class IncrelutionItem(Item):
    game: str = "Increlution"


item_table = {
    "Progressive Farming Job": ItemData(11, ItemClassification.progression),
    "Progressive Woodcutting Job": ItemData(12, ItemClassification.progression),
    "Progressive Fishing Job": ItemData(13, ItemClassification.progression),
    "Progressive Cooking Job": ItemData(14, ItemClassification.progression),
    "Progressive Digging Job": ItemData(15, ItemClassification.progression),
    "Progressive Hunting Job": ItemData(16, ItemClassification.progression),
    "Progressive Social Job": ItemData(17, ItemClassification.progression),
    "Progressive Carts Construction": ItemData(21, ItemClassification.progression),
    "Progressive Huts Construction": ItemData(22, ItemClassification.progression),
    "Progressive Construction Construction": ItemData(23, ItemClassification.progression),
    "Progressive Progression Construction": ItemData(24, ItemClassification.progression),
    "Progressive Skill Item Construction": ItemData(25, ItemClassification.progression),
    "Perk: Generation exp. req.": ItemData(101, ItemClassification.useful),
    "Perk: Instinct exp. req.": ItemData(102, ItemClassification.useful),
    "Perk: Base decay": ItemData(103, ItemClassification.useful),
    "Perk: Decay growth/min": ItemData(104, ItemClassification.useful),
    "Perk: Max health gain": ItemData(105, ItemClassification.useful),
    "Perk: Food cooldown": ItemData(106, ItemClassification.useful),
    "Perk: Food value": ItemData(107, ItemClassification.useful),
    "Perk: Combat shield": ItemData(108, ItemClassification.useful),
    "Perk: Completion damage": ItemData(109, ItemClassification.useful),
    "Perk: Passive jobs": ItemData(110, ItemClassification.useful),
    "Victory": ItemData(2345678, ItemClassification.progression),
    "Filler": ItemData(2389423, ItemClassification.filler),
}

