import typing
from Options import Option, Range, Choice, Toggle


class GemSettings(Choice):
    """How the 4 Gems are handled."""
    display_name = "Gems"
    option_vanilla = 0
    option_randomized = 1
    option_free = 2
    default = 1

class RequiredEndings(Range):
    """How many endings are required to be completed to win the game."""
    display_name = "Endings"
    range_start = 1
    range_end = 99
    default = 40

class RequireFailableJumps(Toggle):
    """This includes jumps in logic that are difficult and result in death if missed"""
    display_name = "RequireFailableJumps"
    option_true = 1
    option_false = 0
    default = 0

# class FinalAct(Toggle):
#     """Whether you will need to collect the 3 keys and beat the final act to complete the game."""
#     display_name = "Final Act"
#     option_true = 1
#     option_false = 0
#     default = 0


# class Downfall(Toggle):
#     """When Downfall is Installed this will switch the played mode to Downfall"""
#     display_name = "Downfall"
#     option_true = 1
#     option_false = 0
#     default = 0


reventure_options: typing.Dict[str, type(Option)] = {
    "endings": RequiredEndings,
    "gems": GemSettings,
    "hardjumps": RequireFailableJumps,
}
