from Options import Range
from dataclasses import dataclass

from Options import PerGameCommonOptions, Range, Choice

class LastChapter(Range):
    """
    This option determine until what chapter is included.
    """

    display_name = "Last chapter"
    range_start = 2
    range_end = 11
    default = 2
    
class LogicStyle(Choice):
    """
    Which logic will be used to generate the game. Note that you can only use items when you get the item AND when you can in vanilla.
    Free: just logic for stuff that's strictly required, like bridge.
    Jobs: also logic such that you will have all jobs you would normally have available. You will get some items to start with.
    Full: in this logic you have everything available at the time you would have it vanilla. You will get a lot of items to start with.
    """

    display_name = "Logic style"
    option_free = 1
    option_jobs = 2
    option_full = 3
    default = 3
    
class HowManyPerks(Range):
    """
    If there are locations left to put items in, you can place NG+ perks in there.
    There are 10 different NG+ perks in total.
    This option represents the amount of each type in the itempool.
    Don't worry about putting too many, there won't be more than empty slots.
    TIP: you can also put them in start_inventory to start with some of them.
    """

    display_name = "Number of perks per type"
    range_start = 0
    range_end = 10
    default = 1
    

@dataclass
class IncrelutionOptions(PerGameCommonOptions):
    last_chapter: LastChapter
    logic_style: LogicStyle
    how_many_perks: HowManyPerks
    