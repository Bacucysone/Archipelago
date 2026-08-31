## WHAT TO DO
# When prompted, connect to AP server
# RoomInfo package: seed_name
# Login to server using one slotname and required password
# If successful, save the password and check the "connected" packet -> "players" and "checked_locations"
# Should receive an "ItemReceived" packet shortly after -> Update the items pool of the current game
# Try to generate the world for the logic: we need apworld and yaml at this point. If this is not possible, print error message and wait for another try
from enum import Enum
from typing import Optional, Any

from BaseClasses import MultiWorld, CollectionState, Location, Item
from NetUtils import NetworkItem, decode, encode
from Options import PerGameCommonOptions
from Generate import read_weights_yamls
from worlds import AutoWorld
from settings import get_settings
import os, websockets

class LocationState(Enum):
    Unreachable = 0
    Reachable = 1
    Checked = 2
    

class WorldTracker:
    world: MultiWorld
    locations: dict[str, LocationState]
  
    def __init__(self, yaml_path: str, seed: Optional[int], checked_locations: list[int], items: list[NetworkItem]):
        self.world = MultiWorld(1)
        
        yaml_raw = read_weights_yamls(yaml_path)[0]
        game_name = yaml_raw["game"]
        yaml_options = yaml_raw[game_name]
        
        self.world.generation_is_fake = True
        self.world.set_seed(seed, False, None)
        self.world.game = {1: game_name}
        self.world.player_name = yaml_raw["name"]

        world_type = AutoWorld.AutoWorldRegister.world_types[game_name]
        self.world.worlds[1] = world_type(self.world, 1)
        options_dataclass: type[PerGameCommonOptions] = world_type.options_dataclass
        self.world.worlds[1].options = options_dataclass(**yaml_options)

        self.world.set_item_links()
        self.world.state = CollectionState(self.world)
    
        AutoWorld.call_all(self.world, "generate_early")
    
        AutoWorld.call_all(self.world, "create_regions")
    
        AutoWorld.call_all(self.world, "create_items")
    
        AutoWorld.call_all(self.world, "set_rules")
        AutoWorld.call_all(self.world, "connect_entrances")
        AutoWorld.call_all(self.world, "generate_basic")
    
        for item in items:
            self.add_item(item)
        self.locations = {loc.name: LocationState.Checked if loc.address in checked_locations else LocationState.Unreachable for loc in self.world.get_locations(1)}
        self.compute_locations_states()
        
    def compute_locations_states(self):
        for location in self.world.get_reachable_locations(player = 1):
            if self.locations[location.name] == LocationState.Unreachable:
                self.locations[location.name] = LocationState.Reachable
        
    def add_item(self, id: int) -> None:
        self.world.state.add_item(self.world.worlds[1].item_id_to_name[id], 1, 1)
        self.compute_locations_states()
    
    def item_id_to_name(self, id: int) -> str:
        return self.world.worlds[1].item_id_to_name[id]
    
    def check_location(self, id: int) -> None:
        self.locations[self.world.worlds[1].location_id_to_name[id]] = LocationState.Checked
        self.compute_locations_states()
        
        
class MyClient:
    trackers: list[WorldTracker | None]
    currently_tracking: int
    yamls: dict[str, str]
    player_names: list[str]
    seed: Optional[int]
    password: Optional[str]
    buffer_checked_locations: list[int]
    socket: websockets.WebSocketServerProtocol
    
    def __init__(self):
        defaults = get_settings().generator
        self.yamls = {}
        for filename in os.listdir(defaults.player_files_path):
            full_filename = os.path.join(defaults.player_files_path, filename)
            try:
                f_yaml = read_weights_yamls(full_filename)
                self.yamls[f_yaml[0]["name"]] = full_filename
            except Exception:
                continue
        self.buffer_checked_locations = []
        
    async def connect(self):
        address = ""
        port=0
        self.socket = await websockets.connect(address, port=port, ping_timeout=None, ping_interval=None, ssl=None, max_size=16*1024*1024)
    
    def process_packet_received(self, packet: dict[str, Any]) -> None:
        match packet["cmd"]:
            case "RoomInfo":
                try:
                    self.seed = int(packet["seed_name"])
                except ValueError:
                    self.seed = None
            case "Connected":
                self.buffer_checked_locations = packet["checked_locations"]
                
            case "ReceivedItems":
                if self.trackers[self.currently_tracking] is None:
                    self.trackers[self.currently_tracking] = (
                        WorldTracker(self.yamls[self.player_names[self.currently_tracking - 1]], self.seed, self.buffer_checked_locations, packet["items"])
                    )
            case "PrintJson":
                if packet["type"] == "ItemSend" or packet["type"] == "ItemCheat":
                    rec_player = packet["receiving"]
                    if self.trackers[rec_player] is not None:
                        self.trackers[rec_player].add_item(packet["item"]["item"])
                    send_player = packet["item"]["player"]
                    if self.trackers[send_player] is not None:
                        self.trackers[send_player].check_location(packet["item"]["location"])