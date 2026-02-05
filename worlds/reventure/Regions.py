from BaseClasses import Entrance, Location, MultiWorld, Region
from Options import PerGameCommonOptions
from .Locations import location_table
from .CustomRegions import create_region_graph, parse_region_graph_from_file

def create_regions(options: PerGameCommonOptions, multiworld: MultiWorld, player: int, isExperimental: bool):
    # if isExperimental:
    #     # region_graph = create_region_graph()
    #     region_graph = parse_region_graph_from_file("PlayersExtra/output.reg")

    #     allexits = []
    #     for graph_region in region_graph.regiondict.values():
    #         locations = None
    #         if graph_region.location:
    #             locations = [graph_region.name]
    #         exits = [f"{graph_region.name}={",".join(connection.apitems.apitems)}={connection.region.name}" for connection in graph_region.connections]
    #         allexits += exits
    #         region = create_region(multiworld, player, graph_region.name, locations, exits)
    #         multiworld.regions.append(region)

    #     for exit in allexits:
    #         (name, apitems, target) = exit.split('=')
    #         region = multiworld.get_entrance(exit, player).connect(multiworld.get_region(target, player))
    #     return region_graph

    # Normal creation

    locations = []
    with open("PlayersExtra/location_apstates.txt", 'r') as f:
        lines = f.readlines()
        for line in lines[2:]:
            loc_name = line.split('=')[0]
            if loc_name:
                locations.append(loc_name)
    multiworld.regions += [
        create_region(multiworld, player, 'Menu', None, ['Startbutton']),
        create_region(multiworld, player, 'Reventureworld', locations)
    ]

    # link up our region with the entrance we just made
    multiworld.get_entrance('Startbutton', player).connect(multiworld.get_region('Reventureworld', player))
    return


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, player, world)
    if locations:
        for location in locations:
            loc_id = location_table.get(location, 0)
            location = ReventureLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret

class ReventureLocation(Location):
    game: str = "Reventure"

    def __init__(self, player: int, name: str, address=None, parent=None):
        super(ReventureLocation, self).__init__(player, name, address, parent)
        if address is None:
            self.event = True
            self.locked = True