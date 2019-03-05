from gaia.gamestate.gamestate import GameState


class MoveGenerator:

    def __init__(self, gamestate: GameState, player_id: str):
        self.gamestate = gamestate
        self.player_id = player_id

    # Generate a list of all possible moves for a specific player on a specific turn.
    def perform(self):
        self.generate_build_actions()
        self.generate_upgrade_actions()

    # internal methods
    def generate_build_actions(self):
        pass

    def generate_upgrade_actions(self):
        pass

    def generate_bonus_actions(self):
        pass

    def generate_science_actions(self):
        pass

    def generate_pass_actions(self):
        pass
