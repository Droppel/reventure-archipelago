import copy
import typing

class APItems:
    def __init__(self):
        self.apitems = []
    
    def add_apitem(self, item: str):
        if not item in self.apitems:
            self.apitems.append(item)
    
    def remove_apitem(self, item: str):
        if item in self.apitems:
            self.apitems.remove(item)
    
    def add_apitems(self, items: typing.List[str]):
        for item in items:
            self.add_apitem(item)

    def is_subset(self, other: "APItems"):
        return all(item in other.apitems for item in self.apitems)
    
    def is_strict_subset(self, other: "APItems"):
        return self.is_subset(other) and not len(self.apitems) == len(other.apitems)
    
    def add_apitems_from_string(self, items: str):
        self.add_apitems(items.split(", "))

    def to_string(self):
        self.apitems.sort()
        return ", ".join(self.apitems)
        
class APState:
    def __init__(self):
        self.potapitems: typing.List[APItems] = []
    
    def reduce_one(self):
        for i in range(len(self.potapitems)):
            for j in range(i+1, len(self.potapitems)):
                if self.potapitems[i].is_subset(self.potapitems[j]):
                    self.potapitems.pop(j)
                    return True
                if self.potapitems[j].is_subset(self.potapitems[i]):
                    self.potapitems.pop(i)
                    return True
        return False
    
    def reduce_all(self):
        changed = False
        while self.reduce_one():
            changed = True
        return changed

class ReventureState:
    def __init__(self):
        self.apstate = {}
        self.state = {}
        # Items
        self.state["has_chicken"] = False
        self.state["sac_chicken"] = False
        self.state["has_shovel"] = False
        self.state["sac_shovel"] = False
        self.state["has_sword"] = False
        self.state["sac_sword"] = False
        self.state["has_shield"] = False
        self.state["sac_shield"] = False
        self.state["has_map"] = False
        self.state["sac_map"] = False
        self.state["has_compass"] = False
        self.state["sac_compass"] = False
        self.state["has_mrhugs"] = False
        self.state["sac_mrhugs"] = False
        self.state["has_lavaTrinket"] = False
        self.state["sac_lavaTrinket"] = False

        # Events
        self.state["castleBridgeDown"] = False

        # Shovel Short Cuts
        self.state["shovelSSC"] = False
        self.state["lonksHouseSSC1"] = False
        self.state["lonksHouseSSC2"] = False
        pass

    def ap_has(self, item: str):
        return self.apstate[item]

    def event(self, event: str):
        return self.state[event]

    def checkForceSSC(self, ssc: str):
        return self.event(ssc) or not self.event("has_shovel")
    
    def get_jump(self):
        jump = 3
        if self.state["has_shovel"]:
            jump -= 0.5
        if self.state["has_sword"]:
            jump -= 0.5
        if self.state["has_chicken"]:
            jump -= 0.5
        if self.state["has_shield"]:
            jump -= 0.5
        if self.state["has_lavaTrinket"]:
            jump -= 0.5
        return jump

class BaseRegion:
    def __init__(self, name: str):
        self.name = name
        self.connections: typing.List[BaseConnection] = []
        self.statechange: typing.List[StateChange] = []
        self.locations: typing.List[BaseConnection] = []

    def add_connection(self, connection):
        self.connections.append(connection)
    
    def add_statechange(self, statechange):
        self.statechange.append(statechange)

    def add_location(self, location):
        self.locations.append(location)

CollectionRule = typing.Callable[[ReventureState], bool]
class BaseConnection:
    def __init__(self, goal_region: BaseRegion, rule: CollectionRule, apitems: typing.List[str] = []):
        self.goal_region = goal_region
        self.rule = rule
        self.apitems = apitems
    
    def can_use(self, state: ReventureState):
        return self.rule(state)

class StateChange:
    def __init__(self, states: typing.List[str], values: typing.List[bool], rule: CollectionRule, apitems: typing.List[str] = []):
        self.rule = rule
        self.apitems = apitems
        self.states = states
        self.values = values
    
    def can_use(self, state: ReventureState):
        return self.rule(state)

class Connection:
    # name equals the name of the goal region
    def __init__(self, name: str, apitems: typing.List[str] = []):
        self.name = name
        self.apitems = APItems()
        self.apitems.add_apitems(apitems)

