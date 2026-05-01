data = {

    'ISTTOK': {
        'type':  'tokamak',
        'color': '#FF0000',
        'a':     0.085,
        'B':     0.500,
        'core': {
            'Te': 0.150,
            'ne': 5.00e18,
        },
        'edge': {
            'Te': 0.020,
            'ne': 7.50e17,
        },
        'sol': {
            'Te': 0.0075,
            'ne': 3.50e17,
        },
    },

    'HSX': {
        'type':  'stellarator',
        'color': '#FFA500',
        'a':     0.120,
        'B':     1.000,
        'core': {
            'Te': 2.000,
            'ne': 6.00e18,
        },
        'edge': {
            'Te': 0.060,
            'ne': 8.00e17,
        },
        'sol': {
            'Te': 0.030,
            'ne': 4.50e17,
        },
    },

    'TCV': {
        'type':  'tokamak',
        'color': '#00FF00',
        'a':     0.240,
        'B':     1.440,
        'core': {
            'Te': 1.250,
            'ne': 2.50e19,
        },
        'edge': {
            'Te': 0.100,
            'ne': 3.00e19,
        },
        'sol': {
            'Te': 0.0125,
            'ne': 1.35e19,
        },
    },

    'ASDEX-U': {
        'type':  'tokamak',
        'color': '#00FFFF',
        'a':     0.500,
        'B':     2.500,
        'core': {
            'Te': 3.000,
            'ne': 8.00e19,
        },
        'edge': {
            'Te': 0.400,
            'ne': 4.00e19,
        },
        'sol': {
            'Te': 0.075,
            'ne': 2.00e19,
        },
    },

    'W7-X': {
        'type':  'stellarator',
        'color': '#0000FF',
        'a':     0.500,
        'B':     2.500,
        'core': {
            'Te': 7.000,
            'ne': 3.00e19,
        },
        'edge': {
            'Te': 0.200,
            'ne': 2.75e19,
        },
        'sol': {
            'Te': 0.020,
            'ne': 3.00e18,
        },
    },

    'JET': {
        'type':  'tokamak',
        'color': '#FFC0CB',
        'a':     1.250,
        'B':     2.800,
        'core': {
            'Te': 10.000,
            'ne': 5.00e19,
        },
        'edge': {
            'Te': 1.500,
            'ne': 4.00e19,
        },
        'sol': {
            'Te': 0.150,
            'ne': 3.00e19,
        },
    },

    'ITER': {
        'type':  'tokamak',
        'color': '#7F00FF',
        'a':     2.800,
        'B':     5.680,
        'core': {
            'Te': 12.900,
            'ne': 9.80e19,
        },
        'edge': {
            'Te': 0.200,
            'ne': 6.00e19,
        },
        'sol': {
            'Te': 0.075,
            'ne': 2.00e19,
        },
    },

}

# Lists for iterating
DEVICES      = list(data.keys())
REGIONS      = ['core', 'edge', 'sol']
TOKAMAKS     = [d for d, v in data.items() if v['type'] == 'tokamak']
STELLARATORS = [d for d, v in data.items() if v['type'] == 'stellarators']