from dataclasses import dataclass
from Options import (Toggle, PerGameCommonOptions, OptionGroup, Choice, Range)

class Dispatcher(Choice):
    """Choose what to do with dispatcher license:
        From start: you get it by the start of the game
        Non randomized: it will not be randomized and can be bought with $10.000
        Randomized: it can be anywhere (WARNING: it can be put anywhere in the multiworld)
    """
    display_name = "Dispatcher license"
    option_from_start = 0
    option_non_randomized = 1
    option_randomized = 2
    default = 1

class StartingMoney(Range):
    """How much money you start with"""
    display_name="Starting money"
    range_start=0
    range_end=1000000
    default=2000

class StationLicenses(Choice):
    """ By logic, you are required to acquire a station license to perform
    activities in its proximity (Discover restoration loco points, starting jobs, buying
    in shops when applicable). 
     - No licenses: Makes it so that station licenses are not needed (gives you them all)
     - Start with one: Start with at least one at random so you can play the game (except MB)
     - All random: No restriction (WARNING: your first station license can be anywhere)"""
    display_name="Station licenses"
    option_all_random = 0
    option_start_with_one = 1
    option_no_licenses = 2
    default = 1

class StartLocoLicenses(Choice):
    """ Choose which train license you want to start:
     - One of the 6 locomotives: straightforward
     - Starting random: start at random with one of DE2, DM3 or S060
     - Full random: No restriction (WARNING your first loco license can be anywhere)"""
    display_name="Starting loco license"
    option_de2 = 0
    option_dm3 = 1
    option_dh4 = 2
    option_s060 = 3
    option_s282 = 4
    option_de6 = 5
    option_starting_random = 6
    option_full_random = 7
    default = 6

class NbShuntings(Range):
    """How many shuntings give unique items"""
    display_name="Number of shunting jobs locations"
    range_start=1
    range_end=10
    default=7
class NbLocos(Range):
    """One of the locations is to perform a given number
    of jobs using each locomotive (6 checks)."""
    display_name="Number of jobs required for a check per loco"
    range_start=0
    range_end=20
    default=5

class NbFreights(Range):
    """How many transport jobs give unique items"""
    display_name="Number of transport jobs locations"
    range_start=1
    range_end=10
    default=3

# class RandoShops(Choice):
#     """ Choose how are the shops randomized:
#      - Not randomized: every item will be at its location
#      - Unique items: All unique items (sold only in one shop) are randomized (79 checks)
#      - All items: All items (including consumables) will be randomized (79+ checks)"""
#     option_no=0
#     option_unique = 1
#     option_full = 2

class NbJobs(Range):
    """To win the randomizer, you will need to perform at least N shunting or
    transport jobs from M stations. Here you choose N."""
    display_name="Number of jobs required to finish a station"
    range_start=1
    range_end=40
    default=7

class NbStations(Range):
    """To win the randomizer, you will need to perform at least N shunting or
    transport jobs from M stations. Here you choose M."""
    display_name="Number of finished stations required to beat the game"
    range_start=1
    range_end=20
    default=7

class StartJobLicenses(Choice):
    """Choose your starting job license
     - One of the three: straightforward
     - One random: choose one at random
     - No restriction: WARNING your first job license may be anywhere"""
    display_name="Starting loco license"
    option_transport = 0
    option_shunting = 1
    option_logistical_haul = 2
    option_one_random = 3
    option_no_restriction = 4
    default=3

# class ShopHint(Choice):
#     """Choose what is displayed as description of AP shop item
#     (no effect is shop is not randomized)
#     - Always hint: AP Item will tell you what item it is
#     - Can buy hint: AP Item will tell you what item it is only if you have the appropriate station license
#     - Never hint: AP Item will tell you what item it is only when you buy it
#     """
#     option_always_hint=0
#     option_can_buy_hint = 1
#     option_never_hint = 2
#     default = 1


@dataclass
class DVOptions(PerGameCommonOptions):
    dispatcher: Dispatcher
    start_loco: StartLocoLicenses
    station_licenses: StationLicenses
    money: StartingMoney
    nb_jobs: NbJobs
    nb_stations: NbStations
    nb_freights: NbFreights
    nb_shunts: NbShuntings
    nb_locos: NbLocos
    #shop: RandoShops
    start_job: StartJobLicenses
    #shop_hint: ShopHint

dv_option_groups = [
    OptionGroup("End goal", [
        NbJobs,
        NbStations
    ]), 
    OptionGroup("Licenses", [
        Dispatcher,
        StartLocoLicenses,
        StationLicenses,
        StartJobLicenses
    ]),
    OptionGroup("Game preferences", [
        StartingMoney
    ]),
    OptionGroup("Randomizer preferences", [
        NbFreights,
        NbShuntings,
        NbLocos,
        #RandoShops
    ]),
    # OptionGroup("Hint policy", [
    #     ShopHint
    # ])
    
]
