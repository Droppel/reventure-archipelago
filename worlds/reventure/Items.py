import typing

from BaseClasses import Item
from typing import Dict

reventureOffset = 900270000

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    event: bool = False
    special: bool = False

item_table: Dict[str, ItemData] = {
    'Nothing': ItemData(reventureOffset, False),
    #Sword
    'Progressive Sword': ItemData(reventureOffset+1, True, special=True),
    # UNUSED 'SpawnSwordChest': ItemData(reventureOffset+2, True),
    #Item Locations
    'Shovel': ItemData(reventureOffset+3, True),
    'Boomerang': ItemData(reventureOffset+4, True),
    'Map': ItemData(reventureOffset+5, True),
    'Compass': ItemData(reventureOffset+6, True),
    'Whistle': ItemData(reventureOffset+7, True),
    'Burger': ItemData(reventureOffset+8, True),
    'Dark Stone': ItemData(reventureOffset+9, True),
    'Hook': ItemData(reventureOffset+10, True),
    'Fishing Rod': ItemData(reventureOffset+11, True),
    'Lava Trinket': ItemData(reventureOffset+12, True),
    'Mister Hugs': ItemData(reventureOffset+13, True),
    'Bombs': ItemData(reventureOffset+14, True),
    'Shield': ItemData(reventureOffset+15, True),
    'Nuke': ItemData(reventureOffset+16, True),
    'Princess': ItemData(reventureOffset+17, True),
    'Anvil': ItemData(reventureOffset+18, True),
    'Strawberry': ItemData(reventureOffset+19, True),
    
    #Transportation/Paths
    'Shop Cannon': ItemData(reventureOffset+20, True),
    'Castle To Shop Cannon': ItemData(reventureOffset+21, True),
    'Dark Fortress Cannon': ItemData(reventureOffset+22, True),
    'Castle To Dark Fortress Cannon': ItemData(reventureOffset+23, True),
    'Desert Geyser East': ItemData(reventureOffset+24, True),
    'Desert Geyser West': ItemData(reventureOffset+25, True),
    'Volcano Geyser': ItemData(reventureOffset+26, True), 
    'Waterfall Geyser': ItemData(reventureOffset+27, True),
    'Elevator Button': ItemData(reventureOffset+28, True),
    'Call Elevator Buttons': ItemData(reventureOffset+29, True),
    'Mirror Portal': ItemData(reventureOffset+30, True),
    'Fairy Portal': ItemData(reventureOffset+31, True),
    'Vine': ItemData(reventureOffset+32, True),
    'Open Castle Floor': ItemData(reventureOffset+33, True),
    'Faceplant Stone': ItemData(reventureOffset+34, True),
    'Sewer Pipe': ItemData(reventureOffset+35, True),
    'Dark Stone Lever Left': ItemData(reventureOffset+36, True),
    'Dark Stone Lever Middle': ItemData(reventureOffset+37, True),
    'Dark Stone Lever Right': ItemData(reventureOffset+38, True),

    #NPCs
    'Dragon': ItemData(reventureOffset+39, True),
    'Shopkeeper': ItemData(reventureOffset+40, True),
    'Mimic': ItemData(reventureOffset+41, True),
    'King': ItemData(reventureOffset+42, True),
    'Chicken': ItemData(reventureOffset+43, True, special=True),
    'Elder': ItemData(reventureOffset+44, True),
    'Boulder': ItemData(reventureOffset+45, True),
    
    #Cosmetic
    'Closet': ItemData(reventureOffset+46, False),
    'Princess Statue': ItemData(reventureOffset+47, True),
    'PC': ItemData(reventureOffset+48, False),
    'Dolphins': ItemData(reventureOffset+49, False),
    'Mimic Pet': ItemData(reventureOffset+50, False),

    #Gem
    'Gem': ItemData(reventureOffset+51, True, special=True),

    #Ending
    'Victory': ItemData(None, True, True),
}

event_item_pairs: Dict[str, str] = {
    "100: The End": "Victory",
}
