from typing import NamedTuple, Optional, List
from BaseClasses import Location, ItemClassification, Region

from .items import get_id, get_starting_items, DVItem

class DVLocationData(NamedTuple):
    name: str
    code: int
    region: str

class DVLocation(Location):
    game: str = "Derail Valley"

all_stations = ["CME", "CMS", "CP", "CS", "CW", "FF", "FM", "FRC", "FRS", "GF", "HB", "IME", "IMW", "MB", "MF", "OR", "OWC", "OWN", "SM", "SW"]

def get_locations(world: "DVWorld", region: Region) -> List[DVLocation]:
    locos = ["DE2", "DM3", "DH4", "DE6", "S060", "S282"]
    all_locations_data = get_all_locations_data()
    ret = []
    # match world.options.shop:
    #     case 0:
    #         pass
    #     case 1:
    #         ret.extend([DVLocation(world.player, loc.name, loc.code, "Shop") for loc in all_locations_data if 0x100 <= loc.code and loc.code < 0x400])
    #     case 2:
    #         ret.extend([DVLocation(world.player, loc.name, loc.code, "Shop") for loc in all_locations_data if 0x50 <= loc.code and loc.code < 0x400])
    for k, station in enumerate(world.all_stations):
        for i in range(world.options.nb_shunts.value):
            ret.append(DVLocation(world.player, f"{station} shunting n°{i+1}", 0x1000+0x100*k+i, region))
        for i in range(world.options.nb_freights.value):
            ret.append(DVLocation(world.player, f"{station} transport job n°{i+1}", 0x2500+0x100*k+i, region))
    ret.extend([DVLocation(world.player, loc.name, loc.code, region) for loc in all_locations_data if 0x400 <= loc.code and loc.code < 0x700])
    for station in all_stations:
        end_station = DVLocation(world.player, "Finish "+station, None, region)
        end_station.place_locked_item(DVItem("Finish "+station, ItemClassification.progression, None, world.player))
        ret.append(end_station)

    return ret

