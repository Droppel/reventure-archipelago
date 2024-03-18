from BaseClasses import CollectionState, MultiWorld
from Options import PerGameCommonOptions
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import set_rule

def set_rules(options: PerGameCommonOptions, multiworld: MultiWorld, p: int):
    def has_burger(state: CollectionState, p: int) -> bool:
        return state.has("SpawnBurgerChest", p) and state.has("DarkstoneLeverMiddle", p)
    
    def has_darkstone(state: CollectionState, p: int) -> bool:
        return state.has_all(["SpawnDarkstoneChest", "DarkstoneLeverMiddle"], p)

    def has_chicken(state: CollectionState, p: int) -> bool:
        return state.has("GrowChicken", p, 4)
    
    def has_nuke(state: CollectionState, player: int) -> bool:
        return state.has_all(["SpawnNukeItem", "SpawnHookChest"], player)
    
    if options.treasureSword:
        def has_sword(state: CollectionState, p):
            if state.has("ProgressiveSword", p, 2):
                return True
            elif state.has("ProgressiveSword", p, 1):
                return state.has("SpawnShovelChest") and state.has_any(["SpawnHookChest", "UnlockGeyserWaterfall"], p)
            else:
                return False
    else:
        def has_sword(state: CollectionState, p):
            return state.has("ProgressiveSword", p)
    
    def has_weight(state: CollectionState, player: int, req: int) -> bool:
        weightedItems = 0
        if has_sword(state, player):
            weightedItems += 1
        if state.has("SpawnShovelChest", player):
            weightedItems += 1
        if state.has("SpawnShieldChest", player):
            weightedItems += 1
        if state.has("SpawnBombsChest", player):
            weightedItems += 1
        if state.has("SpawnHookChest", player):
            weightedItems += 1
        if state.has("SpawnLavaTrinketChest", player):
            weightedItems += 1
        if state.has("SpawnWhistleChest", player):
            weightedItems += 1
        if state.has("SpawnBoomerang", player):
            weightedItems += 1
        if has_nuke(state, player):
            weightedItems += 1
        if has_darkstone(state, player):
            weightedItems += 1
        if has_chicken(state, player):
            weightedItems += 1
        return weightedItems >= req
    
    def has_items(state: CollectionState, player: int, req: int) -> bool:
        items = 0
        valid_items = ["SpawnHookChest", "SpawnBombsChest", "SpawnShieldChest", "SpawnShovelChest",
                       "SpawnLavaTrinketChest", "SpawnWhistleChest", "SpawnBoomerang", "SpawnMrHugsChest", 
                       "SpawnMapChest", "SpawnCompassChest"]
        for item in valid_items:
            if state.has(item, player):
                items += 1
        if has_sword(state, player):
            items += 1
        if has_nuke(state, player):
            items += 1
        if has_darkstone(state, player):
            items += 1
        if has_chicken(state, player):
            items += 1
        if has_burger(state, player):
            items += 1
        return items >= req
    
    if options.endings-1 >= 50:
        # Inverted because it's faster
        def has_endings(state: CollectionState, player: int, req: int) -> bool:
            count = 0
            locations = state.multiworld.get_locations(player)
            invreq = 100 - req
            for loc in locations:
                if loc.name == "100_UltimateEnding":
                    continue
                count += not loc.can_reach(state)
                if count >= invreq:
                    return False
            return True
    else:
        def has_endings(state: CollectionState, player: int, req: int) -> bool:
            count = 0
            locations = state.multiworld.get_locations(player)
            for loc in locations:
                if loc.name == "100_UltimateEnding":
                    continue
                count += loc.can_reach(state)
                if count >= req:
                    return True
            return False

    def can_reach_princessportal_with_item(state: CollectionState, player: int) -> bool:
        return state.has("UnlockMirrorPortal", player) and (state.has("GrowVine", player)
                or (has_chicken(state, player)
                and (has_sword(state, player) 
                or state.has_any(["SpawnHookChest", "UnlockGeyserWaterfall"], player))))

    def can_pass_castle_with_item(state: CollectionState, p: int) -> bool:
        return has_sword(state, p) or (has_chicken(state, p) and state.has("BuildStatue", p)) or (
            state.has_any(["SpawnHookChest", "SpawnShovelChest", "UnlockShopCannon", "UnlockGeyserVolcanoe", "OpenCastleFloor", "UnlockFairyPortal"], p))

    def can_reach_princess_with_item(state: CollectionState, player: int) -> bool:
        return state.has("SpawnPrincessItem", player) and (can_reach_princessportal_with_item(state, player)
                                                          or state.has_any(["SpawnHookChest", "UnlockElevatorButton", "UnlockCallElevatorButtons"], player))
        

    set_rule(multiworld.get_location("01_StabElder", p), lambda state: has_sword(state, p) and state.has("SpawnElder", p))
    set_rule(multiworld.get_location("02_LonkFaceplant", p), lambda state: state.has("UnlockFacePlantStone", p))
    set_rule(multiworld.get_location("03_KilledByMinion", p), lambda state: True)
    set_rule(multiworld.get_location("04_StabGuard", p), lambda state: has_sword(state, p)),
    set_rule(multiworld.get_location("05_KillTheKing", p), lambda state: has_sword(state, p) and state.has("SpawnKing", p))
    set_rule(multiworld.get_location("06_FallIntoLava", p), lambda state: True)
    set_rule(multiworld.get_location("07_JumpIntoPiranhaLake", p), lambda state: True)
    set_rule(multiworld.get_location("08_WaterfallsBottom", p), lambda state: True)
    set_rule(multiworld.get_location("09_StabShopKeeper", p), lambda state: has_sword(state, p) and state.has("SpawnShopkeeper", p))
    set_rule(multiworld.get_location("10_DigIntoBottomlessPit", p), lambda state: state.has("SpawnShovelChest", p))
    set_rule(multiworld.get_location("11_RescueCat", p), lambda state: state.has("SpawnMrHugsChest", p))
    set_rule(multiworld.get_location("12_FindFishingRod", p), lambda state: state.has("SpawnFishingRodChest", p))
    set_rule(multiworld.get_location("13_HugMinion", p), lambda state: state.has("SpawnMrHugsChest", p))
    set_rule(multiworld.get_location("14_RoastedByDragon", p), lambda state: state.has("SpawnDragon", p))
    set_rule(multiworld.get_location("15_KilledByDarkArenaMinion", p), lambda state: True)
    set_rule(multiworld.get_location("16_StabDragon", p), lambda state: has_sword(state, p) and state.has("SpawnDragon", p))
    set_rule(multiworld.get_location("17_FaultyCannonShot", p), lambda state: 
             state.has_any(["UnlockShopCannon", "UnlockCastleToShopCannon", "UnlockDarkCastleCannon", "UnlockCastleToDarkCastleCannon"], p))
    set_rule(multiworld.get_location("18_HugTheKing", p), lambda state: state.has_all(["SpawnMrHugsChest", "SpawnKing"], p))
    set_rule(multiworld.get_location("19_HugGuard", p), lambda state: state.has("SpawnMrHugsChest", p))
    set_rule(multiworld.get_location("20_TakeTheDayOff", p), lambda state: True)
    set_rule(multiworld.get_location("21_FallIntoSpikes", p), lambda state: True)
    set_rule(multiworld.get_location("22_PickupAnvil", p), lambda state: state.has("SpawnAnvilItem", p))
    set_rule(multiworld.get_location("23_EatenByFakePrincess", p), lambda state: state.has("SpawnMimic", p))
    set_rule(multiworld.get_location("24_ClimbMountain", p), lambda state: state.has("SpawnStrawberry", p))
    set_rule(multiworld.get_location("25_StabMinionMultipleTimes", p), lambda state: has_sword(state, p))
    set_rule(multiworld.get_location("26_CrushedByOwnStuff", p), lambda state: has_weight(state, p, 5) and state.has("SpawnHookChest", p)) # Not fully exhaustive
    set_rule(multiworld.get_location("27_ShootCannonballToCastle", p), lambda state: has_nuke(state, p) and state.has("UnlockShopCannon", p))
    set_rule(multiworld.get_location("28_CaughtByOwnBomb", p), lambda state: state.has("SpawnBombsChest", p))
    set_rule(multiworld.get_location("29_DragonWithShield", p), lambda state: state.has_all(["SpawnDragon", "SpawnShieldChest"], p))
    set_rule(multiworld.get_location("30_EnterTheChimney", p), lambda state: True)
    set_rule(multiworld.get_location("31_DestroyAllPots", p), lambda state: has_sword(state, p))
    set_rule(multiworld.get_location("32_StabBoulder", p), lambda state: has_sword(state, p) and state.has("SpawnBoulderNPC", p))
    set_rule(multiworld.get_location("33_LeapOfFaithFromTheMountain", p), lambda state: True)
    set_rule(multiworld.get_location("34_ElevatorCrush", p), lambda state: state.has_any(["UnlockElevatorButton", "UnlockCallElevatorButtons", "SpawnPrincessItem"], p))
    set_rule(multiworld.get_location("35_GetIntoThePipe", p), lambda state: state.has("OpenSewerPipe", p))
    set_rule(multiworld.get_location("36_DragonWithFireTrinket", p), lambda state: state.has_all(["SpawnDragon", "SpawnLavaTrinketChest"], p))
    set_rule(multiworld.get_location("37_HugShopkeeper", p), lambda state: state.has_all(["SpawnShopkeeper", "SpawnMrHugsChest"], p))
    set_rule(multiworld.get_location("38_WrongLever", p), lambda state: state.has("DarkstoneLeverLeft", p))
    set_rule(multiworld.get_location("39_GetIntoBigChest", p), lambda state: True)
    set_rule(multiworld.get_location("40_HugElder", p), lambda state: state.has("SpawnMrHugsChest", p) and state.has("SpawnElder", p))
    set_rule(multiworld.get_location("41_DragonWithShieldAndFireTrinket", p), lambda state: state.has_all(["SpawnDragon", "SpawnLavaTrinketChest", "SpawnShieldChest"], p))
    set_rule(multiworld.get_location("42_AirDuctsAccident", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("43_HugDragon", p), lambda state: state.has_all(["SpawnDragon", "SpawnMrHugsChest"], p))
    set_rule(multiworld.get_location("44_WrongLever2", p), lambda state: state.has("DarkstoneLeverRight", p))
    set_rule(multiworld.get_location("45_TakePrincessToBed", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("46_JumpOffTheCliff", p), lambda state: True)
    set_rule(multiworld.get_location("47_HarakiriSuicide", p), lambda state: has_sword(state, p))
    if options.hardjumps:
        set_rule(multiworld.get_location("48_SelfDestructFortress", p), lambda state: True)
    else:
        set_rule(multiworld.get_location("48_SelfDestructFortress", p), lambda state: state.has("SpawnHookChest", p)
             or (can_pass_castle_with_item(state, p) and has_chicken(state, p)))
    if options.hardcombat:
        set_rule(multiworld.get_location("49_HundredMinionsMassacre", p), lambda state: has_sword(state, p))
    else:
        set_rule(multiworld.get_location("49_HundredMinionsMassacre", p), lambda state: has_sword(state, p)
             and state.has("SpawnShieldChest", p))
    set_rule(multiworld.get_location("50_KilledByDarkLord", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("51_TakePrincessBackToTown", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("52_ShootPrincessToTown", p), lambda state: state.has_all(["SpawnPrincessItem", "UnlockDarkCastleCannon"], p))
    set_rule(multiworld.get_location("53_FallWithPrincessToAnvilPit", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("54_HugBoulder", p), lambda state: state.has("SpawnMrHugsChest", p) and state.has("SpawnBoulderNPC", p))
    set_rule(multiworld.get_location("55_JumpOffTheBalconyWithPrincess", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("56_ShootCannonballToShop", p), lambda state: has_nuke(state, p) and state.has("UnlockCastleToShopCannon", p)
             and can_pass_castle_with_item(state, p))
    set_rule(multiworld.get_location("57_HugPrincess", p), lambda state: state.has_all(["SpawnMrHugsChest", "SpawnPrincessItem"], p))
    set_rule(multiworld.get_location("58_JumpOffTheBalcony", p), lambda state: True)
    set_rule(multiworld.get_location("59_StayAfk", p), lambda state: True)
    set_rule(multiworld.get_location("60_PlaceBombUnderCastle", p), lambda state: state.has("SpawnBombsChest", p))
    set_rule(multiworld.get_location("61_DontKillMinions", p), lambda state: True)
    set_rule(multiworld.get_location("62_FindTreasure", p), lambda state: state.has("SpawnShovelChest", p) and (has_sword(state, p)
             or state.has_any(["SpawnHookChest", "UnlockGeyserWaterfall"], p)))
    set_rule(multiworld.get_location("63_KillChicken", p), lambda state: has_sword(state, p) and has_chicken(state, p))
    set_rule(multiworld.get_location("64_StabPrincess", p), lambda state: has_sword(state, p) and can_reach_princess_with_item(state, p))
    set_rule(multiworld.get_location("65_OverhealByFairies", p), lambda state: True)
    set_rule(multiworld.get_location("66_DarkStoneToAltar", p), lambda state: has_darkstone(state, p))
    set_rule(multiworld.get_location("67_CrushedAtUltimateDoor", p), lambda state: True)
    set_rule(multiworld.get_location("68_DarkLordComicStash", p), lambda state: True)
    set_rule(multiworld.get_location("69_StabDarkLord", p), lambda state: has_sword(state, p) and can_reach_princess_with_item(state, p))
    set_rule(multiworld.get_location("71_SacrificeEveryItem", p), lambda state: has_items(state, p, 6) and (has_sword(state, p)
             or state.has_all(["SpawnShovelChest", "UnlockGeyserWaterfall"], p) or (state.has("SpawnBombsChest", p)
             and state.has_any(["UnlockShopCannon", "UnlockGeyserVolcanoe", "OpenCastleFloor", "UnlockFairyPortal"], p))))
    set_rule(multiworld.get_location("70_TriggerTrollSpikes", p), lambda state: True)
    set_rule(multiworld.get_location("72_SacrificePrincess", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("73_HugDarkLord", p), lambda state: state.has_all(["SpawnMrHugsChest", "SpawnPrincessItem"], p))
    if options.hardjumps or options.hardcombat:    
        set_rule(multiworld.get_location("74_ShotgunFakePrincess", p), lambda state: has_sword(state, p)
             and state.has_all(["SpawnShopkeeper", "SpawnMimic", "UnlockShopCannon"], p)
             and state.has_any(["UnlockCallElevatorButtons", "UnlockElevatorButton"], p))
    else:    
        set_rule(multiworld.get_location("74_ShotgunFakePrincess", p), lambda state: has_sword(state, p)
             and state.has_all(["SpawnShopkeeper", "SpawnMimic", "UnlockShopCannon"], p)
             and state.has_any(["UnlockCallElevatorButtons", "UnlockElevatorButton"], p)
             and state.has_any(["SpawnBombsChest", "SpawnShovelChest"], p))
    set_rule(multiworld.get_location("75_FakePrincessInsideChest", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("76_TakePrincessToDarkAltar", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("77_GetIntoTheCloud", p), lambda state: state.has("GrowVine", p) or (has_chicken(state, p) and (has_sword(state, p)
             or state.has("SpawnHookChest", p) or (can_pass_castle_with_item(state, p) and state.has("UnlockGeyserWaterfall", p)))))
    set_rule(multiworld.get_location("78_KidnapPrincess", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("79_HugChicken", p), lambda state: has_chicken(state, p) and state.has("SpawnMrHugsChest", p))
    set_rule(multiworld.get_location("80_TakeChickenToDarkAltar", p), lambda state: has_chicken(state, p) and can_pass_castle_with_item(state, p))
    set_rule(multiworld.get_location("81_PrincessToDesertGate", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("82_FallIntoWaterfallWithPrincess", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("83_BreakSpaceTimeContinuum", p), lambda state: state.has("SpawnWhistleChest", p))
    set_rule(multiworld.get_location("84_ShootCannonballToTown", p), lambda state: has_nuke(state, p) and state.has("UnlockDarkCastleCannon", p) 
             and can_pass_castle_with_item(state, p))
    set_rule(multiworld.get_location("85_KillAllFairies", p), lambda state: has_sword(state, p) or state.has("SpawnMrHugsChest", p)
             or state.has("SpawnBoomerang", p))
    set_rule(multiworld.get_location("86_MakeBabiesWithPrincess", p), lambda state: has_sword(state, p) and state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("87_KillAllDevsHell", p), lambda state: can_reach_princess_with_item(state, p)
             and ((has_sword(state, p) and (state.has("SpawnHookChest", p) or (has_chicken(state, p) and state.has("SpawnShovelChest", p)))) 
             or (state.has("SpawnBoomerang", p) and state.has_any(["SpawnHookChest", "SpawnShovelChest"], p))))
    set_rule(multiworld.get_location("88_DesertEnd", p), lambda state: has_weight(state, p, 4) and state.has_all(["SpawnHookChest", "UnlockGeyserDesert2"], p))
    if options.hardjumps:
        set_rule(multiworld.get_location("89_FindAlienLarvae", p), lambda state: state.has("SpawnPrincessItem", p) or (state.has("SpawnShovelChest", p)))
    else:
        set_rule(multiworld.get_location("89_FindAlienLarvae", p), lambda state: state.has("SpawnPrincessItem", p) or (state.has_all(["SpawnShovelChest", "SpawnLavaTrinketChest"], p)))
    set_rule(multiworld.get_location("90_FaceDarkLordWithShield", p), lambda state: state.has("SpawnShieldChest", p) and can_reach_princess_with_item(state, p)
             and can_pass_castle_with_item(state, p))
    set_rule(multiworld.get_location("91_MultipleDesertJumps", p), lambda state: has_weight(state, p, 4) and state.has("SpawnHookChest", p))
    set_rule(multiworld.get_location("92_DatePrincessAndDragon", p), lambda state: state.has_all(["SpawnPrincessItem", "SpawnDragon"], p))
    set_rule(multiworld.get_location("93_GiveDarkStoneToDarkLord", p), lambda state: has_darkstone(state, p) and state.has("SpawnPrincessItem", p)
             and state.has_any(["SpawnHookChest", "UnlockElevatorButton", "UnlockCallElevatorButtons"], p))
    set_rule(multiworld.get_location("94_TakePrincessToLonksHouse", p), lambda state: state.has("SpawnPrincessItem", p))
    set_rule(multiworld.get_location("95_StayInTheWater", p), lambda state: True)
    set_rule(multiworld.get_location("96_AboardPirateShip", p), lambda state: True)
    set_rule(multiworld.get_location("97_SwimIntoTheOcean", p), lambda state: True)
    set_rule(multiworld.get_location("98_FeedTheMimic", p), lambda state: has_burger(state, p) and state.has("SpawnMimic", p)
             and (state.has_any(["SpawnHookChest", "UnlockElevatorButton", "UnlockCallElevatorButtons"], p) or state.has_all(["GrowVine", "UnlockMirrorPortal"], p)))
    set_rule(multiworld.get_location("99_FeedTheKing", p), lambda state: has_burger(state, p) and state.has("SpawnKing", p))
    if options.randomizeGems: # Randomized Gems
        requiredAmount = (options.gemsInPool * options.gemsRequired) // 100
        set_rule(multiworld.get_location("100_UltimateEnding", p), lambda state: has_endings(state, p, options.endings-1) and state.has("Gem", p, requiredAmount))
    else: #Vanilla Gems
        set_rule(multiworld.get_location("100_UltimateEnding", p), lambda state: has_endings(state, p, options.endings-1) and state.has_all(["SpawnShovelChest", "SpawnHookChest"], p) and has_weight(state, p, 4))

    multiworld.completion_condition[p] = lambda state: state.has("Victory", p)

