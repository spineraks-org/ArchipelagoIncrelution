from Options import Range
from dataclasses import dataclass

from Options import PerGameCommonOptions, Range

class LastChapter(Range):
    """
    This option determine until what chapter is included.
    """

    display_name = "Last chapter"
    range_start = 2
    range_end = 2
    default = 2

@dataclass
class IncrelutionOptions(PerGameCommonOptions):
    last_chapter: LastChapter