def get_all_locations_data() -> List[DVLocationData]:
    location_table: List[DVLocationData] = []
    for i in range(10):
        location_table.append(DVLocationData(f"Common shop item {i+1}", 0x50+i, "Shop"))
    #GF shop
    for i in range(19):
        location_table.append(DVLocationData(f"GF shop unique item {i+1}", 0x100+i, "ShopGF"))
    #MF shop
    for i in range(18):
        location_table.append(DVLocationData(f"MF shop unique item {i+1}", 0x150+i, "ShopMF"))
    #HB shop
    for i in range(11):
        location_table.append(DVLocationData(f"HB shop unique item {i+1}", 0x200+i, "ShopHB"))
    #FF shop
    for i in range(5):
        location_table.append(DVLocationData(f"FF shop unique item {i+1}", 0x250+i, "ShopFF"))
    #CW shop
    for i in range(26):
        location_table.append(DVLocationData(f"CW shop unique item {i+1}", 0x300+i, "ShopCW"))

    #Demo Locos
    location_table.extend([
        DVLocationData("CP Shed / A6S", 0x400, "Museum"),
		DVLocationData("CME green building", 0x401, "Museum"),
		DVLocationData("CP Shed / A4S", 0x402, "Museum"),
		DVLocationData("CP / A6S North", 0x403, "Museum"),
		DVLocationData("CMS / A2L", 0x404, "Museum"),
		DVLocationData("SM Service Shed", 0x405, "Museum"),
		DVLocationData("GF Loco Spawn Shed right", 0x406, "Museum"),
		DVLocationData("IME / A1L", 0x407, "Museum"),
		DVLocationData("HB Loco Spawn", 0x408, "Museum"),
		DVLocationData("HB D yard Shed", 0x409, "Museum"),
		DVLocationData("IMW / B8L North", 0x40A, "Museum"),
		DVLocationData("GF /A3S", 0x40B, "Museum"),
		DVLocationData("CP / A6S South", 0x40C, "Museum"),
		DVLocationData("FRS / B1L", 0x40D, "Museum"),
		DVLocationData("SM / A6I", 0x40E, "Museum"),
		DVLocationData("HB Shop", 0x40F, "Museum"),
		DVLocationData("FF B yard", 0x410, "Museum"),
		DVLocationData("GF South exit", 0x411, "Museum"),
		DVLocationData("CW Plaza B yard", 0x412, "Museum"),
		DVLocationData("HB Roundhouse", 0x413, "Museum"),
		DVLocationData("OWC / A1L", 0x414, "Museum"),
		DVLocationData("CP / A4S", 0x415, "Museum"),
		DVLocationData("SM / A4S", 0x416, "Museum"),
		DVLocationData("SW / C1O Shed", 0x417, "Museum"),
		DVLocationData("GF / C1SP", 0x418, "Museum"),
		DVLocationData("HB / F4SP", 0x419, "Museum"),
		DVLocationData("FF C yard between buildings", 0x41A, "Museum"),
		DVLocationData("GF Loco Spawn Shed left", 0x41B, "Museum"),
		DVLocationData("MF Roundhouse East", 0x41C, "Museum"),
		DVLocationData("OWN Service Shed", 0x41D, "Museum"),
		DVLocationData("CW / C6L", 0x41E, "Museum"),
		DVLocationData("CS / A1LP", 0x41F, "Museum"),
		DVLocationData("OR / A4S", 0x420, "Museum"),
		DVLocationData("CW/OWC middle triangle", 0x421, "Museum"),
		DVLocationData("CW NE of B yard", 0x422, "Museum"),
		DVLocationData("SM / A3S", 0x423, "Museum"),
		DVLocationData("FM / A3L", 0x424, "Museum"),
		DVLocationData("IMW / B8L South", 0x425, "Museum"),
		DVLocationData("OR / A6S", 0x426, "Museum"),
		DVLocationData("FF / D1L", 0x427, "Museum"),
		DVLocationData("FF Service shed", 0x428, "Museum"),
		DVLocationData("CMS brick building", 0x429, "Museum"),
		DVLocationData("FF Turntable", 0x42A, "Museum"),
		DVLocationData("CS Museum", 0x42B, "Museum"),
		DVLocationData("IMW SE of Office", 0x42C, "Museum"),
		DVLocationData("CP / A1S", 0x42D, "Museum"),
		DVLocationData("HB D yard shed", 0x42E, "Museum"),
		DVLocationData("SM W/ A7L 1", 0x42F, "Museum"),
		DVLocationData("HB F yard East", 0x430, "Museum"),
		DVLocationData("OR / B7S", 0x431, "Museum"),
		DVLocationData("OR / A3S", 0x432, "Museum"),
		DVLocationData("SM / A7L 2", 0x433, "Museum"),
		DVLocationData("MF Roundhouse East 2", 0x434, "Museum"),
		DVLocationData("FRC C yard North", 0x435, "Museum"),
		DVLocationData("CW East exit", 0x436, "Museum"),
		DVLocationData("CME Coal Mine", 0x437, "Museum"),
		DVLocationData("MF Roundhouse West", 0x438, "Museum") ])

    
    for i, station in enumerate(all_stations):
        location_table.extend([DVLocationData(f"{station} shunting n°{k+1}", 0x2000+0x100*i+k, "Shunting jobs") for k in range(10)])
        location_table.extend([DVLocationData(f"{station} transport job n°{k+1}", 0x4000+i*0x100+k, "Transport jobs") for k in range(10)])
    
    all_locos = ["DE2", "DM3", "DH4", "DE6", "S060", "S282"]
    for i, loco in enumerate(all_locos):
        location_table.append(DVLocationData(loco+" nb of jobs", 0x600+i, "Loco jobs"))
        location_table.append(DVLocationData(loco+" relic parts to museum", 0x620+i, "Museum"))
        location_table.append(DVLocationData(loco+" relic painted", 0x630+i, "Museum"))
    location_table.extend([
        DVLocationData("DE2 license", 0x660, "Start"),#G
        DVLocationData("DM3 license", 0x661, "Start"),#G
        DVLocationData("DH4 license", 0x662, "Intermediate license"),#G
        DVLocationData("DE6 license", 0x663, "Advanced license"),#G
        DVLocationData("S060 license", 0x664, "Start"),#G
        DVLocationData("S282 license", 0x665, "Advanced license"),#G
    ])#G

    #Licenses
    location_table.append(DVLocationData("Dispatcher license", 0x66B, "Menu"))#G

    location_table.extend([
        DVLocationData("Manual service license", 0x666, "Intermediate license"),#G
        DVLocationData("Multiple unit license", 0x667, "Intermediate license"),#G
        DVLocationData("Concurrent 1 license", 0x668, "Start"),#G
        DVLocationData("Concurrent 2 license", 0x669, "Intermediate license"),#G
        DVLocationData("Museum license", 0x66A, "Advanced license"),#G
        DVLocationData("Train driver license", 0x66C, "Start"),#G
        DVLocationData("Shunting license", 0x670, "Start"),
        DVLocationData("Logistical haul license", 0x671, "Intermediate license"),
        DVLocationData("Fragile license", 0x672, "Start"),
        DVLocationData("Long 1 license", 0x673, "Start"),
        DVLocationData("Long 2 license", 0x674, "Intermediate license"),
        DVLocationData("Hazmat 1 license", 0x675, "Intermediate license"),
        DVLocationData("Hazmat 2 license", 0x676, "Intermediate license"),
        DVLocationData("Hazmat 3 license", 0x677, "Advanced license"),
        DVLocationData("Military 1 license", 0x678, "Start"),
        DVLocationData("Military 2 license", 0x679, "Intermediate license"),
        DVLocationData("Military 3 license", 0x67A, "Advanced license"),
        DVLocationData("Freight haul license", 0x67B, "Start"),
    ])

    #Hidden garages
    location_table.extend([
        DVLocationData("Opening Steves garage", 0x690, "Start"),
        DVLocationData("Opening Reginald garage", 0x691, "Start"),
        DVLocationData("Opening Old Bob garage", 0x692, "Start"),
        DVLocationData("Opening Olaf garage", 0x693, "Start"),
    ])

    return location_table