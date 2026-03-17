from worlds.AutoWorld import WebWorld, World
from typing import Set, List
from BaseClasses import ItemClassification, Tutorial, Item, MultiWorld
import settings, typing, os, threading

from .items import DVItem, get_items, get_classification, get_starting_items, get_filler_items
from .locations import get_locations, get_all_locations_data
from .rules import set_location_rules
from .options import dv_option_groups, DVOptions
from .regions import init_areas
from .options import DVOptions, dv_option_groups
from .patch import DVPatch, create_save

class DVWeb(WebWorld):
    theme = "stone"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Derail Valley randomizer"
        "and connecting to an Archipelago server.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Bacucysone"]
    )
    rich_text_options_doc=True
    option_groups = dv_option_groups
    tutorials = [setup_en]


class DVSettings(settings.Group):
    class PatchFile(settings.UserFilePath):
        """Path of the patch information for the mod"""


class DVWorld(World):
    """Drive a collection of locomotives to earn money, licenses, and find the relic demonstrator locomotives"""
    game = "Derail Valley"
    option_definitions = DVOptions
    data_version=1
    required_client_version=(0,6,0)

    options_dataclass = DVOptions  # options the player can set
    options: DVOptions  # typing hints for option results
    settings: typing.ClassVar[DVOptions]  # will be automatically assigned from type hint
    topology_present = True  # show path to required location checks in spoiler

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.

    all_items = get_items()
    all_locations = get_all_locations_data()

    all_stations = ["CME", "CMS", "CP", "CS", "CW", "FF", "FM", "FRC", "FRS", "GF", "HB", "IME", "IMW", "MB", "MF", "OR", "OWC", "OWN", "SM", "SW"]
    all_locos = ["DE2", "DM3", "DH4", "DE6", "S060", "S282"]
    item_name_to_id = {data.name: data.code for
                       data in all_items}
    location_name_to_id = {loc_type.name: loc_type.code for
                            loc_type in all_locations}
    starting_items: List[Item] = []

    def create_item(self, name:str):
        id = self.item_name_to_id[name]
        classe = get_classification(name)
        return DVItem(name, classe, id, self.player)
        

    def create_regions(self) -> None:
        locations = init_areas(self)
        set_location_rules(self, locations)
    
    def get_excluded_items(self)-> Set[Item]:
        excluded: Set[Item] = set()
        return excluded

    def get_common_items(self, excluded_items: List[Item]) -> List[Item]:
        pool : List[Item] = []
        for data in self.all_items:
            name = data.name
            if name not in excluded_items:
                for _ in range(data.amount):
                    new_item = self.create_item(name)
                    pool.append(new_item)
        return pool

    def get_filler_item_name(self):
        return self.random.choice(get_filler_items()).name

    def pad_items(self, pool: List[Item]) -> None:
        for _ in range(len(self.multiworld.get_unfilled_locations(self.player)) - len(pool)):
            item = self.create_item(self.get_filler_item_name())
            pool.append(item)

    def create_items(self):
        starting_items = get_starting_items(self)
        station_licenses = []
        for item in starting_items:
            if item in self.all_stations:
                station_licenses.append(self.all_stations.index(item))
            self.push_precollected(self.create_item(item))
        if len(station_licenses) == 0:
            station_licenses.append(18)
        self.starting_station = self.random.choice(station_licenses)
        pool = self.get_common_items(starting_items)
        self.pad_items(pool)
        self.multiworld.itempool += pool
    
    def generate_output(self, output_directory: str) -> None:
        patch = DVPatch(self, self.multiworld.get_out_file_name_base(self.player)+".save", output_directory, self.player)
        patch.write()
        # paky = create_save(self, os.path.join(output_directory, self.multiworld.get_out_file_name_base(self.player)+".save"))
        # paky.write_to_file()


