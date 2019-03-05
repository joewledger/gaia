

def valid_moves_example_response():
    return [
        { # Behaves uniquely. Must choose to do before other moves. This must be remembered between player turns. There can be multiple.
            'type': 'leech',
            'player_id': '1234',
            'amount': 3
        },

        {
            'type': 'build',
            'hex': 11,
            'navigation': 4,
            'dig': 1-3
        },

        {
            'type': 'upgrade',
            'hex': 23,
            'opt1': 1,
            'opt2': None
        },

        {
            'type': 'action',
            'bonus-action': 4
        },

        {
            'type': 'pass',
            'tiles': [1, 5, 7, 11]
        }
    ]