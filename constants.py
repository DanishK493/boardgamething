ROWS = 16
COLS = 16
TILE_SIZE = 16
SIDE_PANEL = 150
SCREEN_WIDTH = TILE_SIZE * COLS
SCREEN_HEIGHT = TILE_SIZE * ROWS
FPS = 60
ANIMATION_STEPS = 3
ANIMATIOn_DELAY = 150
TOWER_LEVELS = 4
SPAWN_COOLDOWN = 400
HEALTH = 100
MONEY = 650
BUY_COST = 200
UPGRADE_COST = 100
DAMAGE = 5
KILL_REWARD = 1
LEVEL_COMPLETE_REWARD = 100
TOTAL_LEVELS = 15
TOWER_DATA = [
    {"range":45,"cooldown":1500},
    {"range":55,"cooldown":1200},
    {"range":65,"cooldown":1000},
    {"range":75,"cooldown":900}
]
ENEMY_DATA = {
    "weak": {
    "health": 10,
    "speed": 1
  },
    "medium": {
    "health": 20,
    "speed": 2
  },
    "strong": {
    "health": 30,
    "speed": 3
  }
}
ENEMY_SPAWN_DATA = [
  {
    "weak": 15,
    "medium": 0,
    "strong": 0
  },
  {
    "weak": 30,
    "medium": 0,
    "strong": 0
  },
  {
    "weak": 20,
    "medium": 5,
    "strong": 0
  },
  {
    "weak": 30,
    "medium": 15,
    "strong": 0
  },
  {
    "weak": 5,
    "medium": 20,
    "strong": 0
  },
  {
    "weak": 15,
    "medium": 15,
    "strong": 1
  },
  {
    "weak": 20,
    "medium": 25,
    "strong": 2
  },
  {
    "weak": 10,
    "medium": 20,
    "strong": 5
  },
  {
    "weak": 15,
    "medium": 10,
    "strong": 5
  },
  {
    "weak": 0,
    "medium": 100,
    "strong": 0
  },
  {
    "weak": 5,
    "medium": 10,
    "strong": 7
  },
  {
    "weak": 0,
    "medium": 15,
    "strong": 10
  },
  {
    "weak": 15,
    "medium": 15,
    "strong": 15
  },
  {
    "weak": 20,
    "medium": 20,
    "strong": 20
  },
  {
    "weak": 25,
    "medium": 25,
    "strong": 25
  }
]