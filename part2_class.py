"""
Class
"""
class params:
  def __init__(self):
    self.customer = ['H','J','L','T']
    self.product = ['P','Q','R','S']
    self.plant = ['A','B','C','D']
    self.production = {
    'A': {
        'P': {
            'H': 64,
            'J': 67,
            'L': 2,
            'T': 10,
        },
        'Q': {
            'H': 58,
            'J': 109,
            'L': 61,
            'T': 20,
        },
        'R': {
            'H': 24,
            'J': 244,
            'L': 386,
            'T': 6,
        },
        'S': {
            'H': 6,
            'J': 117,
            'L': 660,
            'T': 15,
        },
    },
    'B': {
        'P': {
            'H': 31,
            'J': 131,
            'L': 11,
            'T': 1,
        },
        'Q': {
            'H': 115,
            'J': 88,
            'L': 96,
            'T': 11,
        },
        'R': {
            'H': 44,
            'J': 250,
            'L': 12,
            'T': 66,
        },
        'S': {
            'H': 0,
            'J': 224,
            'L': 3,
            'T': 13,
        },
    },
    'C': {
        'P': {
            'H': 2,
            'J': 2,
            'L': 6,
            'T': 22,
        },
        'Q': {
            'H': 17,
            'J': 55,
            'L': 30,
            'T': 9,
        },
        'R': {
            'H': 6,
            'J': 3,
            'L': 2,
            'T': 19,
        },
        'S': {
            'H': 0,
            'J': 56,
            'L': 134,
            'T': 761,
        },
    },
    'D': {
        'P': {
            'H': 3,
            'J': 0,
            'L': 1,
            'T': 17,
        },
        'Q': {
            'H': 10,
            'J': 48,
            'L': 13,
            'T': 10,
        },
        'R': {
            'H': 26,
            'J': 3,
            'L': 0,
            'T': 9,
        },
        'S': {
            'H': 4,
            'J': 3,
            'L': 3,
            'T': 11,
        },
    }
  }
    self.labour_hours = {
    'A': {
        'P': 100,
        'Q': 200,
        'R': 100,
        'S': 100,
    },
    'B': {
        'P': 100,
        'Q': 150,
        'R': 90,
        'S': 90,
    },
    'C': {
        'P': 80,
        'Q': 210,
        'R': 90,
        'S': 70,
    },
    'D': {
        'P': 300,
        'Q': 240,
        'R': 100,
        'S': 140,
    }
  }
    self.distance = {
    'A': {
        'H': 128,
        'J': 170,
        'L': 63,
        'T': 216,
    },
    'B': {
        'H': 28,
        'J': 51,
        'L': 100,
        'T': 85,
    },
    'C': {
        'H': 76,
        'J': 100,
        'L': 121,
        'T': 121,
    },
    'D': {
        'H': 873,
        'J': 878,
        'L': 827,
        'T': 913,
    }
  }
    self.demand = {
    'H': {
        'P': 100,
        'Q': 200,
        'R': 100,
        'S': 10,
    },
    'J': {
        'P': 200,
        'Q': 300,
        'R': 500,
        'S': 400,
    },
    'L': {
        'P': 20,
        'Q': 200,
        'R': 400,
        'S': 800,
    },
    'T': {
        'P': 50,
        'Q': 50,
        'R': 100,
        'S': 800,
    }
  }
    self.max_capacity = {
    'A': 210000,
    'B': 120000,
    'C': 190000,
    'D': 200000
    }
    self.labour_cost = {
    'A': 30,
    'B': 30,
    'C': 42,
    'D': 13
    }
    self.load_size = 3
    self.cost_per_mile = 30

"""
Functions
"""
