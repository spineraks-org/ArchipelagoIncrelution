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
    "Victory": ItemData(2345678, ItemClassification.progression),
    "Filler": ItemData(2389423, ItemClassification.filler),
}