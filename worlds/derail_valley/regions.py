from BaseClasses import Region
from typing import List

from .locations import get_locations, DVLocation


def init_areas(world: "DVWorld") -> List[DVLocation]:
    region = Region("Menu", world.player, world.multiworld)
    all_locations = get_locations(world, region)
    for location in all_locations:
        region.locations.append(location)
    world.multiworld.regions += [region]
    return all_locations

