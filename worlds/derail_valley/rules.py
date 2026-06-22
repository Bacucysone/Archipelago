from rule_builder.rules import Has, HasAny, HasAll, HasFromList, HasAllCounts, True_, Or
from BaseClasses import Location

from .locations import get_locations

can_operate_steam = HasAll("Oiler", "Lighter") & HasAny("Shovel", "Golden Shovel", "Expert Shovel")

def military(station):
    if station == "MB":
        return Has("Progressive Military license")
    return True_()
def can_operate(loco):
    if loco in ["S060 locomotive license", "S282 locomotive license"]:
        return can_operate_steam & Has(loco)
    return Has(loco)
def set_location_rules(world: "DVWorld", location_table: Location) -> None:
    player = world.player
    transport_job = HasAny("Freight haul license", "Logistical haul license")
    job_license = Has("Shunting license") | transport_job
    all_stations_but_mb = HasAny("CME", "CMS", "CP", "CS", "CW", "FF", "FM", "FRC", "FRS", "GF", "HB", "IME", "IMW", "MF", "OR", "OWC", "OWN", "SM", "SW") # not used
    nb_shunts = world.options.nb_shunts.value
    nb_freights = world.options.nb_freights.value
    can_operate_one_loco = Or(*[can_operate(f"{loco} locomotive license") for loco in world.all_locos])
    can_make_money = job_license & can_operate_one_loco 

    # if world.options.shop > 0:
    #     for i in range(19):
    #         set_rule(world.multiworld.get_location(f"GF shop unique item {i+1}", player), lambda state: can_make_money(state) and state.has("GF", player))
        
    #     for i in range(18):
    #         set_rule(world.multiworld.get_location(f"MF shop unique item {i+1}", player), lambda state: can_make_money(state) and state.has("MF", player))
        
    #     for i in range(11):
    #         set_rule(world.multiworld.get_location(f"HB shop unique item {i+1}", player), lambda state: can_make_money(state) and state.has("HB", player))

    #     for i in range(5):
    #         set_rule(world.multiworld.get_location(f"FF shop unique item {i+1}", player), lambda state: can_make_money(state) and state.has("FF", player))
        
    #     for i in range(26):
    #         set_rule(world.multiworld.get_location(f"CW shop unique item {i+1}", player), lambda state: can_make_money(state) and state.has("CW", player))
    # if world.options.shop > 1:
    #     for i in range(10):
    #         set_rule(world.multiworld.get_location(f"Common shop item {i+1}", player), lambda state: can_make_money(state) and state.has_any(["GF","MF", "HB", "FF", "CW"], player))
    
    # Win condition
    world.set_completion_rule(HasFromList(*("Finish "+station for station in world.all_stations), count=world.options.nb_stations.value))
    
    # Rules for demonstrator locations
    for loc in location_table:
        if loc.address is not None and 0x400 <= loc.address and loc.address < 0x500:
            n = 2 if loc.name[2] in [' ', '/'] else 3
            station = loc.name[:n]
            world.set_rule(world.multiworld.get_location(loc.name, player), HasAll(station+f" Station unlock", "Museum license"))

    # Orders belong to their stations
    for station in world.all_stations:
        for k in range(nb_shunts):
            world.set_rule(world.multiworld.get_location(station+f" shunting order {k+1}", player), can_operate_one_loco & HasAll(station+f" Station unlock", "Shunting license") & military(station))
        for k in range(nb_freights):
            world.set_rule(world.multiworld.get_location(station+f" transport order {k+1}", player), can_operate_one_loco & Has(station+f" Station unlock") & transport_job & military(station))
        
        world.set_rule(world.multiworld.get_location("Finish "+station, player), can_make_money & Has(station+f" Station unlock") & military(station))
    
    for loco in world.all_locos:
        if world.options.nb_locos.value > 0:
            world.set_rule(world.multiworld.get_location(loco+" orders completed", player), can_make_money & can_operate(f"{loco} locomotive license"))
        if world.options.museum_checks == True:
            world.set_rule(world.multiworld.get_location(loco+" relic parts to museum", player), can_make_money & HasAll("Museum license","Demo locomotive "+loco))
            world.set_rule(world.multiworld.get_location(loco+" relic painted", player), can_make_money & HasAllCounts({f"{loco} locomotive license":1, "Paint Sprayer":1, "Manual service license":1, "Museum license":1, "Demo locomotive "+loco: 2}| ({} if True else {"Sand can":2, "Demonstrator Paint Can":2})))
    
    world.set_rule(world.multiworld.get_location("DE2 license", player), can_make_money)
    world.set_rule(world.multiworld.get_location("DM3 license", player), can_make_money)
    world.set_rule(world.multiworld.get_location("DH4 license", player), can_make_money & Has("Progressive Train Length license", 2))
    world.set_rule(world.multiworld.get_location("DE6 license", player), can_make_money & Has("Progressive Concurrent orders license", 2))
    world.set_rule(world.multiworld.get_location("S060 license", player), can_make_money)
    world.set_rule(world.multiworld.get_location("S282 license", player), can_make_money & Has("Progressive Concurrent orders license", 2))
    world.set_rule(world.multiworld.get_location("Dispatcher license", player), can_make_money)
    world.set_rule(world.multiworld.get_location("Manual service license", player), can_make_money & Has("Progressive Train Length license"))
    world.set_rule(world.multiworld.get_location("Multiple unit license", player), can_make_money & Has("Progressive Concurrent orders license"))
    world.set_rule(world.multiworld.get_location("Concurrent 1 license", player), can_make_money)
    world.set_rule(world.multiworld.get_location("Concurrent 2 license", player), can_make_money & Has("Progressive Concurrent orders license"))
    world.set_rule(world.multiworld.get_location("Museum license", player), can_make_money & Has("Manual service license"))
    world.set_rule(world.multiworld.get_location("Train driver license", player), can_make_money)

    world.set_rule(world.multiworld.get_location("Shunting license", player), can_make_money)
    world.set_rule(world.multiworld.get_location("Logistical haul license", player), can_make_money & Has("Progressive Concurrent orders license"))
    world.set_rule(world.multiworld.get_location("Fragile license", player), can_make_money)
    world.set_rule(world.multiworld.get_location("Long 1 license", player), can_make_money)
    world.set_rule(world.multiworld.get_location("Long 2 license", player), can_make_money & Has("Progressive Train Length license"))
    world.set_rule(world.multiworld.get_location("Hazmat 1 license", player), can_make_money & Has("Fragile license"))
    world.set_rule(world.multiworld.get_location("Hazmat 2 license", player), can_make_money & Has("Progressive Hazmat license"))
    world.set_rule(world.multiworld.get_location("Hazmat 3 license", player), can_make_money & Has("Progressive Hazmat license", 2))
    world.set_rule(world.multiworld.get_location("Military 1 license", player), can_make_money)
    world.set_rule(world.multiworld.get_location("Military 2 license", player), can_make_money & Has("Progressive Military license"))
    world.set_rule(world.multiworld.get_location("Military 3 license", player), can_make_money & Has("Progressive Military license", 2))
    world.set_rule(world.multiworld.get_location("Freight haul license", player), can_make_money)

    world.set_rule(world.multiworld.get_location("Opening Steves garage", player), Has("Steve's Garage Key (DE6 Slug)"))
    world.set_rule(world.multiworld.get_location("Opening Reginald garage", player), Has("Reginald's Garage Key (Caboose)"))
    world.set_rule(world.multiworld.get_location("Opening Old Bob garage", player), Has("Old Bob's Garage Key (BE2)"))
    world.set_rule(world.multiworld.get_location("Opening Olaf garage", player), Has("Olaf's Garage Key (DM1U)"))


