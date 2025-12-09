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
    intro_to_cbf_bump_intro = world.get_entrance("Intro to CBF Bump Intro")

    set_rule(intro_to_cbf_bump_intro, lambda state: True)



def set_all_location_rules(world: BoTealLotusWorld) -> None:
    add_rule(world.get_location("Intro Teapot"), lambda state: True)
    add_rule(world.get_location("Intro Kodama"), lambda state: state.has_any(["Staff"], world.player))


def set_completion_condition(world: BoTealLotusWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
