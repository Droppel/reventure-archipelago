from random import choice
import string

from BaseClasses import Entrance, Item, ItemClassification, Location, MultiWorld, Region, Tutorial
from .items import item_table, event_item_pairs, filler_items
from .locations import location_table
from .options import reventure_options
from .regions import create_regions
from .rules import set_rules
from worlds.AutoWorld import WebWorld, World


class ReventureWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Reventure for Archipelago. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "reventure_en.md",
        "reventure/en",
        ["Droppel"]
    )]


class ReventureWorld(World):
    """
    An adventure game where you find creative ways to die (And sometimes win)
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
        total_location_count = len(self.multiworld.get_unfilled_locations(self.player)) - len(event_item_pairs)
        for name, data in item_table.items():
            if data.event or data.special or data.filler: # Skip Events, Special items and Filler items
                continue
            item = ReventureItem(name, self.player)
            pool.append(item)

        # Add Chicken
        pool.append(self.create_item("Chicken"))
        pool.append(self.create_item("Chicken"))
        pool.append(self.create_item("Chicken"))
        pool.append(self.create_item("Chicken"))

        # Add Swords
        pool.append(self.create_item("Progressive Sword"))
        pool.append(self.create_item("Progressive Sword"))
        if self.options.treasureSword:
            pool.append(self.create_item("Progressive Sword"))
        
        # Handle Gems
        if self.options.randomizeGems:
            for _ in range(0, self.options.gemsInPool):
                pool.append(self.create_item("Gem"))

        # Fill pool with filler items
        for _ in range(0, total_location_count - len(pool)):
            pool.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += pool

        # Final Goal Event
        for event, item in event_item_pairs.items():
            event_item = ReventureItem(item, self.player)
            self.multiworld.get_location(event, self.player).place_locked_item(event_item)

    def set_rules(self):
        set_rules(self.options, self.multiworld, self.player)

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
        return choice(filler_items)


class ReventureItem(Item):
    game = "Reventure"

    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        super(ReventureItem, self).__init__(
            name,
            ItemClassification.progression if item_data.progression else ItemClassification.filler,
            item_data.code, player
        )
