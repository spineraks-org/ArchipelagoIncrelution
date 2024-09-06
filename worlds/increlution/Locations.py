import typing

from BaseClasses import Location
from .info_locations import loc_info

class LocationDict(typing.TypedDict, total=False): 
    name: str 
    chapter: int 
    map: int
    
class LocData(typing.NamedTuple):
    id: int
    region: str
    chapter: int
    
class IncrelutionLocation(Location):
    game: str = "Increlution"

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)

location_table = {entry["name"]: LocData(entry["id"], "Board", entry["chapter"]) for entry in loc_info}