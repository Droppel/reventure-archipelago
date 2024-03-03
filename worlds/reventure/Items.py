import typing

from BaseClasses import Item
from typing import Dict

reventureOffset = 900270000

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    event: bool = False
    gem: bool = False

item_table: Dict[str, ItemData] = {
    #Item Locations
    'Nothing': ItemData(reventureOffset, False),
    'SpawnSwordPedestalItem': ItemData(reventureOffset+1, True),
    'SpawnSwordChest': ItemData(reventureOffset+2, True),
    'SpawnShovelChest': ItemData(reventureOffset+3, True),
    'SpawnBoomerang': ItemData(reventureOffset+4, True),
    'SpawnMapChest': ItemData(reventureOffset+5, True),
    'SpawnCompassChest': ItemData(reventureOffset+6, True),
    'SpawnWhistleChest': ItemData(reventureOffset+7, True),
    'SpawnBurgerChest': ItemData(reventureOffset+8, True),
    'SpawnDarkstoneChest': ItemData(reventureOffset+9, True),
    'SpawnHookChest': ItemData(reventureOffset+10, True),
    'SpawnFishingRodChest': ItemData(reventureOffset+11, True),
    'SpawnLavaTrinketChest': ItemData(reventureOffset+12, True),
    'SpawnMrHugsChest': ItemData(reventureOffset+13, True),
    'SpawnBombsChest': ItemData(reventureOffset+14, True),
    'SpawnShieldChest': ItemData(reventureOffset+15, True),
    'SpawnNukeItem': ItemData(reventureOffset+16, True),
    'SpawnPrincessItem': ItemData(reventureOffset+17, True),
    'SpawnAnvilItem': ItemData(reventureOffset+18, True),
    'SpawnStrawberry': ItemData(reventureOffset+19, True),
    
    #Transportation/Paths
    'UnlockShopCannon': ItemData(reventureOffset+20, True),
    'UnlockCastleToShopCannon': ItemData(reventureOffset+21, True),
    'UnlockDarkCastleCannon': ItemData(reventureOffset+22, True),
    'UnlockCastleToDarkCastleCannon': ItemData(reventureOffset+23, True),
    'UnlockGeyserDesert1': ItemData(reventureOffset+24, True),
    'UnlockGeyserDesert2': ItemData(reventureOffset+25, True),
    'UnlockGeyserVolcanoe': ItemData(reventureOffset+26, True), 
    'UnlockGeyserWaterfall': ItemData(reventureOffset+27, True),
    'UnlockElevatorButton': ItemData(reventureOffset+28, True),
    'UnlockCallElevatorButtons': ItemData(reventureOffset+29, True),
    'UnlockMirrorPortal': ItemData(reventureOffset+30, True),
    'UnlockFairyPortal': ItemData(reventureOffset+31, True),
    'GrowVine': ItemData(reventureOffset+32, True),
    'OpenCastleFloor': ItemData(reventureOffset+33, True),
    'UnlockFacePlantStone': ItemData(reventureOffset+34, True),
    'OpenSewerPipe': ItemData(reventureOffset+35, True),
    'DarkstoneLeverLeft': ItemData(reventureOffset+36, True),
    'DarkstoneLeverMiddle': ItemData(reventureOffset+37, True),
    'DarkstoneLeverRight': ItemData(reventureOffset+38, True),

    #NPCs
    'SpawnDragon': ItemData(reventureOffset+39, True),
    'SpawnShopkeeper': ItemData(reventureOffset+40, True),
    'SpawnMimic': ItemData(reventureOffset+41, True),
    'SpawnKing': ItemData(reventureOffset+42, True),
    'GrowChicken': ItemData(reventureOffset+43, True),
    'SpawnElder': ItemData(reventureOffset+44, True),
    'SpawnBoulderNPC': ItemData(reventureOffset+45, True),
    
    #Cosmetic
    'EnableCloset': ItemData(reventureOffset+46, False),
    'BuildStatue': ItemData(reventureOffset+47, True),
    'AddPC': ItemData(reventureOffset+48, False),
    'SpawnDolphins': ItemData(reventureOffset+49, False),
    'SpawnMimicPet': ItemData(reventureOffset+50, False),

    #Milestones
    'EarthGem': ItemData(reventureOffset+51, True, gem=True),
    'FireGem': ItemData(reventureOffset+52, True, gem=True),
    'WaterGem': ItemData(reventureOffset+53, True, gem=True),
    'WindGem': ItemData(reventureOffset+54, True, gem=True),

    #Ending
    'Victory': ItemData(None, True, True),
}

event_item_pairs: Dict[str, str] = {
    "100_UltimateEnding": "Victory",
}
