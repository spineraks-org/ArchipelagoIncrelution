from BaseClasses import MultiWorld
from .info_locations_logic import location_logic
from .info_locations import locations
from .info_jobs import jobs
from .info_constructions import constructions


def set_increlution_rules(world: MultiWorld, player: int, logic_style: int):

    for location in world.get_locations(player):
        required_items = location_logic[location.name]
        required_items = [item for item in required_items if item]
        
        required_unlocks = []
        
        for item in required_items:
            if item in jobs:
                skill = jobs[item]["skill"]
                id = jobs[item]["id_in_game"]
                required_unlocks.append((f"Progressive {skill} Job", len([j for j in jobs.values() if j["skill"] == skill and j["id_in_game"] <= id])))
            elif item in constructions:
                skill = constructions[item]["skill"]
                id = constructions[item]["id_in_game"]
                required_unlocks.append((f"Progressive {skill} Construction", len([j for j in constructions.values() if j["skill"] == skill and j["id_in_game"] <= id])))            
            else:
                raise LookupError(f"Couldn't find item in jobs or constructions, {item}")
            
        if logic_style > 1:
            for item in jobs:
                if(jobs[item]["chapter"] <= locations[location.name]["chapter"]):
                    skill = jobs[item]["skill"]
                    id = jobs[item]["id_in_game"]
                    required_unlocks.append((f"Progressive {skill} Job", len([j for j in jobs.values() if j["skill"] == skill and j["id_in_game"] <= id])))
            
        if logic_style > 2:
            for item in constructions:
                        if(constructions[item]["chapter"] <= locations[location.name]["chapter"]):
                            skill = constructions[item]["skill"]
                            id = constructions[item]["id_in_game"]
                            required_unlocks.append((f"Progressive {skill} Construction", len([j for j in constructions.values() if j["skill"] == skill and j["id_in_game"] <= id])))
            
        # Dictionary to store the highest value for each job
        job_dict = {}

        # Iterate through the list and update the dictionary with the highest value
        for job, number in required_unlocks:
            if job not in job_dict or number > job_dict[job] and job != "Progressive Cooking Job":
                job_dict[job] = number

        # Convert the dictionary back to a list of tuples
        required_unlocks = list(job_dict.items())
        
        print(f"{location} need {required_unlocks}")
                
        location.access_rule = lambda state, player=player, required_unlocks=required_unlocks: all(state.has(s, player, a) for (s, a) in required_unlocks)


def set_increlution_completion(world: MultiWorld, player: int):

    world.completion_condition[player] = lambda state: state.has("Victory", player)