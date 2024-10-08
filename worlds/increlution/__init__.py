import math
from typing import Dict

from BaseClasses import CollectionState, Entrance, Item, Region, Tutorial

from worlds.AutoWorld import WebWorld, World

from .Items import IncrelutionItem, item_table
from .Locations import location_table, IncrelutionLocation
from .Options import IncrelutionOptions, LogicStyle, IncludePassiveJobs
from .Rules import set_increlution_rules, set_increlution_completion
from .info_jobs import jobs
from .info_constructions import constructions
from .info_locations import loc_info


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

    ap_world_version = "0.1.0"


    def generate_early(self):
        """
        In generate early, we fill the item-pool, then determine the number of locations, and add filler items.
        """
        
        
        self.logic_type = -1
        if(self.options.logic_style == LogicStyle.option_free):
            self.logic_type = 1
        if(self.options.logic_style == LogicStyle.option_jobs):
            self.logic_type = 2
        if(self.options.logic_style == LogicStyle.option_full):
            self.logic_type = 3
        
        self.itempool = []
        self.last_chapter = self.options.last_chapter.value + 0.99
        self.number_of_locations = len([expl for expl in loc_info if expl["chapter"] <= self.last_chapter])
        for job_name, job in jobs.items():
            if job["chapter"] <= self.last_chapter:
                if job['skill'] == "Cooking":
                    self.multiworld.push_precollected(self.create_item(f"Progressive {job['skill']} Job"))
                else:
                    self.itempool.append(f"Progressive {job['skill']} Job")
        for c_name, construction in constructions.items():
            if construction["chapter"] <= self.last_chapter:
                if construction['chapter'] == 0:
                    self.multiworld.push_precollected(self.create_item(f"Progressive {construction['skill']} Construction"))
                else:
                    self.itempool.append(f"Progressive {construction['skill']} Construction")
                    
        if self.logic_type >= 2:
            self.multiworld.push_precollected(self.create_item("Progressive Farming Job"))
            self.itempool.remove("Progressive Farming Job")
            self.multiworld.push_precollected(self.create_item("Progressive Woodcutting Job"))
            self.itempool.remove("Progressive Woodcutting Job")
            self.multiworld.push_precollected(self.create_item("Progressive Construction Construction"))
            self.itempool.remove("Progressive Construction Construction")
        if self.logic_type >= 3:
            self.multiworld.push_precollected(self.create_item("Progressive Farming Job"))
            self.itempool.remove("Progressive Farming Job")
            self.multiworld.push_precollected(self.create_item("Progressive Digging Job"))
            self.itempool.remove("Progressive Digging Job")
            self.multiworld.push_precollected(self.create_item("Progressive Fishing Job"))
            self.itempool.remove("Progressive Fishing Job")
            self.multiworld.push_precollected(self.create_item("Progressive Huts Construction"))
            self.itempool.remove("Progressive Huts Construction")
            self.multiworld.push_precollected(self.create_item("Progressive Carts Construction"))
            self.itempool.remove("Progressive Carts Construction")
            self.multiworld.push_precollected(self.create_item("Progressive Progression Construction"))
            self.itempool.remove("Progressive Progression Construction")
            
        perk_names = [
                        "Perk: Generation exp. req.", 
                        "Perk: Instinct exp. req.", 
                        "Perk: Base decay", 
                        "Perk: Decay growth/min", 
                        "Perk: Max health gain",
                        "Perk: Food cooldown", 
                        "Perk: Food value", 
                        "Perk: Combat shield", 
                        "Perk: Completion damage"
                      ]
        
        if self.options.include_passive_jobs == IncludePassiveJobs.option_yes:
            perk_names.append("Perk: Passive jobs")
        
        for i in range(self.options.perks_to_start_with.value):
            for p in perk_names:
                self.multiworld.push_precollected(self.create_item(p))    
        
        for i in range(min(self.options.perks_in_itempool.value * len(perk_names), self.number_of_locations - len(self.itempool) - 1)):
            self.itempool.append(perk_names[i % len(perk_names)])   
            
        if self.number_of_locations - len(self.itempool) - 1 > 0:
            self.itempool += ["Filler"] * (self.number_of_locations - len(self.itempool) - 1)
            
        # for i in range(10):
        #     print(f"if(item == '{perk_names[i]}'){{game[a0_0x3f84('0x101')]['perks'][{i}]['mantissa'] = counts[item];logtext += 'Received {perk_names[i]}\\n'}}")
        

    def create_items(self):        
        self.multiworld.itempool += [self.create_item(name) for name in self.itempool]
        print("itempool", len(self.multiworld.itempool))

    def create_regions(self):
        # simple menu-board construction
        menu = Region("Menu", self.player, self.multiworld)
        board = Region("Board", self.player, self.multiworld)
        
        board.locations = [
            IncrelutionLocation(self.player, loc_name, loc_data.id, board)
            for loc_name, loc_data in location_table.items()
            if loc_data.region == board.name and loc_data.chapter <= self.last_chapter
        ]
        
        # Add the victory item to the correct location.
        victory_location_name = max((loc for loc in loc_info if loc['chapter'] <= self.last_chapter), key=lambda x: x['id'])['name']

        # self.get_location("Explore the area").place_locked_item(self.create_item("Progressive Farming Job"))
        # self.get_location("Explore the cave").place_locked_item(self.create_item("Progressive Woodcutting Job"))
        # self.get_location("Fight cave spider").place_locked_item(self.create_item("Progressive Digging Job"))
        # self.get_location("Explore cave exit").place_locked_item(self.create_item("Progressive Progression Construction"))
        self.get_location(victory_location_name).place_locked_item(self.create_item("Victory"))
        
        print("locations", len(self.multiworld.get_locations(self.player)))

        # add the regions
        connection = Entrance(self.player, "New Board", menu)
        menu.exits.append(connection)
        connection.connect(board)
        self.multiworld.regions += [menu, board]
        

    def set_rules(self):
        """
        set rules per location, and add the rule for beating the game
        """
            
        set_increlution_rules(self.multiworld, self.player, self.logic_type)
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
    
    # def generate_output(self, output_directory: str) -> None:
    #     counts = {}
    #     for job_name, job in jobs.items():
    #         if job["skill"] not in counts:
    #             counts[job["skill"]] = 0
    #         counts[job["skill"]] += 1
    #         print(f"if(item == 'Progressive {job['skill']} Job' && counts[item] == {counts[job['skill']]}){{a0_0x3feeba[{job['id_in_game']}]['shouldShow'] = window.oldJob[{job['id_in_game']}];logtext += 'Received job {job_name}\\n'}}")
    #     counts = {}
    #     for con_name, construction in constructions.items():
    #         if construction["skill"] not in counts:
    #             counts[construction["skill"]] = 0
    #         counts[construction["skill"]] += 1
    #         print(f"if(item == 'Progressive {construction['skill']} Construction' && counts[item] == {counts[construction['skill']]}){{a0_0x81eb24[{construction['id_in_game']}]['shouldShow'] = window.oldCon[{construction['id_in_game']}];logtext += 'Received construction {con_name}\\n'}}")


