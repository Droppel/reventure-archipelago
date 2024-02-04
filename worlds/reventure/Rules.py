from BaseClasses import MultiWorld
from Options import PerGameCommonOptions
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import set_rule

class ReventureLogic(LogicMixin):
    recursionTracker = 0

    def _reventure_has_burger(self, player: int) -> bool:
        return self.has("SpawnBurgerChest", player) and self.has("DarkstoneLeverMiddle", player)
    
    def _reventure_has_darkstone(self, player: int) -> bool:
        return self.has("SpawnDarkstoneChest", player) and self.has("DarkstoneLeverMiddle", player)

    def _reventure_has_chicken(self, player: int) -> bool:
        return self.has("GrowChicken", player, 4)

    def _reventure_has_sword(self, player: int) -> bool:
        return self.has_any(["SpawnSwordPedestalItem", "SpawnSwordChest"], player)
    
    def _reventure_has_nuke(self, player: int) -> bool:
        return self.has_all(["SpawnNukeItem", "SpawnHookChest"], player)

    def _reventure_has_weight(self, player: int, req: int) -> bool:
        weightedItems = 0
        if self._reventure_has_sword(player):
            weightedItems += 1
        if self.has("SpawnShovelChest", player):
            weightedItems += 1
        if self.has("SpawnShieldChest", player):
            weightedItems += 1
        if self.has("SpawnBombsChest", player):
            weightedItems += 1
        if self.has("SpawnHookChest", player):
            weightedItems += 1
        if self.has("SpawnLavaTrinketChest", player):
            weightedItems += 1
        if self.has("SpawnWhistleChest", player):
            weightedItems += 1
        return weightedItems >= req
    
    def _reventure_has_items(self, player: int, req: int) -> bool:
        items = 0
        if self._reventure_has_sword(player):
            items += 1
        if self.has("SpawnShovelChest", player):
            items += 1
        if self.has("SpawnShieldChest", player):
            items += 1
        if self.has("SpawnBombsChest", player):
            items += 1
        if self.has("SpawnHookChest", player):
            items += 1
        if self.has("SpawnLavaTrinketChest", player):
            items += 1
        if self.has("SpawnWhistleChest", player):
            items += 1
        if self.has("SpawnMrHugsChest", player):
            items += 1
        if self.has("SpawnMapChest", player):
            items += 1
        if self.has("SpawnCompassChest", player):
            items += 1
        return items >= req
    
    def _reventure_has_endings(self, player: int, req: int) -> bool:
        count = 0
        locations = self.multiworld.get_locations(player)

        if req >= 50:
            # Inverted because it's faster
            invreq = 100 - req
            for loc in locations:
                if (loc.name == "UltimateEnding"):
                    continue
                count += not loc.can_reach(self)
                if count >= invreq:
                    return False
            return True
        else:
            for loc in locations:
                if (loc.name == "UltimateEnding"):
                    continue
                count += loc.can_reach(self)
                if count >= req:
                    return True
            return False

    def _reventure_can_reach_princessportal_with_item(self, player: int) -> bool:
        return self.has("UnlockMirrorPortal", player) and (self._reventure_has_chicken(player) or self.has("GrowVine", player))

    def _reventure_can_reach_princess_with_item(self, player: int) -> bool:
        return self.has("SpawnPrincessItem", player) and (self._reventure_can_reach_princessportal_with_item(player) or self.has_any(["SpawnHookChest", "UnlockElevatorButton"], player))


