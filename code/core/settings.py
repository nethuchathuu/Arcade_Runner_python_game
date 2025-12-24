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

ASSETS_PATH = os.path.join(BASE_DIR, CONFIG['assets_path'])
