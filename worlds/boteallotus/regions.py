from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import BoTealLotusWorld

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).


def create_and_connect_regions(world: BoTealLotusWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: BoTealLotusWorld) -> None:
    # Creating a region is as simple as calling the constructor of the Region class.
    intro = Region("CBF Intro", world.player, world.multiworld)
    cbf_bump_intro = Region("CBF Bump Intro", world.player, world.multiworld)

    # Let's put all these regions in a list.
    regions = [intro, cbf_bump_intro]

    # Some regions may only exist if the player enables certain options.
    # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    # if world.options.hammer:
    #     top_middle_room = Region("Top Middle Room", world.player, world.multiworld)
    #     regions.append(top_middle_room)

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def connect_regions(world: BoTealLotusWorld) -> None:
    # We have regions now, but still need to connect them to each other.
    # But wait, we no longer have access to the region variables we created in create_all_regions()!
    # Luckily, once you've submitted your regions to multiworld.regions,
    # you can get them at any time using world.get_region(...).
    cbf_intro = world.get_region("CBF Intro")
    cbf_bump_intro = world.get_region("CBF Bump Intro")
    cbf_cave_entrance = world.get_region("CBF Cave Entrance")

    uc_cave_entrance = world.get_region("UC Cave Entrance")
    uc_ameterasu_area = world.get_region("UC Amaterasu Area")
    uc_shortcut = world.get_region("UC Shortcut")
    uc_main_chamber = world.get_region("UC Main Chamber")
    uc_arena_puzzle = world.get_region("UC Arena Puzzle")
    uc_north_puzzle = world.get_region("UC North Puzzle")
    uc_herder_home = world.get_region("UC Herder Home")

    sc_coast_1 = world.get_region("SC Coast 1")
    sc_coast_2 = world.get_region("SC Coast 2")
    sc_walls = world.get_region("SC Walls")
    sc_tier_1 = world.get_region("SC Tier 1")
    sc_tier_2 = world.get_region("SC Tier 2")
    sc_tier_3 = world.get_region("SC Tier 3")
    sc_fox_house = world.get_region("SC Fox House")

    mf_tea_fields = world.get_region("MF Tea Fields")
    mf_asahi = world.get_region("MF Asahi")
    mf_arena = world.get_region("MF Arena")
    mf_treetops = world.get_region("MF Treetops")
    mf_escort_bride = world.get_region("MF Escort Bride")
    mf_shrine_ceremony = world.get_region("MF Shrine Ceremony")
    mf_boss = world.get_region("MF Boss")
    mf_burrows_entry = world.get_region("MF Burrows Entry")
    mf_maze = world.get_region("MF Maze")

    kb_entrance = world.get_region("KB Entrance")
    kb_bug_nest = world.get_region("KB Bug Nest")
    kb_south = world.get_region("KB South")
    kb_west = world.get_region("KB West")
    
    # The region.connect helper even allows adding a rule immediately.
    # We'll talk more about rule creation in the set_all_rules() function in rules.py.
    cbf_intro.connect(cbf_bump_intro, "Intro to CBF Bump Intro")