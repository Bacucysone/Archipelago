from typing import Set, List, NamedTuple, Optional
from BaseClasses import ItemClassification, Item

class ItemData(NamedTuple):
    name: str
    classification: ItemClassification
    code: Optional[int]
    amount: int=1

class DVItem(Item):
    game="Derail Valley"

_item_table: List[ItemData] = [
    ItemData("Nothing", ItemClassification.trap, -1, 0),
    ItemData("Money", ItemClassification.filler, 0x1, 0),
    ItemData("Double job token", ItemClassification.useful, 0x2, 0),

    ItemData("AmpLimiter", ItemClassification.filler, 0x100, 0),
    ItemData("AntiWheelslipComputer", ItemClassification.filler, 0x101, 0),
    ItemData("AutomaticTrainStop", ItemClassification.filler, 0x103, 0),
    ItemData("BatteryCharger", ItemClassification.filler, 0x105, 0),
    ItemData("BeaconAmber", ItemClassification.filler, 0x106, 0),
    ItemData("BeaconBlue", ItemClassification.filler, 0x107, 0),
    ItemData("BeaconRed", ItemClassification.filler, 0x108, 0),
    ItemData("Boombox", ItemClassification.filler, 0x109, 0),
    ItemData("BrakeChecklist", ItemClassification.filler, 0x10D, 0),
    ItemData("BrakeCylinderLEDBar", ItemClassification.filler, 0x10E, 0),
    ItemData("Cassette_Album01", ItemClassification.filler, 0x113, 0),
    ItemData("Cassette_Album02", ItemClassification.filler, 0x114, 0),
    ItemData("Cassette_Album03", ItemClassification.filler, 0x115, 0),
    ItemData("Cassette_Album04", ItemClassification.filler, 0x116, 0),
    ItemData("Cassette_Album05", ItemClassification.filler, 0x117, 0),
    ItemData("Cassette_Album06", ItemClassification.filler, 0x118, 0),
    ItemData("Cassette_Album07", ItemClassification.filler, 0x119, 0),
    ItemData("Cassette_Album08", ItemClassification.filler, 0x11A, 0),
    ItemData("Cassette_Album09", ItemClassification.filler, 0x11B, 0),
    ItemData("Cassette_Album10", ItemClassification.filler, 0x11C, 0),
    ItemData("Cassette_Album11", ItemClassification.filler, 0x11D, 0),
    ItemData("Cassette_Album12", ItemClassification.filler, 0x11E, 0),
    ItemData("Cassette_Album13", ItemClassification.filler, 0x11F, 0),
    ItemData("Cassette_Album14", ItemClassification.filler, 0x120, 0),
    ItemData("Cassette_Album15", ItemClassification.filler, 0x121, 0),
    ItemData("Cassette_Album16", ItemClassification.filler, 0x122, 0),
    ItemData("Cassette_Playlist01", ItemClassification.filler, 0x123, 0),
    ItemData("Cassette_Playlist02", ItemClassification.filler, 0x124, 0),
    ItemData("Cassette_Playlist03", ItemClassification.filler, 0x125, 0),
    ItemData("Cassette_Playlist04", ItemClassification.filler, 0x126, 0),
    ItemData("Cassette_Playlist05", ItemClassification.filler, 0x127, 0),
    ItemData("Cassette_Playlist06", ItemClassification.filler, 0x128, 0),
    ItemData("Cassette_Playlist07", ItemClassification.filler, 0x129, 0),
    ItemData("Cassette_Playlist08", ItemClassification.filler, 0x12A, 0),
    ItemData("Cassette_Playlist09", ItemClassification.filler, 0x12B, 0),
    ItemData("Cassette_Playlist10", ItemClassification.filler, 0x12C, 0),
    ItemData("Clinometer", ItemClassification.filler, 0x12D, 0),
    ItemData("Compass", ItemClassification.filler, 0x136, 0),
    ItemData("Crate", ItemClassification.filler, 0x137, 0),
    ItemData("CratePlastic", ItemClassification.filler, 0x138, 0),
    ItemData("CrimpingTool", ItemClassification.filler, 0x139, 0),
    ItemData("DefectDetector", ItemClassification.filler, 0x13D, 0),
    ItemData("DigitalClock", ItemClassification.filler, 0x13E, 0),
    ItemData("DigitalSpeedometer", ItemClassification.filler, 0x13F, 0),
    ItemData("DistanceTracker", ItemClassification.filler, 0x140, 0),
    ItemData("DuctTape", ItemClassification.filler, 0x141, 0),
    ItemData("EOTLantern", ItemClassification.filler, 0x144, 0),
    ItemData("ExpertShovel", ItemClassification.progression, 0x146, 0),
    ItemData("FillerGun", ItemClassification.filler, 0x148, 0),
    ItemData("FlagMarkerBlue", ItemClassification.filler, 0x14A, 0),
    ItemData("FlagMarkerCyan", ItemClassification.filler, 0x14B, 0),
    ItemData("FlagMarkerGreen", ItemClassification.filler, 0x14C, 0),
    ItemData("FlagMarkerOrange", ItemClassification.filler, 0x14D, 0),
    ItemData("FlagMarkerPurple", ItemClassification.filler, 0x14E, 0),
    ItemData("FlagMarkerRed", ItemClassification.filler, 0x14F, 0),
    ItemData("FlagMarkerWhite", ItemClassification.filler, 0x150, 0),
    ItemData("FlagMarkerYellow", ItemClassification.filler, 0x151, 0),
    ItemData("Flashlight", ItemClassification.filler, 0x152, 0),
    ItemData("GoldenShovel", ItemClassification.progression, 0x153, 0),
    ItemData("GooglyEye", ItemClassification.filler, 0x154, 0),
    ItemData("Hammer", ItemClassification.filler, 0x155, 0),
    ItemData("HandDrill", ItemClassification.useful, 0x156, 1),
    ItemData("HandheldGameConsole", ItemClassification.filler, 0x157, 0),
    ItemData("Headlight", ItemClassification.filler, 0x15A, 0),
    ItemData("InfraredThermometer", ItemClassification.filler, 0x15B, 0),
    ItemData("ItemContainerBriefcase", ItemClassification.filler, 0x15C, 0),
    ItemData("ItemContainerCrate", ItemClassification.filler, 0x15D, 0),
    ItemData("ItemContainerFolder", ItemClassification.filler, 0x15E, 0),
    ItemData("ItemContainerFolderBlue", ItemClassification.filler, 0x15F, 0),
    ItemData("ItemContainerFolderRed", ItemClassification.filler, 0x160, 0),
    ItemData("ItemContainerFolderYellow", ItemClassification.filler, 0x161, 0),
    ItemData("ItemContainerToolbox", ItemClassification.filler, 0x163, 0),
    ItemData("Key", ItemClassification.progression, 0x169, 1),
    ItemData("KeyCaboose", ItemClassification.progression, 0x16B, 1),
    ItemData("KeyDE6Slug", ItemClassification.progression, 0x16C, 1),
    ItemData("KeyDM1U", ItemClassification.progression, 0x16D, 1),
    ItemData("LabelMaker", ItemClassification.filler, 0x16F, 0),
    ItemData("Lamp", ItemClassification.filler, 0x170, 0),
    ItemData("Lantern", ItemClassification.filler, 0x171, 0),
    ItemData("LightBarBlue", ItemClassification.filler, 0x1A5, 0),
    ItemData("LightBarCyan", ItemClassification.filler, 0x1A6, 0),
    ItemData("LightBarGreen", ItemClassification.filler, 0x1A7, 0),
    ItemData("LightBarOrange", ItemClassification.filler, 0x1A8, 0),
    ItemData("LightBarPurple", ItemClassification.filler, 0x1A9, 0),
    ItemData("LightBarRed", ItemClassification.filler, 0x1AA, 0),
    ItemData("LightBarWhite", ItemClassification.filler, 0x1AB, 0),
    ItemData("LightBarYellow", ItemClassification.filler, 0x1AC, 0),
    ItemData("lighter", ItemClassification.progression, 0x1AD, 1),
    ItemData("ModernHeadlightL", ItemClassification.filler, 0x1B2, 0),
    ItemData("ModernHeadlightR", ItemClassification.filler, 0x1B3, 0),
    ItemData("ModernTaillightL", ItemClassification.filler, 0x1B4, 0),
    ItemData("ModernTaillightR", ItemClassification.filler, 0x1B5, 0),
    ItemData("Mount70Long", ItemClassification.filler, 0x1B6, 0),
    ItemData("Mount90Square", ItemClassification.filler, 0x1B7, 0),
    ItemData("Mount90SquareBig", ItemClassification.filler, 0x1B8, 0),
    ItemData("Mount90SquareLong", ItemClassification.filler, 0x1B9, 0),
    ItemData("Mount90Wide", ItemClassification.filler, 0x1BA, 0),
    ItemData("MountLong", ItemClassification.filler, 0x1BB, 0),
    ItemData("MountSmall", ItemClassification.filler, 0x1BC, 0),
    ItemData("MountSquare", ItemClassification.filler, 0x1BD, 0),
    ItemData("MountSquareBig", ItemClassification.filler, 0x1BE, 0),
    ItemData("MountSquareVeryLong", ItemClassification.filler, 0x1BF, 0),
    ItemData("MountStandBig", ItemClassification.filler, 0x1C0, 0),
    ItemData("MountVeryLong", ItemClassification.filler, 0x1C1, 0),
    ItemData("Nameplate", ItemClassification.filler, 0x1C4, 0),
    ItemData("Oiler", ItemClassification.progression, 0x1C5, 1),
    ItemData("OverheatingProtection", ItemClassification.filler, 0x1C6, 0),
    ItemData("PaintCan", ItemClassification.filler, 0x1C7, 0),
    ItemData("PaintCan_Museum", ItemClassification.filler, 0x1C8, 0),
    ItemData("PaintCan_Sand", ItemClassification.filler, 0x1C9, 0),
    ItemData("PaintSprayer", ItemClassification.progression, 0x1CD, 1),
    ItemData("ProximityReader", ItemClassification.filler, 0x1D3, 0),
    ItemData("ProximitySensor", ItemClassification.filler, 0x1D4, 0),
    ItemData("RemoteController", ItemClassification.filler, 0x1D7, 0),
    ItemData("RemoteSignalBooster", ItemClassification.filler, 0x1D8, 0),
    ItemData("ShelfSmall", ItemClassification.filler, 0x1DC, 0),
    ItemData("shovel", ItemClassification.progression, 0x1DD, 1),
    ItemData("ShovelMount", ItemClassification.filler, 0x1DE, 0),
    ItemData("SolderingGun", ItemClassification.filler, 0x1DF, 0),
    ItemData("SolderingWireReel", ItemClassification.filler, 0x1E0, 0),
    ItemData("SteamEngineChecklist", ItemClassification.filler, 0x1E2, 0),
    ItemData("StickyTape", ItemClassification.filler, 0x1E3, 0),
    ItemData("Stopwatch", ItemClassification.filler, 0x1E4, 0),
    ItemData("SunVisor", ItemClassification.filler, 0x1E5, 0),
    ItemData("SwitchAlternating", ItemClassification.filler, 0x1E6, 0),
    ItemData("SwitchAnalog", ItemClassification.filler, 0x1E7, 0),
    ItemData("SwitchButton", ItemClassification.filler, 0x1E8, 0),
    ItemData("SwitchLever", ItemClassification.filler, 0x1E9, 0),
    ItemData("SwitchRotary", ItemClassification.filler, 0x1EA, 0),
    ItemData("SwitchSetter", ItemClassification.filler, 0x1EB, 0),
    ItemData("SwivelLight", ItemClassification.filler, 0x1EC, 0),
    ItemData("Taillight", ItemClassification.filler, 0x1EE, 0),
    ItemData("UniversalControlStand", ItemClassification.filler, 0x1F2, 0),
    ItemData("WirelessMUController", ItemClassification.filler, 0x1F5, 0),

    ItemData("CME", ItemClassification.progression, 0x200, 1),
    ItemData("CMS", ItemClassification.progression, 0x201, 1),
    ItemData("CP", ItemClassification.progression, 0x202, 1),
    ItemData("CS", ItemClassification.progression, 0x203, 1),
    ItemData("CW", ItemClassification.progression, 0x204, 1),
    ItemData("FF", ItemClassification.progression, 0x205, 1),
    ItemData("FM", ItemClassification.progression, 0x206, 1),
    ItemData("FRC", ItemClassification.progression, 0x207, 1),
    ItemData("FRS", ItemClassification.progression, 0x208, 1),
    ItemData("GF", ItemClassification.progression, 0x209, 1),
    ItemData("HB", ItemClassification.progression, 0x20A, 1),
    ItemData("IME", ItemClassification.progression, 0x20B, 1),
    ItemData("IMW", ItemClassification.progression, 0x20C, 1),
    ItemData("MB", ItemClassification.progression, 0x20D, 1),
    ItemData("MF", ItemClassification.progression, 0x20E, 1),
    ItemData("OR", ItemClassification.progression, 0x20F, 1),
    ItemData("OWC", ItemClassification.progression, 0x210, 1),
    ItemData("OWN", ItemClassification.progression, 0x211, 1),
    ItemData("SM", ItemClassification.progression, 0x212, 1),
    ItemData("SW", ItemClassification.progression, 0x213, 1),

    ItemData("Dispatcher license", ItemClassification.useful, 0x300, 1),
    ItemData("Train conductor license", ItemClassification.filler, 0x301, 1),
    ItemData("DE2", ItemClassification.progression, 0x302, 1),
    ItemData("DM3", ItemClassification.progression, 0x303, 1),
    ItemData("DH4", ItemClassification.progression, 0x304, 1),
    ItemData("DE6", ItemClassification.progression, 0x305, 1),
    ItemData("S060", ItemClassification.progression, 0x306, 1),
    ItemData("S282", ItemClassification.progression, 0x307, 1),
    ItemData("Multiple unit license", ItemClassification.useful, 0x308, 1),
    ItemData("Museum license", ItemClassification.progression, 0x309, 1),
    ItemData("Manual service license", ItemClassification.progression, 0x30A, 1),
    ItemData("Progressive concurrent license", ItemClassification.progression, 0x30B, 2),

    ItemData("Freight haul license", ItemClassification.progression, 0x310, 1),
    ItemData("Logistical haul license", ItemClassification.progression, 0x311, 1),
    ItemData("Shunting license", ItemClassification.progression, 0x312, 1),
    ItemData("Fragile license", ItemClassification.progression, 0x313, 1),
    ItemData("Progressive long license", ItemClassification.progression, 0x314, 2),
    ItemData("Progressive hazmat license", ItemClassification.progression, 0x315, 3),
    ItemData("Progressive military license", ItemClassification.progression, 0x316, 3),
    

    ItemData("Demo Loco DE2", ItemClassification.progression, 0x350, 2),
    ItemData("Demo Loco DM3", ItemClassification.progression, 0x351, 2),
    ItemData("Demo Loco DH4", ItemClassification.progression, 0x352, 2),
    ItemData("Demo Loco DE6", ItemClassification.progression, 0x353, 2),
    ItemData("Demo Loco S060", ItemClassification.progression, 0x354, 2),
    ItemData("Demo Loco S282", ItemClassification.progression, 0x355, 2),

    ItemData("BE2", ItemClassification.filler, 0x360, 1),
    ItemData("Caboose", ItemClassification.filler, 0x361, 1),
    ItemData("DE6 Slug", ItemClassification.filler, 0x362, 1),
    ItemData("DM1U", ItemClassification.filler, 0x363, 1)
]

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
    return _item_table
def get_filler_items():
    return [x for x in _item_table if x.amount==0 and x.classification == ItemClassification.filler]
def get_starting_items(world: "DVWorld"):
    L = []
    if world.options.dispatcher == 0:
        L.append("Dispatcher license")
    match world.options.start_loco:
        case 0:
            L.append("DE2")
        case 1:
            L.append("DM3")
        case 2:
            L.append("DH4")
        case 3:
            L.append("S060")
        case 4:
            L.append("S282")
        case 5:
            L.append("DE6")
        case 6: # Starter random
            L.append(world.random.choice(["DE2", "DM3", "S060"]))
    if "S060" in L or "S282" in L:
        L.extend(["shovel", "Oiler", "lighter"])
    match world.options.station_licenses:
        case 1:
            all_stations_but_mb = [x for x in world.all_stations if x != "MB"]
            L.append(world.random.choice(all_stations_but_mb))
        case 2:
            L.extend(world.all_stations)
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