from BaseClasses import MultiWorld


def set_increlution_rules(world: MultiWorld, player: int):

    for location in world.get_locations(player):
        location.access_rule = lambda state: True


def set_increlution_completion(world: MultiWorld, player: int):

    world.completion_condition[player] = lambda state: state.has("Victory", player)