import logging
import sys


def init_logging():
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.DEBUG,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


# Bot

PYAUTOGUI_SLEEP_SECONDS_BETWEEN_CALLS = 2
START_SLEEP_SECONDS = 10

DO_OPEN_MONKEYS = True

CLICK_ON_MATCHING_CONFIDENCE = 0.9
WAIT_FOR_MATCHING_CONFIDENCE = 0.9

RELOAD_TOWER_COUNTER = 3

CHECK_LEVEL_UP_COUNTER = 10
CHECK_GAME_PAUSED_COUNTER = 30
CHECK_DEFEATED_COUNTER = 10
ABILITY_COOLDOWN = 15

LOGS_DIR = '_logs'

# Menu
BUTTON_MENU_PLAY = 'resources/menu/button_menu_play.jpg'
BUTTON_MENU_MAPS_BEGINNER = 'resources/menu/button_menu_maps_beginner.jpg'
BUTTON_MENU_MAPS_EXPERT = 'resources/menu/button_menu_maps_expert.jpg'
BUTTON_MENU_EASY_DIFF = 'resources/menu/button_menu_easy_diff.jpg'
BUTTON_MENU_HARD_DIFF = 'resources/menu/button_menu_hard_diff.jpg'
BUTTON_MENU_STANDARD_MODE = 'resources/menu/button_menu_standard_mode.jpg'
BUTTON_MENU_IMPOPPABLE_MODE = 'resources/menu/button_menu_impoppable_mode.jpg'
BUTTON_MENU_CHIMPS_MODE = 'resources/menu/button_menu_chimps_mode.jpg'
BUTTON_MENU_BONUS_MAP = 'resources/menu/bonus_map_icon.jpg'
BUTTON_MENU_NEXT_END = 'resources/menu/button_next_end_game.jpg'

BUTTON_GAME_START = 'resources/menu/button_game_start.jpg'
BUTTON_GAME_FAST_FORWARD = 'resources/menu/button_game_fast_forward.jpg'
BUTTON_GAME_TO_HOME = 'resources/menu/button_game_to_home.jpg'
BUTTON_GAME_RESTART = 'resources/menu/button_game_restart.jpg'
BUTTON_GAME_RESTART_CONFIRM = 'resources/menu/button_game_confirm_restart.jpg'
BUTTON_GAME_FREEPLAY = 'resources/menu/button_game_freeplay.jpg'

PROMPT_DEFEAT = 'resources/menu/prompt_defeat.jpg'
PROMPT_LEVEL_UP = 'resources/menu/prompt_level_up.jpg'

PROMPT_OVERWRITE = 'resources/menu/prompt_overwrite.jpg'
BUTTON_OVERWRITE_OK = 'resources/menu/button_overwrite_ok.jpg'

CAN_AFFORD_TOWER = 'resources/menu/can_afford_tower.jpg'

# Events
COLLECTION_XS = range(400, 1200, 100)
COLLECTION_Y = 450

BUTTON_EVENT_COLLECT = 'resources/menu/button_event_collect.jpg'
BUTTON_EVENT_CONTINUE = 'resources/menu/button_event_continue.jpg'

# Towers
TOWER_NINJA_UPGRADE = 'resources/towers/ninja/upgrade_{}_{}.jpg'
TOWER_SUPER_UPGRADE = 'resources/towers/super/upgrade_{}_{}.jpg'
TOWER_DART_UPGRADE = 'resources/towers/dart/upgrade_{}_{}.jpg'
TOWER_BOOMERANG_UPGRADE = 'resources/towers/boomerang/upgrade_{}_{}.jpg'
TOWER_WIZARD_UPGRADE = 'resources/towers/wizard/upgrade_{}_{}.jpg'
TOWER_SNIPER_UPGRADE = 'resources/towers/sniper/upgrade_{}_{}.jpg'
TOWER_DRUID_UPGRADE = 'resources/towers/druid/upgrade_{}_{}.jpg'
TOWER__UPGRADE = 'resources/towers/ninja/upgrade_{}_{}.jpg'

