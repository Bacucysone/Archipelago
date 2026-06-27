import json
from typing import Set, List, NamedTuple
from BaseClasses import ItemClassification, Item

class ItemData(NamedTuple):
    name: str
    classification: ItemClassification
    code: int
    category: str | int
    amount: int
    

class DVItem(Item):
    game="Derail Valley"

def get_item_data() -> list[ItemData]:
    def class_parse(c: str) -> ItemClassification:
        if c.endswith("progression"):
            return ItemClassification.progression
        if c.endswith("useful"):
            return ItemClassification.useful
        if c.endswith("trap"):
            return ItemClassification.trap
        return ItemClassification.filler
      
    raw_dict = json.load(open("derail_valley_data.json", "r"))
    ret = []
    for group in raw_dict["items"]:
        offset = 0 if "offset" not in group else int(group["offset"], 16)
        idx = 0
        for item in group["objects"]:
            if "name" not in item:
                idx += 1
                continue
            name_list = [item["name"]]
            changed = True
            while changed:
                changed = False
                new_list = []
                for name in name_list:
                    if "$" in name:
                        changed = True
                        dollar_split = name.split("$(")
                        paren_split = dollar_split[1].split(")")
                        table_name = paren_split[0]
                        new_list.extend([dollar_split[0] + map_name + ")".join(paren_split[1:]) + "$(".join(dollar_split[2:]) for map_name in raw_dict["tables"][table_name]])
                    else:
                        new_list.append(name)
                name_list = new_list

            for name in name_list:
                classification_str = item["classification"] if "classification" in item else group["classification"]
                ret.append(ItemData(
                    name,
                    class_parse(classification_str),
                    item["id"] if "id" in item else offset + idx,
                    group["groupName"],
                    item["amount"] if "amount" in item else 0 if classification_str.startswith("infinite") or classification_str.startswith("trap") else 1
                ))
                idx += 1
    return ret

_item_table: List[ItemData] = get_item_data()

def get_classification(name: str) -> ItemClassification:
    for data in _item_table:
        if name == data.name:
            return data.classification
    return ItemClassification.filler

def get_id(name:str) -> int:
    for data in _item_table:
        if name == data.name:
            return data.code
    return -1

def get_items() -> Set[ItemData]:
    return set(_item_table)
def get_filler_items():
    return [x for x in _item_table if x.amount==0 and x.classification == ItemClassification.filler]
def get_starting_items(world: "DVWorld"):
    L = []
    if world.options.dispatcher == 0:
        L.append("Dispatcher license")
    match world.options.start_loco:
        case 0:
            L.append("DE2 locomotive license")
        case 1:
            L.append("DM3 locomotive license")
        case 2:
            L.append("DH4 locomotive license")
        case 3:
            L.append("S060 locomotive license")
        case 4:
            L.append("S282 locomotive license")
        case 5:
            L.append("DE6 locomotive license")
        case 6: # Starter random
            L.append(world.random.choice(["DE2 locomotive license", "DM3 locomotive license", "S060 locomotive license"]))
    if "S060 locomotive license" in L or "S282 locomotive license" in L:
        L.extend(["Shovel", "Oiler", "Lighter"])
    match world.options.station_licenses:
        case 1:
            all_stations_but_mb = [x for x in world.all_stations_unlock if x != "MB Station unlock"]
            L.append(world.random.choice(all_stations_but_mb))
        case 2:
            L.extend([x for x in world.all_stations_unlock])
    match world.options.start_job:
        case 0:
            L.append("Freight haul license")
        case 1:
            L.append("Shunting license")
        case 2:
            L.append("Logistical haul license")
        case 4:
            pass
        case _:
            L.append(world.random.choice(["Freight haul license", "Shunting license", "Logistical haul license"]))
    return L