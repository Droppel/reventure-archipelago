from BaseClasses import MultiWorld

def create_regions(world: MultiWorld, player: int):
    from . import create_region
    from .Locations import location_table

    world.regions += [
        create_region(world, player, 'Menu', None, ['Startbutton']),
        create_region(world, player, 'Reventureworld', [location for location in location_table])
    ]

    # link up our region with the entrance we just made
    world.get_entrance('Startbutton', player).connect(world.get_region('Reventureworld', player))
