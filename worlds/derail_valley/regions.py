from BaseClasses import Region

from .locations import get_locations

def init_areas(world: "DVWorld", locations) -> None:
    region = Region("Menu", world.player, world.multiworld)
    all_locations = get_locations(world)
    for location in all_locations:
        region.locations.append(location)
    world.multiworld.regions += [region]