def set_rules(options: PerGameCommonOptions, multiworld: MultiWorld, p: int):
    set_rule(multiworld.get_location("StabElder", p), lambda state: state._reventure_has_sword(p) and state.has("SpawnElder", p))
    set_rule(multiworld.get_location("LonkFaceplant", p), lambda state: state.has("UnlockFacePlantStone", p))
    set_rule(multiworld.get_location("KilledByMinion", p), lambda state: True)
    set_rule(multiworld.get_location("StabGuard", p), lambda state: state._reventure_has_sword(p)),
    set_rule(multiworld.get_location("KillTheKing", p), lambda state: state._reventure_has_sword(p) and state.has("SpawnKing", p))
    set_rule(multiworld.get_location("FallIntoLava", p), lambda state: True)
    set_rule(multiworld.get_location("JumpIntoPiranhaLake", p), lambda state: True)
    set_rule(multiworld.get_location("WaterfallsBottom", p), lambda state: True)
    set_rule(multiworld.get_location("StabShopKeeper", p), lambda state: state._reventure_has_sword(p) and state.has("SpawnShopkeeper", p))
    set_rule(multiworld.get_location("DigIntoBottomlessPit", p), lambda state: state.has("SpawnShovelChest", p))
    set_rule(multiworld.get_location("RescueCat", p), lambda state: state.has("SpawnMrHugsChest", p))
    set_rule(multiworld.get_location("FindFishingRod", p), lambda state: state.has("SpawnFishingRodChest", p))
    set_rule(multiworld.get_location("HugMinion", p), lambda state: state.has("SpawnMrHugsChest", p))
    set_rule(multiworld.get_location("RoastedByDragon", p), lambda state: state.has("SpawnDragon", p))
    set_rule(multiworld.get_location("KilledByDarkArenaMinion", p), lambda state: True)
    set_rule(multiworld.get_location("StabDragon", p), lambda state: state._reventure_has_sword(p) and state.has("SpawnDragon", p))
    set_rule(multiworld.get_location("FaultyCannonShot", p), lambda state: state.has_any(["UnlockShopCannon", "UnlockCastleToShopCannon", "UnlockDarkCastleCannon"], p))
    set_rule(multiworld.get_location("HugTheKing", p), lambda state: state.has_all(["SpawnMrHugsChest", "SpawnKing"], p))
    set_rule(multiworld.get_location("HugGuard", p), lambda state: state.has("SpawnMrHugsChest", p))
    set_rule(multiworld.get_location("TakeTheDayOff", p), lambda state: True)
    set_rule(multiworld.get_location("FallIntoSpikes", p), lambda state: True)
    set_rule(multiworld.get_location("PickupAnvil", p), lambda state: state.has("SpawnAnvilItem", p))
    set_rule(multiworld.get_location("EatenByFakePrincess", p), lambda state: state.has("SpawnMimic", p))
    set_rule(multiworld.get_location("ClimbMountain", p), lambda state: state.has("SpawnStrawberry", p))
    set_rule(multiworld.get_location("StabMinionMultipleTimes", p), lambda state: state._reventure_has_sword(p))
    set_rule(multiworld.get_location("CrushedByOwnStuff", p), lambda state: state._reventure_has_weight(p, 5))
    set_rule(multiworld.get_location("ShootCannonballToCastle", p), lambda state: state._reventure_has_nuke(p) and state.has("UnlockShopCannon", p))
    set_rule(multiworld.get_location("CaughtByOwnBomb", p), lambda state: state.has("SpawnBombsChest", p))
    set_rule(multiworld.get_location("DragonWithShield", p), lambda state: state.has_all(["SpawnDragon", "SpawnShieldChest"], p))
    set_rule(multiworld.get_location("EnterTheChimney", p), lambda state: True)
    set_rule(multiworld.get_location("DestroyAllPots", p), lambda state: state._reventure_has_sword(p))
    set_rule(multiworld.get_location("StabBoulder", p), lambda state: state._reventure_has_sword(p) and state.has("SpawnBoulderNPC", p))
    set_rule(multiworld.get_location("LeapOfFaithFromTheMountain", p), lambda state: True)
    set_rule(multiworld.get_location("ElevatorCrush", p), lambda state: state.has_any(["UnlockElevatorButton", "UnlockCallElevatorButtons"], p))
    set_rule(multiworld.get_location("GetIntoThePipe", p), lambda state: state.has("OpenSewerPipe", p))
    set_rule(multiworld.get_location("DragonWithFireTrinket", p), lambda state: state.has_all(["SpawnDragon", "SpawnLavaTrinketChest"], p))
    set_rule(multiworld.get_location("HugShopkeeper", p), lambda state: state.has_all(["SpawnShopkeeper", "SpawnMrHugsChest"], p))
    set_rule(multiworld.get_location("WrongLever", p), lambda state: state.has("DarkstoneLeverLeft", p))
    set_rule(multiworld.get_location("GetIntoBigChest", p), lambda state: True)
    set_rule(multiworld.get_location("HugElder", p), lambda state: state.has("SpawnMrHugsChest", p) and state.has("SpawnElder", p))
    set_rule(multiworld.get_location("DragonWithShieldAndFireTrinket", p), lambda state: state.has_all(["SpawnDragon", "SpawnLavaTrinketChest", "SpawnShieldChest"], p))
    set_rule(multiworld.get_location("AirDuctsAccident", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("HugDragon", p), lambda state: state.has_all(["SpawnDragon", "SpawnMrHugsChest"], p))
    set_rule(multiworld.get_location("WrongLever2", p), lambda state: state.has("DarkstoneLeverRight", p))
    set_rule(multiworld.get_location("TakePrincessToBed", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("JumpOffTheCliff", p), lambda state: True)
    set_rule(multiworld.get_location("HarakiriSuicide", p), lambda state: state._reventure_has_sword(p))
    set_rule(multiworld.get_location("SelfDestructFortress", p), lambda state: True)
    set_rule(multiworld.get_location("HundredMinionsMassacre", p), lambda state: state._reventure_has_sword(p))
    set_rule(multiworld.get_location("KilledByDarkLord", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("TakePrincessBackToTown", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("ShootPrincessToTown", p), lambda state: state.has_all(["SpawnPrincessItem", "UnlockDarkCastleCannon"], p))
    set_rule(multiworld.get_location("FallWithPrincessToAnvilPit", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("HugBoulder", p), lambda state: state.has("SpawnMrHugsChest", p) and state.has("SpawnBoulderNPC", p))
    set_rule(multiworld.get_location("JumpOffTheBalconyWithPrincess", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("ShootCannonballToShop", p), lambda state: state._reventure_has_nuke(p) and state.has("UnlockCastleToShopCannon", p))
    set_rule(multiworld.get_location("HugPrincess", p), lambda state: state.has_all(["SpawnMrHugsChest", "SpawnPrincessItem"], p))
    set_rule(multiworld.get_location("JumpOffTheBalcony", p), lambda state: True)
    set_rule(multiworld.get_location("StayAfk", p), lambda state: True)
    set_rule(multiworld.get_location("PlaceBombUnderCastle", p), lambda state: state.has("SpawnBombsChest", p))
    set_rule(multiworld.get_location("DontKillMinions", p), lambda state: True)
    set_rule(multiworld.get_location("FindTreasure", p), lambda state: state.has("SpawnShovelChest", p) and (state._reventure_has_sword(p) or state.has_any(["SpawnHookChest", "UnlockGeyserWaterfall"], p)))
    set_rule(multiworld.get_location("KillChicken", p), lambda state: state._reventure_has_sword(p) and state._reventure_has_chicken(p))
    set_rule(multiworld.get_location("StabPrincess", p), lambda state: state._reventure_has_sword(p) and state._reventure_can_reach_princess_with_item(p))
    set_rule(multiworld.get_location("OverhealByFairies", p), lambda state: True)
    set_rule(multiworld.get_location("DarkStoneToAltar", p), lambda state: state._reventure_has_darkstone(p))
    set_rule(multiworld.get_location("CrushedAtUltimateDoor", p), lambda state: True)
    set_rule(multiworld.get_location("DarkLordComicStash", p), lambda state: True)
    set_rule(multiworld.get_location("StabDarkLord", p), lambda state: state._reventure_has_sword(p) and state._reventure_can_reach_princess_with_item(p))
    set_rule(multiworld.get_location("TriggerTrollSpikes", p), lambda state: True)
    set_rule(multiworld.get_location("SacrificeEveryItem", p), lambda state: state._reventure_has_items(p, 6))
    set_rule(multiworld.get_location("SacrificePrincess", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("HugDarkLord", p), lambda state: state.has_all(["SpawnMrHugsChest", "SpawnPrincessItem"], p))
    set_rule(multiworld.get_location("ShotgunFakePrincess", p), lambda state: state._reventure_has_sword(p) and state.has_all(["SpawnShopkeeper", "SpawnMimic", "UnlockShopCannon", "UnlockElevatorButton"], p))
    set_rule(multiworld.get_location("FakePrincessInsideChest", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("TakePrincessToDarkAltar", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("GetIntoTheCloud", p), lambda state: state.has("GrowVine", p) or (state._reventure_has_chicken(p) and (state._reventure_has_sword(p) or state.has_any(["SpawnHookChest", "UnlockGeyserWaterfall"], p))))
    set_rule(multiworld.get_location("KidnapPrincess", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("HugChicken", p), lambda state: state._reventure_has_chicken(p) and state.has("SpawnMrHugsChest", p))
    set_rule(multiworld.get_location("TakeChickenToDarkAltar", p), lambda state: state._reventure_has_chicken(p))
    set_rule(multiworld.get_location("PrincessToDesertGate", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("FallIntoWaterfallWithPrincess", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("BreakSpaceTimeContinuum", p), lambda state: state.has("SpawnWhistleChest", p))
    set_rule(multiworld.get_location("ShootCannonballToTown", p), lambda state: state._reventure_has_nuke(p) and state.has("UnlockDarkCastleCannon", p))
    set_rule(multiworld.get_location("KillAllFairies", p), lambda state: state._reventure_has_sword(p) or state.has("SpawnMrHugsChest", p) or (state.has("SpawnBoomerang", p) and (state.has("SpawnHookChest", p) or state._reventure_has_chicken(p))))
    set_rule(multiworld.get_location("MakeBabiesWithPrincess", p), lambda state: state._reventure_has_sword(p) and state._reventure_can_reach_princess_with_item(p))
    set_rule(multiworld.get_location("KillAllDevsHell", p), lambda state: state._reventure_has_sword(p) and state.has("SpawnPrincessItem", p) and (state.has("SpawnHookChest", p) or (state.has("SpawnShovelChest", p) and state._reventure_has_chicken(p) and (state.has("UnlockElevatorButton", p) or state._reventure_can_reach_princessportal_with_item(p)))))
    set_rule(multiworld.get_location("DesertEnd", p), lambda state: state._reventure_has_weight(p, 4) and state.has("UnlockGeyserDesert2", p))
    set_rule(multiworld.get_location("FindAlienLarvae", p), lambda state: state.has("SpawnShovelChest", p))
    set_rule(multiworld.get_location("FaceDarkLordWithShield", p), lambda state: state.has_all(["SpawnShieldChest", "SpawnPrincessItem"], p) and (state._reventure_can_reach_princessportal_with_item(p) or (state.has_any(["SpawnHookChest", "UnlockElevatorButton"], p) and (state._reventure_has_sword(p) or state._reventure_has_chicken(p) or state.has_any(["SpawnShovelChest", "UnlockShopCannon", "UnlockGeyserVolcanoe"], p)))))
    set_rule(multiworld.get_location("MultipleDesertJumps", p), lambda state: state._reventure_has_weight(p, 4))
    set_rule(multiworld.get_location("DatePrincessAndDragon", p), lambda state: state.has_all(["SpawnPrincessItem", "SpawnDragon"], p))
    set_rule(multiworld.get_location("GiveDarkStoneToDarkLord", p), lambda state: state._reventure_has_darkstone(p) and state._reventure_can_reach_princess_with_item(p))
    set_rule(multiworld.get_location("TakePrincessToLonksHouse", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("StayInTheWater", p), lambda state: True)
    set_rule(multiworld.get_location("AboardPirateShip", p), lambda state: True)
    set_rule(multiworld.get_location("SwimIntoTheOcean", p), lambda state: True)
    set_rule(multiworld.get_location("FeedTheMimic", p), lambda state: state._reventure_has_burger(p) and state.has("SpawnMimic", p) and (state._reventure_can_reach_princessportal_with_item(p) or state.has_any(["SpawnHookChest", "UnlockElevatorButton"], p)))
    set_rule(multiworld.get_location("FeedTheKing", p), lambda state: state._reventure_has_burger(p) and state.has("SpawnKing", p))
    if options.gems == 0:
        set_rule(multiworld.get_location("UltimateEnding", p), lambda state: state._reventure_has_endings(p, options.endings-1) and state.has_all(["SpawnShovelChest", "SpawnHookChest"], p) and state._reventure_has_weight(p, 4))
    elif options.gems == 1:
        set_rule(multiworld.get_location("UltimateEnding", p), lambda state: state._reventure_has_endings(p, options.endings-1) and state.has_all(["EarthGem", "WaterGem", "FireGem", "WindGem"], p))
    elif options.gems == 2:
        set_rule(multiworld.get_location("UltimateEnding", p), lambda state: state._reventure_has_endings(p, options.endings-1))

    multiworld.completion_condition[p] = lambda state: state.has("Victory", p)

