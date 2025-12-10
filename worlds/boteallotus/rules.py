from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from .world import BoTealLotusWorld


def set_all_rules(world: BoTealLotusWorld) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.

    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: BoTealLotusWorld) -> None:
    pass



def set_all_location_rules(world: BoTealLotusWorld) -> None:
    add_rule(world.get_location("Intro Teapot"), lambda state: True)
    add_rule(world.get_location("Intro Kodama"), lambda state: True)
    add_rule(world.get_location("Bamboo Forest Kodama 1"), lambda state: True)
    add_rule(world.get_location("Bamboo Forest Kodama 2"), lambda state: True)
    add_rule(world.get_location("Bamboo Forest Kodama 3"), lambda state: True)


def set_completion_condition(world: BoTealLotusWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