# Heroes
HERO_SELECTED_OBYN_1 = 'resources/towers/heroes/obyn_1.jpg'
HERO_SELECTED_OBYN_2 = 'resources/towers/heroes/obyn_2.jpg'
HERO_SELECTED_OBYN_3 = 'resources/towers/heroes/obyn_3.jpg'

HERO_SELECTED = {'obyn': [HERO_SELECTED_OBYN_1, HERO_SELECTED_OBYN_2, HERO_SELECTED_OBYN_3]}

# Maps
BEGINNER_MAPS_PAGE_1 = [['monkey_meadow', 'tree_stump', 'town_center'],['the_cabin', 'resort', 'skates']]
BEGINNER_MAPS_PAGE_2 = [['lotus_island', 'candy_falls', 'winter_park'],['carved', 'park_Path', 'alpine_run']]
BEGINNER_MAPS_PAGE_3 = [['frozen_over', 'in_the_loop', 'cubism'],['four_circles', 'hedge', 'end_of_the_road']]
BEGINNER_MAPS_PAGE_4 = [['logs', '', ''],['', '', '']]

BEGINNER_MAPS = [BEGINNER_MAPS_PAGE_1, BEGINNER_MAPS_PAGE_2, BEGINNER_MAPS_PAGE_3, BEGINNER_MAPS_PAGE_4]

BEGINNER_MAP_FILES = 'resources/maps/{}/'
DART_SPOT = 'dart.jpg'
WIZARD_SPOT = 'wizard.jpg'
DRUID_SPOT = 'druid.jpg'
SNIPER_SPOT = 'sniper.jpg'
BOOMERANG_SPOT = 'boomerang.jpg'
NINJA_SPOT = 'ninja.jpg'
HERO_SPOT = 'hero.jpg'
MAP_ICON = 'map.jpg'

# Dark Castle
MAPS_DARK_CASTLE = 'resources/maps/dark_castle/map.jpg'

MAPS_POS_DARK_CASTLE_INTERSECTION_TOP = 'resources/maps/dark_castle/intersection_top_path.jpg'
MAPS_POS_DARK_CASTLE_INTERSECTION_BOTTOM = 'resources/maps/dark_castle/intersection_bottom_path.jpg'
MAPS_POS_DARK_CASTLE_TOP_LEFT_MAIN_ROAD = 'resources/maps/dark_castle/top_left_main_road.jpg'

MAPS_ROUND_DARK_CASTLE_4 = 'resources/maps/dark_castle/round_4.jpg'  # 23
MAPS_ROUND_DARK_CASTLE_20 = 'resources/maps/dark_castle/round_20.jpg'  # 163

# Hotkeys
HOTKEY_UPGRADE_1 = ','
HOTKEY_UPGRADE_2 = '.'
HOTKEY_UPGRADE_3 = '/'
HOTKEY_UPGRADES = [HOTKEY_UPGRADE_1, HOTKEY_UPGRADE_2, HOTKEY_UPGRADE_3]

HOTKEY_HERO = "u"
HOTKEY_TOWER_DART = 'q'
HOTKEY_TOWER_BOOMERANG = 'w'
HOTKEY_TOWER_WIZARD = 'a'
HOTKEY_TOWER_DRUID = 'g'
HOTKEY_TOWER_NINJA = 'd'
HOTKEY_TOWER_SNIPER = 'z'
HOTKEY_TOWER_SUPER_MONKEY = 's'

MAP_GRID_OFFSET_X = 240
MAP_GRID_OFFSET_Y = 80

MAP_TILE_SIZE_X = 300
MAP_TILE_SIZE_Y = 240

MAP_TILE_SPACING_X = 60
MAP_TILE_SPACING_Y = 30

# 585, 935, 1295