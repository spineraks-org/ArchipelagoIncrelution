import math
from typing import Dict

from BaseClasses import CollectionState, Entrance, Item, Region, Tutorial

from worlds.AutoWorld import WebWorld, World

from .Items import IncrelutionItem, item_table
from .Locations import location_table, IncrelutionLocation, loc_info
from .Options import IncrelutionOptions
from .Rules import set_increlution_rules, set_increlution_completion
from .Unlocks import jobs, constructions


class IncrelutionWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Yacht Dice. This guide covers single-player, multiworld, and website.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Spineraks"],
        )
    ]


class IncrelutionWorld(World):
    """
    Yacht Dice is a straightforward game, custom-made for Archipelago,
    where you cast your dice to chart a course for high scores,
    unlocking valuable treasures along the way.
    Discover more dice, extra rolls, multipliers,
    and unlockable categories to navigate the depths of the game.
    Roll your way to victory by reaching the target score!
    """

    game: str = "Increlution"
    options_dataclass = IncrelutionOptions

    web = IncrelutionWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}

    location_name_to_id = {name: data.id for name, data in location_table.items()}

    ap_world_version = "0.001"


    def generate_early(self):
        """
        In generate early, we fill the item-pool, then determine the number of locations, and add filler items.
        """
        self.itempool = []
        self.last_chapter = self.options.last_chapter.value
        self.number_of_locations = len([expl for expl in loc_info if expl["chapter"] <= self.last_chapter])
        for job in jobs:
            if job["chapter"] <= self.last_chapter:
                self.itempool.append(f"Progressive {job['skill']} Job")
        for construction in constructions:
            if job["chapter"] <= self.last_chapter:
                self.itempool.append(f"Progressive {job['skill']} Construction")
        self.itempool += ["Filler"] * (self.number_of_locations - len(self.itempool) - 1)       
        

    def create_items(self):        
        self.multiworld.itempool += [self.create_item(name) for name in self.itempool]

    def create_regions(self):
        # call the ini_locations function, that generates locations based on the inputs.
        # simple menu-board construction
        menu = Region("Menu", self.player, self.multiworld)
        board = Region("Board", self.player, self.multiworld)
        
        board.locations = [
            IncrelutionLocation(self.player, loc_name, loc_data.id, board)
            for loc_name, loc_data in location_table.items()
            if loc_data.region == board.name and loc_data.chapter <= self.last_chapter
        ]
        
        locs = [f"{loc_name} {loc_data.chapter}"
            for loc_name, loc_data in location_table.items()
            if loc_data.region == board.name and loc_data.chapter <= self.last_chapter]
        
        # Add the victory item to the correct location.
        victory_location_name = max((loc for loc in loc_info if loc['chapter'] <= self.last_chapter), key=lambda x: x['id'])['name']

        self.get_location(victory_location_name).place_locked_item(self.create_item("Victory"))

        # add the regions
        connection = Entrance(self.player, "New Board", menu)
        menu.exits.append(connection)
        connection.connect(board)
        self.multiworld.regions += [menu, board]
        

    def set_rules(self):
        """
        set rules per location, and add the rule for beating the game
        """
        set_increlution_rules(self.multiworld, self.player)
        set_increlution_completion(self.multiworld, self.player)

    def fill_slot_data(self):
        """
        make slot data, which consists of yachtdice_data, options, and some other variables.
        """
        slot_data = {}
        slot_data["last_chapter"] = self.options.last_chapter.value
        return slot_data

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = IncrelutionItem(name, item_data.classification, item_data.code, self.player)
        return item