class Region:
    def __init__(self, base_region: BaseRegion, state: ReventureState, location: bool = False):
        self.base_region = base_region
        self.state = state
        self.name = base_region.name
        for event in state.state.keys():
            if state.state[event]:
                self.name += f"__{event}"
        self.connections: typing.List[Connection] = []
        self.location = location
        self.parents: typing.List[str] = []
        self.apstate: APState = APState()
        self.complexity = 0
        for event in state.state.keys():
            if state.state[event]:
                self.complexity += 1
        
    def add_connection(self, connection: Connection):
        self.connections.append(connection)

    def get_connection(self, name: str):
        for conn in self.connections:
            if conn.name == name:
                return conn
    
    def remove_connection(self, connection: str):
        for conn in self.connections:
            if conn.name == connection:
                self.connections.remove(conn)
                return

    def add_parent(self, parent: "Region", conn_apitems: APItems):
        self.parents.append(parent.name)
        for potapitems in parent.apstate.potapitems:
            new_potapitems = copy.deepcopy(potapitems)
            new_potapitems.add_apitems(conn_apitems.apitems)
            self.apstate.potapitems.append(new_potapitems)
        self.apstate.reduce_all()

    def merge(self, region: "Region"):
        self.remove_connection(region.name)
        self.parents.remove(region.name)
        region.remove_connection(self.name)
        region.parents.remove(self.name)
        for connection in region.connections:
            child = regions_dict[connection.name]
            child.parents.remove(region.name)
            if connection.name in [con.name for con in self.connections]:
                continue
            child.parents.append(self.name)
            self.add_connection(connection)
        for sub_parent in region.parents:
            other_parent = regions_dict[sub_parent]
            conn = other_parent.get_connection(region.name)
            other_parent.remove_connection(region.name)
            if sub_parent in self.parents:
                continue
            self.parents.append(sub_parent)
            other_parent.add_connection(Connection(self.name, conn.apitems.apitems))
            
def is_region_in_list(region: Region, region_list: typing.List[Region]):
    for reg in region_list:
        if reg.name == region.name:
            return True
    return False

def lambda_tostring(func):
    import inspect
    source = inspect.getsourcelines(func)
    funcString = str(source[0][0])
    if funcString.__contains__("def __init__"):
        return ""
    funcString = funcString.strip("[' ']").split(":")[1][:-3]
    return funcString
    
def create_plant_uml(regions: typing.List[Region]):
    plant_uml = "@startuml\nhide circle\n"
    for region in regions:
        plant_uml += f"class \"{region.name}\"\n"
        for connection in region.connections:
            plant_uml += f"\"{region.name}\" --> \"{connection.name}\""
            conn_string = ", ".join(connection.apitems.apitems)
            if conn_string != "":
                plant_uml += f" : {conn_string}"
            plant_uml += "\n"
    plant_uml += "@enduml"
    return plant_uml

