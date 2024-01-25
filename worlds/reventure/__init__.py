import string

from BaseClasses import Entrance, Item, ItemClassification, Location, MultiWorld, Region, Tutorial
from .Items import item_table
from .Locations import location_table
from .Options import reventure_options
from .Regions import create_regions
from .Rules import set_rules
from worlds.AutoWorld import WebWorld, World


class ReventureWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Reventure for Archipelago. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        ["Droppel"]
    )]


class ReventureWorld(World):
    """
    An adventure game where you find creative ways to die (And sometimes achieve "victories")
    """

    option_definitions = reventure_options
    game = "Reventure"
    topology_present = False
    data_version = 1
    web = ReventureWeb()
    required_client_version = (0, 4, 0)

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table

    def create_items(self):
        # Fill out our pool with our items from item_pool, assuming 1 item if not present in item_pool
        pool = []
        for name, data in item_table.items():
            item = ReventureItem(name, self.player)
            pool.append(item)

        self.multiworld.itempool += pool

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def create_item(self, name: str) -> Item:
        return ReventureItem(name, self.player)

    def create_regions(self):
        create_regions(self.multiworld, self.player)

    def fill_slot_data(self) -> dict:
        slot_data = {}
        for option_name in reventure_options:
            option = getattr(self.multiworld, option_name)[self.player]
            slot_data[option_name] = option.value
        return slot_data

    def get_filler_item_name(self) -> str:
        return "Filler Item"


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


class ReventureItem(Item):
    game = "Reventure"

    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        super(ReventureItem, self).__init__(
            name,
            ItemClassification.progression if item_data.progression else ItemClassification.filler,
            item_data.code, player
        )
