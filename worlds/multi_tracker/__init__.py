from worlds import LauncherComponents
from BaseClasses import CollectionState, MultiWorld

LauncherComponents.components.append(LauncherComponents.Component("Multi-tracker"))

class TrackerLogic:
    def __init__(self):
        self.multiworld = MultiWorld()
        