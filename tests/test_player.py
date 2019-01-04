import pytest
from gaia.players import PlayerResources


@pytest.mark.parametrize("power_before, gain_amount, power_after, description", [
    ({0: 4, 1: 4, 2: 0}, 0, {0: 4, 1: 4, 2: 0}, "No power gain"),
    ({0: 4, 1: 4, 2: 0}, 2, {0: 2, 1: 6, 2: 0}, "Small power gain"),
    ({0: 4, 1: 4, 2: 0}, 4, {0: 0, 1: 8, 2: 0}, "First bowl power gain"),
    ({0: 4, 1: 4, 2: 0}, 6, {0: 0, 1: 6, 2: 2}, "First/second bowl small power gain"),
    ({0: 4, 1: 4, 2: 0}, 8, {0: 0, 1: 4, 2: 4}, "First/second bowl medium power gain"),
    ({0: 4, 1: 4, 2: 0}, 10, {0: 0, 1: 2, 2: 6}, "First/second bowl large power gain"),
    ({0: 4, 1: 4, 2: 0}, 12, {0: 0, 1: 0, 2: 8}, "First/second bowl full power gain"),
    ({0: 4, 1: 4, 2: 0}, 13, {0: 0, 1: 0, 2: 8}, "First/second bowl overfull power gain"),
    ({0: 0, 1: 4, 2: 0}, 0, {0: 0, 1: 4, 2: 0}, "Second bowl no power gain"),
    ({0: 0, 1: 4, 2: 0}, 2, {0: 0, 1: 2, 2: 2}, "Second bowl partial power gain"),
    ({0: 0, 1: 4, 2: 0}, 4, {0: 0, 1: 0, 2: 4}, "Second bowl full power gain"),
    ({0: 0, 1: 4, 2: 0}, 5, {0: 0, 1: 0, 2: 4}, "Second bowl overfull power gain"),
    ({0: 0, 1: 0, 2: 4}, 0, {0: 0, 1: 0, 2: 4}, "Third bowl no power gain"),
    ({0: 0, 1: 0, 2: 4}, 2, {0: 0, 1: 0, 2: 4}, "Third bowl overfull power gain"),
])
def test_gain_power(power_before, gain_amount, power_after, description, default_player_resources):
    default_player_resources.power_bowls = power_before
    default_player_resources.gain_power(gain_amount)
    assert default_player_resources.power_bowls == power_after, "Failed: " + description
