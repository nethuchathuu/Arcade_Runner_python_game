import json
import os

# Load config
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')

with open(CONFIG_PATH, 'r') as f:
    CONFIG = json.load(f)

SCREEN_WIDTH = CONFIG['screen_width']
SCREEN_HEIGHT = CONFIG['screen_height']
CAPTION = CONFIG['caption']

X_POSITION = CONFIG['x_position']
GROUND_Y = CONFIG['ground_y']
Y_POSITION = GROUND_Y

DIFFICULTY = CONFIG['difficulty']
DIFFICULTY_SETTINGS = CONFIG['difficulty_settings']
CURRENT_SETTINGS = DIFFICULTY_SETTINGS[DIFFICULTY]

RISE_SPEED = CONFIG['physics']['rise_speed']
FALL_SPEED = CONFIG['physics']['fall_speed']
ANIMATION_SPEED = CONFIG['physics'].get('animation_speed', 120)
SCROLL_SPEED = CONFIG['physics'].get('scroll_speed', 2)
JUMP_FRAME_DURATION = CONFIG['physics'].get('jump_frame_duration', 90)
GRAVITY = CONFIG['physics'].get('gravity', 1.2)
JUMP_VELOCITY = CONFIG['physics'].get('jump_velocity', -20)
JUMP_HORIZONTAL_SPEED = CONFIG['physics'].get('jump_horizontal_speed', 3)
EXTRA_FORCE_HOLDING = CONFIG['physics'].get('extra_force_holding', -1.0)
MAX_HOLD_TIME = CONFIG['physics'].get('max_hold_time', 1000)
MAX_JUMP_HEIGHT = CONFIG['physics'].get('max_jump_height', 720)
MAX_FORWARD_DISPLACEMENT = CONFIG['physics'].get('max_forward_displacement', 500)

# Roll Settings
ROLL_SPEED = 20
ROLL_FRAME_DURATION = 85

ASSETS_PATH = os.path.join(BASE_DIR, CONFIG['assets_path'])