if __name__ == "__main__":

    def check_valid_parents():
        for r in done_regions:
            for c in r.connections:
                if len(r.parents) == 0 and r.name != "LonksHouse":
                    print(f"Region without parents: {r.name}")
                if not r.name in regions_dict[c.name].parents:
                    print(f"Invalid parent connection: {r.name} -> {c}")
                if r.name == c.name:
                    print(f"Self connection: {r.name}")
        # breakpoint = 42

    # Create Location Regions
    loc01 = BaseRegion("01: It\'s Dangerous to be Near Tim")
    loc02 = BaseRegion("02: Shit Happens")
    loc04 = BaseRegion("04: Public Enemy")
    loc05 = BaseRegion("05: Kingslayer")
    # set_rule(multiworld.get_location("09: Customer is Always Right", p), lambda state: has_sword(state, p) and state.has("Shopkeeper", p))
    loc10 = BaseRegion("10: Gold Rush")
    loc11 = BaseRegion("11: Feline Company")
    # set_rule(multiworld.get_location("12: Hobbies", p), lambda state: state.has("Fishing Rod", p))
    loc13 = BaseRegion("13: Allergic to Cuteness")
    loc14 = BaseRegion("14: Dracar-ish")
    loc16 = BaseRegion("16: Monster Hunter")
    loc18 = BaseRegion("18: King of Hearts")
    loc19 = BaseRegion("19: Broken Heart")
    # set_rule(multiworld.get_location("22: Paperweight", p), lambda state: state.has("Anvil", p))
    # set_rule(multiworld.get_location("23: True Beauty is inside", p), lambda state: state.has("Mimic", p))
    # set_rule(multiworld.get_location("24: Strawberry", p), lambda state: state.has("Strawberry", p))
    loc25 = BaseRegion("25: Bully")
    # set_rule(multiworld.get_location("26: Greedy Bastard", p), lambda state: has_weight(state, p, 5) and state.has("Hook", p)) # Not fully exhaustive
    # set_rule(multiworld.get_location("27: Airstrike", p), lambda state: has_nuke(state, p) and state.has("Shop Cannon", p))
    # set_rule(multiworld.get_location("28: Don\'t Try This at Home", p), lambda state: state.has("Bombs", p))
    loc29 = BaseRegion("29: The Man in the Steel Mask")
    # set_rule(multiworld.get_location("31: Collateral Damage", p), lambda state: has_sword(state, p))
    # set_rule(multiworld.get_location("32: You Monster", p), lambda state: has_sword(state, p) and state.has("Boulder", p))
    # set_rule(multiworld.get_location("34: -1st Floor", p), lambda state: state.has_any(["Elevator Button", "Call Elevator Buttons", "Princess"], p))
    loc35 = BaseRegion("35: Wastewater")
    loc36 = BaseRegion("36: Fireproof")
    # set_rule(multiworld.get_location("37: Free Hugs", p), lambda state: state.has_all(["Shopkeeper", "Mister Hugs"], p))
    # set_rule(multiworld.get_location("38: Oh Boy, I\'m so Hungry", p), lambda state: state.has("Dark Stone Lever Left", p))
    loc40 = BaseRegion("40: Sexy Beard")
    loc41 = BaseRegion("41: Post-Traumatic Stress Disorder")
    # set_rule(multiworld.get_location("42: Sneaky Bastard", p), lambda state: state.has("Princess", p))
    loc43 = BaseRegion("43: Dinner for Two")
    # set_rule(multiworld.get_location("44: Bad Leverage", p), lambda state: state.has("Dark Stone Lever Right", p))
    # set_rule(multiworld.get_location("45: Well Excuuuuse Me, Princess", p), lambda state: state.has("Princess", p))
    # set_rule(multiworld.get_location("47: Harakiri", p), lambda state: has_sword(state, p))
    # set_rule(multiworld.get_location("49_HundredMinionsMassacre", p), lambda state: has_sword(state, p))
    # set_rule(multiworld.get_location("50: P0wned", p), lambda state: state.has("Princess", p))
    # set_rule(multiworld.get_location("51: Politics", p), lambda state: state.has("Princess", p))
    # set_rule(multiworld.get_location("52: I\'m Feeling Lucky", p), lambda state: state.has_all(["Princess", "Dark Fortress Cannon"], p))
    # set_rule(multiworld.get_location("53: Videogames", p), lambda state: state.has("Princess", p))
    # set_rule(multiworld.get_location("54: Paraphilia", p), lambda state: state.has("Mister Hugs", p) and state.has("Boulder", p))
    # set_rule(multiworld.get_location("55: Escape Shortcut", p), lambda state: state.has("Princess", p))
    # set_rule(multiworld.get_location("56: Refund Request", p), lambda state: has_nuke(state, p) and state.has("Castle To Shop Cannon", p)
    #          and can_pass_castle_with_item(state, p))
    # set_rule(multiworld.get_location("57: Friendzoned", p), lambda state: state.has_all(["Mister Hugs", "Princess"], p))
    # set_rule(multiworld.get_location("60: Viva La Resistance", p), lambda state: state.has("Bombs", p))
    # set_rule(multiworld.get_location("62: Jackpot", p), lambda state: state.has("Shovel", p) and (has_sword(state, p)
    #          or state.has_any(["Hook", "Waterfall Geyser"], p)))
    loc63 = BaseRegion("63: You Don\'t Mess With Chicken")
    # set_rule(multiworld.get_location("64: I Thought It Was A Mimic", p), lambda state: has_sword(state, p) and can_reach_princess_with_item(state, p))
    # set_rule(multiworld.get_location("66: Finite War", p), lambda state: has_darkstone(state, p))
    # set_rule(multiworld.get_location("69: Quick and Dirty", p), lambda state: has_sword(state, p) and can_reach_princess_with_item(state, p))
    # set_rule(multiworld.get_location("71: Sustainable Development", p), lambda state: has_items(state, p, 6) and (has_sword(state, p)
    #          or state.has_all(["Shovel", "Waterfall Geyser"], p) or (state.has("Bombs", p)
    #          and state.has_any(["Shop Cannon", "Volcano Geyser", "Open Castle Floor", "Fairy Portal"], p))))
    # set_rule(multiworld.get_location("72: Ecologist", p), lambda state: state.has("Princess", p))
    # set_rule(multiworld.get_location("73: Dark Love", p), lambda state: state.has_all(["Mister Hugs", "Princess"], p))
    # set_rule(multiworld.get_location("74: Bittersweet Revenge", p), lambda state: has_sword(state, p)
    #      and state.has_all(["Shopkeeper", "Mimic", "Shop Cannon"], p)
    #      and state.has_any(["Call Elevator Buttons", "Elevator Button"], p))
    # set_rule(multiworld.get_location("75: Please, Not Again", p), lambda state: state.has("Princess", p))
    # set_rule(multiworld.get_location("76: A Waifu is You", p), lambda state: state.has("Princess", p))
    # set_rule(multiworld.get_location("77: Battle Royale", p), lambda state: state.has("Vine", p) or (has_chicken(state, p) and (has_sword(state, p)
    #          or state.has("Hook", p) or (can_pass_castle_with_item(state, p) and state.has("Waterfall Geyser", p)))))
    # set_rule(multiworld.get_location("78: Silver or Lead", p), lambda state: state.has("Princess", p))
    loc79 = BaseRegion("79: Good Ending")
    # set_rule(multiworld.get_location("80: Chicken of Doom", p), lambda state: has_chicken(state, p) and can_pass_castle_with_item(state, p))
    # set_rule(multiworld.get_location("81: Forever Together", p), lambda state: state.has("Princess", p))
    # set_rule(multiworld.get_location("82: Perfect Crime", p), lambda state: state.has("Princess", p))
    # set_rule(multiworld.get_location("83: We Have to Go Back", p), lambda state: state.has("Whistle", p))
    # set_rule(multiworld.get_location("84: Not what you Expected", p), lambda state: has_nuke(state, p) and state.has("Dark Fortress Cannon", p) 
    #          and can_pass_castle_with_item(state, p))
    # set_rule(multiworld.get_location("85: Hey, Listen", p), lambda state: has_sword(state, p) or state.has("Mister Hugs", p)
    #          or state.has("Boomerang", p))
    # set_rule(multiworld.get_location("86: Full House", p), lambda state: has_sword(state, p) and state.has("Princess", p))
    # set_rule(multiworld.get_location("87: Crunch Hell", p), lambda state: can_reach_princess_with_item(state, p)
    #          and ((has_sword(state, p) and (state.has("Hook", p) or (has_chicken(state, p) and state.has("Shovel", p)))) 
    #          or (state.has("Boomerang", p) and state.has_any(["Hook", "Shovel"], p))))
    # set_rule(multiworld.get_location("88: Odyssey", p), lambda state: has_weight(state, p, 4) and state.has_all(["Hook", "Desert Geyser West"], p))
    # set_rule(multiworld.get_location("89: Intestinal Parasites", p), lambda state: state.has("Princess", p) or (state.has("Shovel", p)))
    # set_rule(multiworld.get_location("90: Try Harder", p), lambda state: state.has("Shield", p) and can_reach_princess_with_item(state, p)
    #          and can_pass_castle_with_item(state, p))
    # set_rule(multiworld.get_location("91: Jump Around", p), lambda state: has_weight(state, p, 4) and state.has("Hook", p))
    # set_rule(multiworld.get_location("92: First Date", p), lambda state: state.has_all(["Princess", "Dragon"], p))
    # set_rule(multiworld.get_location("93: Dark Delivery Boy", p), lambda state: has_darkstone(state, p) and state.has("Princess", p)
    #          and state.has_any(["Hook", "Elevator Button", "Call Elevator Buttons"], p))
    # set_rule(multiworld.get_location("94: Influencers", p), lambda state: state.has("Princess", p))
    # set_rule(multiworld.get_location("98: Suspension Points", p), lambda state: has_burger(state, p) and state.has("Mimic", p)
    #          and (state.has_any(["Hook", "Elevator Button", "Call Elevator Buttons"], p) or state.has_all(["Vine", "Mirror Portal"], p)))
    # set_rule(multiworld.get_location("99: Delivery Boy", p), lambda state: has_burger(state, p) and state.has("King", p))

    # Create regions
    lonksHouse = BaseRegion("LonksHouse")
    elder = BaseRegion("Elder")
    chicken = BaseRegion("Chicken")
    shovel = BaseRegion("Shovel")
    castleFirstFloor = BaseRegion("CastleFirstFloor")
    castleShieldChest = BaseRegion("CastleShieldChest")
    castleMapChest = BaseRegion("CastleMapChest")
    castleRoof = BaseRegion("CastleRoof")
    princessRoom = BaseRegion("PrincessRoom")
    volcanoTopExit = BaseRegion("VolcanoTopExit")
    lavaTrinket = BaseRegion("LavaTrinket")
    sscLonkToVolcano = BaseRegion("SSCLonkToVolcano")
    volcanoDropStone = BaseRegion("VolcanoDropStone")
    volcanoBridge = BaseRegion("VolcanoBridge")
    belowVolcanoBridge = BaseRegion("BelowVolcanoBridge")
    sewer = BaseRegion("Sewer")
    leftOfDragon = BaseRegion("LeftOfDragon")
    rightOfDragon = BaseRegion("RightOfDragon")
    goldRoom = BaseRegion("GoldRoom")
    sewerPipe = BaseRegion("SewerPipe")
    volcanoGeyser = BaseRegion("VolcanoGeyser")
    ultimateDoor = BaseRegion("UltimateDoor")
    castleMinions = BaseRegion("CastleMinions")

    lonksHouse.add_connection(BaseConnection(elder, lambda state: state.get_jump() >= 2 and state.checkForceSSC("lonksHouseSSC1")))
    lonksHouse.add_connection(BaseConnection(shovel, lambda state: state.event("shovelSSC") and state.get_jump() >= 3 and state.checkForceSSC("lonksHouseSSC1")))
    lonksHouse.add_connection(BaseConnection(castleFirstFloor, lambda state: state.checkForceSSC("lonksHouseSSC1")))
    lonksHouse.add_connection(BaseConnection(sscLonkToVolcano, lambda state: state.event("lonksHouseSSC1")))
    lonksHouse.add_statechange(StateChange(["has_sword"], [True],
                                           lambda state: not state.event("sac_sword") and not state.event("has_sword") and state.get_jump() >= 2 and state.checkForceSSC("lonksHouseSSC1"),
                                           ["Sword"]))
    lonksHouse.add_statechange(StateChange(["lonksHouseSSC1"], [True],
                                           lambda state: not state.event("lonksHouseSSC1") and state.event("has_shovel")))
    #TODO: This should be added to lonkshouse. But doing that breaks something. Logically there is no difference when adding it to castleFirstFloor instead
    castleFirstFloor.add_location(BaseConnection(loc02, lambda state: True,
                                            ["Faceplant Stone"]))
    lonksHouse.add_location(BaseConnection(loc04, lambda state: state.event("has_sword")))
    lonksHouse.add_location(BaseConnection(loc19, lambda state: state.event("has_mrhugs")))

    sscLonkToVolcano.add_connection(BaseConnection(volcanoBridge, lambda state: state.event("lonksHouseSSC2")))
    sscLonkToVolcano.add_statechange(StateChange(["lonksHouseSSC2"], [True],
                                                lambda state: not state.event("lonksHouseSSC2") and state.event("has_shovel")))
    
    elder.add_connection(BaseConnection(chicken, lambda state: state.get_jump() >= 2))
    elder.add_connection(BaseConnection(shovel, lambda state: True))
    elder.add_connection(BaseConnection(lonksHouse, lambda state: state.get_jump() >= 2))
    elder.add_connection(BaseConnection(volcanoTopExit, lambda state: state.get_jump() >= 2))
    elder.add_statechange(StateChange(["has_sword"], [True],
                                      lambda state: not state.event("sac_sword") and not state.event("has_sword"),
                                      ["Sword"]))
    elder.add_location(BaseConnection(loc01, lambda state: state.event("has_sword"),
                                      ["Elder"]))    
    elder.add_location(BaseConnection(loc40, lambda state: state.event("has_mrhugs"),
                                      ["Elder"]))

    chicken.add_connection(BaseConnection(elder, lambda state: True))
    chicken.add_connection(BaseConnection(lonksHouse, lambda state: True))
    chicken.add_connection(BaseConnection(volcanoTopExit, lambda state: state.get_jump() >= 2))
    chicken.add_statechange(StateChange(["has_chicken"], [True],
                                        lambda state: not state.event("sac_chicken") and not state.event("has_chicken"),
                                        ["Chicken"]))
    chicken.add_location(BaseConnection(loc63, lambda state: not state.event("has_chicken") and state.event("has_sword"),
                                        ["Chicken"]))
    chicken.add_location(BaseConnection(loc79, lambda state: not state.event("has_chicken") and state.event("has_mrhugs"),
                                        ["Chicken"]))

    shovel.add_connection(BaseConnection(elder, lambda state: state.get_jump() >= 3 and state.checkForceSSC("shovelSSC")))
    shovel.add_connection(BaseConnection(lonksHouse, lambda state: state.event("shovelSSC")))
    shovel.add_statechange(StateChange(["has_shovel"], [True],
                                       lambda state: not state.event("has_shovel") and not state.event("sac_shovel"),
                                       ["Shovel"]))
    shovel.add_statechange(StateChange(["shovelSSC"], [True], lambda state: not state.event("shovelSSC") and state.event("has_shovel")))

    castleFirstFloor.add_connection(BaseConnection(lonksHouse, lambda state: True))
    castleFirstFloor.add_connection(BaseConnection(castleShieldChest, lambda state: state.get_jump() >= 2))
    castleFirstFloor.add_connection(BaseConnection(castleMapChest, lambda state: state.get_jump() >= 3))
    castleFirstFloor.add_connection(BaseConnection(sewer, lambda state: True, ["Open Castle Floor"]))
    castleFirstFloor.add_connection(BaseConnection(castleMinions, lambda state: state.event("castleBridgeDown")))
    castleFirstFloor.add_statechange(StateChange(["castleBridgeDown"], [True], lambda state: not state.event("castleBridgeDown") and 
                                                 (state.event("has_sword") or state.event("has_shovel"))))
    castleFirstFloor.add_location(BaseConnection(loc04, lambda state: state.event("has_sword")))
    castleFirstFloor.add_location(BaseConnection(loc05, lambda state: state.event("has_sword"),
                                                 ["King"]))
    castleFirstFloor.add_location(BaseConnection(loc18, lambda state: state.event("has_mrhugs"),
                                                 ["King"]))
    castleFirstFloor.add_location(BaseConnection(loc19, lambda state: state.event("has_mrhugs")))

    castleShieldChest.add_connection(BaseConnection(castleFirstFloor, lambda state: True))
    castleShieldChest.add_statechange(StateChange(["has_shield"], [True],
                                                 lambda state: not state.event("has_shield") and not state.event("sac_shield"),
                                                 ["Shield"]))
    
    castleMapChest.add_connection(BaseConnection(castleFirstFloor, lambda state: True))
    castleMapChest.add_connection(BaseConnection(castleRoof, lambda state: state.get_jump() >= 3))
    castleMapChest.add_statechange(StateChange(["has_map"], [True],
                                               lambda state: not state.event("has_map") and not state.event("sac_map"),
                                               ["map"]))
    castleMapChest.add_statechange(StateChange(["has_compass"], [True],
                                               lambda state: not state.event("has_compass") and not state.event("sac_compass"),
                                               ["compass"]))
    
    castleRoof.add_connection(BaseConnection(castleMapChest, lambda state: True))
    # castleRoof.add_connection(BaseConnection(lonksHouse, lambda state: True)) NOT NEEDED because we can always go through the castle instead
    castleRoof.add_connection(BaseConnection(princessRoom, lambda state: True))

    princessRoom.add_connection(BaseConnection(castleRoof, lambda state: state.get_jump() >= 3))
    princessRoom.add_connection(BaseConnection(castleMinions, lambda state: True))
    princessRoom.add_statechange(StateChange(["has_mrhugs"], [True],
                                           lambda state: not state.event("has_mrhugs") and not state.event("sac_mrhugs"),
                                           ["Mrhugs"]))
    princessRoom.add_location(BaseConnection(loc04, lambda state: state.event("has_sword")))
    princessRoom.add_location(BaseConnection(loc11, lambda state: state.event("has_mrhugs")))
    princessRoom.add_location(BaseConnection(loc19, lambda state: state.event("has_mrhugs")))
    
    volcanoTopExit.add_connection(BaseConnection(elder, lambda state: True))
    volcanoTopExit.add_connection(BaseConnection(chicken, lambda state: True))
    volcanoTopExit.add_connection(BaseConnection(lavaTrinket, lambda state: True))

    lavaTrinket.add_connection(BaseConnection(volcanoTopExit, lambda state: state.get_jump() >= 2))
    lavaTrinket.add_connection(BaseConnection(volcanoDropStone, lambda state: True))
    lavaTrinket.add_statechange(StateChange(["has_lavaTrinket"], [True],
                                       lambda state: not state.event("has_lavaTrinket") and not state.event("sac_lavaTrinket"),
                                       ["Lavatrinket"]))
    
    volcanoDropStone.add_connection(BaseConnection(lavaTrinket, lambda state: state.get_jump() >= 2))
    volcanoDropStone.add_connection(BaseConnection(volcanoBridge, lambda state: True))

    volcanoBridge.add_connection(BaseConnection(volcanoDropStone, lambda state: True))
    volcanoBridge.add_connection(BaseConnection(belowVolcanoBridge, lambda state: True))
    volcanoBridge.add_connection(BaseConnection(sewer, lambda state: state.get_jump() >= 3 or state.event("has_sword")))

    sewer.add_connection(BaseConnection(castleFirstFloor, lambda state: state.get_jump() >= 3, ["Open Castle Floor"]))
    sewer.add_connection(BaseConnection(volcanoBridge, lambda state: True))

    belowVolcanoBridge.add_connection(BaseConnection(leftOfDragon, lambda state: state.event("has_shovel")))
    belowVolcanoBridge.add_connection(BaseConnection(goldRoom, lambda state: True))

    goldRoom.add_connection(BaseConnection(rightOfDragon, lambda state: True))
    goldRoom.add_connection(BaseConnection(sewerPipe, lambda state: state.get_jump() >= 2))

    leftOfDragon.add_connection(BaseConnection(volcanoGeyser, lambda state: state.event("has_shovel")))
    leftOfDragon.add_location(BaseConnection(loc10, lambda state: state.event("has_shovel")))
    leftOfDragon.add_location(BaseConnection(loc14, lambda state: not state.event("has_shield") and not state.event("has_lavaTrinket"), ["Dragon"]))
    leftOfDragon.add_location(BaseConnection(loc29, lambda state: state.event("has_shield") and not state.event("has_lavaTrinket"), ["Dragon"]))
    leftOfDragon.add_location(BaseConnection(loc36, lambda state: not state.event("has_shield") and state.event("has_lavaTrinket"), ["Dragon"]))
    leftOfDragon.add_location(BaseConnection(loc41, lambda state: state.event("has_shield") and state.event("has_lavaTrinket"), ["Dragon"]))

    rightOfDragon.add_connection(BaseConnection(volcanoGeyser, lambda state: True))
    rightOfDragon.add_location(BaseConnection(loc14, lambda state: True, ["Dragon"]))
    rightOfDragon.add_location(BaseConnection(loc16, lambda state: state.event("has_sword"), ["Dragon"]))
    rightOfDragon.add_location(BaseConnection(loc29, lambda state: state.event("has_shield") and not state.event("has_lavaTrinket"), ["Dragon"]))
    rightOfDragon.add_location(BaseConnection(loc36, lambda state: not state.event("has_shield") and state.event("has_lavaTrinket"), ["Dragon"]))
    rightOfDragon.add_location(BaseConnection(loc41, lambda state: state.event("has_shield") and state.event("has_lavaTrinket"), ["Dragon"]))
    rightOfDragon.add_location(BaseConnection(loc43, lambda state: state.event("has_mrhugs"), ["Dragon"]))

    sewerPipe.add_connection(BaseConnection(goldRoom, lambda state: True))
    sewerPipe.add_location(BaseConnection(loc35, lambda state: True, ["Sewer Pipe"]))

    volcanoGeyser.add_connection(BaseConnection(leftOfDragon, lambda state: True))
    volcanoGeyser.add_connection(BaseConnection(ultimateDoor, lambda state: state.get_jump() >= 2))

    ultimateDoor.add_connection(BaseConnection(volcanoGeyser, lambda state: True))

    castleMinions.add_connection(BaseConnection(castleFirstFloor, lambda state: state.event("castleBridgeDown")))
    castleMinions.add_location(BaseConnection(loc13, lambda state: state.event("has_mrhugs")))
    castleMinions.add_location(BaseConnection(loc25, lambda state: state.event("has_sword")))

    # Build full graph
    empty_state: ReventureState = ReventureState()
    todo_regions: typing.List[Region] = []
    todo_regions = [Region(lonksHouse, empty_state)]
    todo_regions[0].apstate.potapitems.append(APItems())
    # todo_regions.append(Region(loc63, empty_state, location=True))

    regions_dict: typing.Dict[str, Region] = {}
    done_regions: typing.List[Region] = []
    while todo_regions:
        region: Region = todo_regions.pop(0)
        regions_dict[region.name] = region
        base_region = region.base_region
        for base_connection in base_region.connections:
            if not base_connection.can_use(region.state):
                continue
            new_region = Region(base_connection.goal_region, region.state)
            region.add_connection(Connection(new_region.name, base_connection.apitems))
            if is_region_in_list(new_region, done_regions) or is_region_in_list(new_region, todo_regions):
                continue
            todo_regions.append(new_region)
        for location in base_region.locations:
            if not location.can_use(region.state):
                continue
            new_region = Region(location.goal_region, empty_state, location=True)
            region.add_connection(Connection(new_region.name, location.apitems))
            if is_region_in_list(new_region, done_regions) or is_region_in_list(new_region, todo_regions):
                continue
            # No reason to work through locations. So add to regions_dict and done_regions
            regions_dict[new_region.name] = new_region
            done_regions.append(new_region)

        for statechange in base_region.statechange:
            if not statechange.can_use(region.state):
                continue
            # Build new state
            new_state = copy.deepcopy(region.state)
            for i in range(len(statechange.states)):
                new_state.state[statechange.states[i]] = statechange.values[i]

            new_region = Region(region.base_region, new_state)
            region.add_connection(Connection(new_region.name, statechange.apitems))
            if is_region_in_list(new_region, done_regions) or is_region_in_list(new_region, todo_regions):
                continue
            todo_regions.append(new_region)
        done_regions.append(region)
    print(f"Regioncount: {len(done_regions)}")

    print("Setting up parents")

    # Setup parents
    for region in done_regions:
        for connection in region.connections:
            regions_dict[connection.name].add_parent(region, connection.apitems)

    # Merge Regions
    
    # print("Merging regions")
    # change = True
    # while change:
    #     change = False
    #     for region in done_regions:
    #         # Free movement between two regions => merge
    #         if len(region.parents) > 0:
    #             # print(f"Running for {region.name}")
    #             for parent in region.parents:
    #                 if parent == region.name:
    #                     region.parents.remove(region.name)
    #                     region.remove_connection(region.name)

    #             for parent in region.parents:
    #                 # print(f"Parent: {parent}")
    #                 if not parent in [con.name for con in region.connections]:
    #                     continue

    #                 parent_region = regions_dict[parent]
    #                 parent_region.merge(region)
    #                 done_regions.remove(region)
    #                 regions_dict.pop(region.name)
    #                 change = True
    #                 break

    print(f"Regioncount: {len(done_regions)}")
    # Setup Apstate
    added_new = True
    while added_new:
        added_new = False
        print("Adding apstates")
        parent_todo_regions = copy.deepcopy(done_regions)
        while len(parent_todo_regions) > 0:
            region = parent_todo_regions[0]
            rec_parent: bool = True
            while rec_parent:
                rec_parent = False
                for parent in region.parents:
                    if parent in parent_todo_regions:
                        region = regions_dict[parent]
                        rec_parent = True
                        break
            parent_todo_regions.remove(region)
            for connection in region.connections:
                child = regions_dict[connection.name]
                prevState = copy.deepcopy(child.apstate)
                for potapitems in region.apstate.potapitems:
                    new_potapitems = copy.deepcopy(potapitems)
                    new_potapitems.add_apitems(connection.apitems.apitems)
                    child.apstate.potapitems.append(new_potapitems)
                child.apstate.reduce_all()
                if len(prevState.potapitems) != len(child.apstate.potapitems):
                    added_new = True
                    continue
                for i in range(len(child.apstate.potapitems)):
                    for j in range(len(child.apstate.potapitems[i].apitems)):
                        if child.apstate.potapitems[i].apitems[j] != prevState.potapitems[i].apitems[j]:
                            added_new = True


    # Remove duplicate solutions
    print("Removing duplicate solutions")
    for region in done_regions:
        if not region.location:
            continue
        # if region.name == "14: Dracar-ish":
        #     print("Debug")
        parent_diffed_by_apitems: typing.Dict[str, typing.List[Region]] = {}
        for parentName in region.parents:
            parent = regions_dict[parentName]
            connection = parent.get_connection(region.name)
            for apitems in parent.apstate.potapitems:
                loc_apitems = copy.deepcopy(apitems)
                loc_apitems.add_apitems(connection.apitems.apitems)
                apitems_string = loc_apitems.to_string()
                if not apitems_string in parent_diffed_by_apitems.keys():
                    parent_diffed_by_apitems[apitems_string] = [parent]
                else:
                    parent_diffed_by_apitems[apitems_string].append(parent)
        # Find used apitem sets, whilst removing unnecessary ones
        used_apstates: typing.List[str] = []
        for apstate_str in parent_diffed_by_apitems.keys():
            if len(used_apstates) == 0:
                used_apstates.append(apstate_str)
                continue
            apstate = APItems()
            apstate.add_apitems_from_string(apstate_str)
            new = True
            remove = []
            for used_apstate_str in used_apstates:
                used_apstate = APItems()
                used_apstate.add_apitems_from_string(used_apstate_str)
                if apstate.is_subset(used_apstate):
                    remove.append(used_apstate_str)
                elif used_apstate.is_subset(apstate):
                    new = False
                    break
            for rem in remove:
                used_apstates.remove(rem)
            if new:
                used_apstates.append(apstate_str)

        # Remove all parents not in used_apstates
        toRemove: typing.List[Region] = []
        for parentName in region.parents:
            parent = regions_dict[parentName]
            is_used = False
            for potapitems in parent.apstate.potapitems:
                loc_apitems = copy.deepcopy(potapitems)
                loc_apitems.add_apitems(connection.apitems.apitems)
                apitems_string = loc_apitems.to_string()
                if apitems_string in used_apstates:
                    is_used = True
                    break
            if not is_used:
                toRemove.append(parent)
        for parent in toRemove:
            parent.remove_connection(region.name)
            region.parents.remove(parent.name)

        # For each apstate only keep parent with lowest complexity
        for apstate in parent_diffed_by_apitems.keys():
            apstate_parents = parent_diffed_by_apitems[apstate]
            if not apstate in used_apstates: # Not in used apstates, remove all parents
                continue
            # In case of a single parent, nothing happens here, so no need to check
            best_parent = apstate_parents[0]
            best_complexity = best_parent.complexity
            for parent in apstate_parents[1:]:
                if parent.complexity >= best_complexity:
                    parent.remove_connection(region.name)
                    region.parents.remove(parent.name)
                else:
                    best_parent.remove_connection(region.name)
                    region.parents.remove(best_parent.name)
                    best_parent = parent
                    best_complexity = parent.complexity

    print(f"Regioncount: {len(done_regions)}")
    changed = True
    while changed:
        print(f"Regioncount: {len(done_regions)}")
        # if len(regions_dict["63: You Don\'t Mess With Chicken"].parents) == 1:
        #     print("Debug")
        # if len(regions_dict["Chicken__has_shield"].parents) == 0:
        #     print("Debug")
        # Remove any regions (Except LonksHouse) that have no parents
        changed = False
        for region in done_regions[1:]:
            if region.location:
                continue
            # One way regions
            if len(region.parents) == 0:
                noparents = True
                # print(f"Running for {region.name}")
                for connection in region.connections:
                    child = regions_dict[connection.name]
                    child.parents.remove(region.name)
                done_regions.remove(region)
                regions_dict.pop(region.name)
                changed = True
        if changed:
            continue

        # Remove any regions without connections
        # Remove any regions only connecting to a parent
        toPrune = []
        for region in done_regions[1:]:
            if region.location:
                continue
            if len(region.connections) == 0:
                toPrune.append(region)
                continue
            # if len(region.connections) == 1:
            #     for parent in region.parents:
            #         if parent == region.connections[0].name:
            #             toPrune.append(region)
            #             continue
        for region in toPrune:
            for parent in region.parents:
                regions_dict[parent].remove_connection(region.name)
            for connection in region.connections:
                regions_dict[connection.name].parents.remove(region.name)
            done_regions.remove(region)
            regions_dict.pop(region.name)
        if len(toPrune) != 0:
            changed = True
            continue

        toPrune = None

        for region in done_regions[1:]:
            if region.location:
                continue
            # One way regions
            if len(region.connections) == 1 and len(region.parents) == 1:
                # if region.name == "VolcanoTopExit__chicken__sword":
                #     print("Debug")
                parent = regions_dict[region.parents[0]]
                # print(f"Running single for {region.name} -> {region.connections[0]}")
                child = regions_dict[region.connections[0].name]
                if parent.name == child.name: # Loop back to parent
                    parent.remove_connection(region.name)
                    parent.parents.remove(region.name)
                    toPrune = region
                    done_regions.remove(toPrune)
                    regions_dict.pop(toPrune.name)
                    break
                connection_from_parent = parent.get_connection(region.name)
                connection_to_child = region.connections[0]
                connection_to_child.apitems.add_apitems(connection_from_parent.apitems.apitems)
                parent.remove_connection(region.name)
                parent.add_connection(connection_to_child)
                child.parents.remove(region.name)
                child.parents.append(parent.name)
                toPrune = region
                done_regions.remove(toPrune)
                regions_dict.pop(toPrune.name)
                break

            # Free movement between two regions => merge
            if len(region.parents) > 0:
                # print(f"Running for {region.name}")
                for parent in region.parents:
                    if parent == region.name:
                        region.parents.remove(region.name)
                        region.remove_connection(region.name)

                for parent in region.parents:
                    # print(f"Parent: {parent}")
                    if not parent in [con.name for con in region.connections]:
                        continue

                    parent_region = regions_dict[parent]
                    parent_region.merge(region)
                    toPrune = region
                    break
            if toPrune != None:
                done_regions.remove(toPrune)
                regions_dict.pop(toPrune.name)
                break
        
        if toPrune != None:
            changed = True
           

    plantuml = create_plant_uml(done_regions)

    print(f"Regioncount: {len(done_regions)}")

    # write to file
    with open("reventure_graph.plantuml", "w") as file:
        file.write(plantuml)