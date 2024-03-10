from BaseClasses import Entrance, Location, MultiWorld, Region
from .locations import location_table

def create_regions(world: MultiWorld, player: int):

    world.regions += [
        create_region(world, player, 'Menu', None, ['Startbutton']),
        create_region(world, player, 'Reventureworld', [location for location in location_table])
    ]

    # link up our region with the entrance we just made
    world.get_entrance('Startbutton', player).connect(world.get_region('Reventureworld', player))

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