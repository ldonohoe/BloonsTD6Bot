import pyautogui as pag
import pydirectinput as pdi
import cv2  # Needed for fuzzy matching with pyautogui
import logging
import time
from abc import ABCMeta, abstractmethod

import config

class Bot(metaclass=ABCMeta):

    def __init__(self):
        self._offset = (0, 0)
        self._monkeys_collection_path = None
        self._num_collected_monkeys = 0
        self._game_counter = 0
        self._wait_location = None
        self._state = 'HOME'
        pag.PAUSE = config.PYAUTOGUI_SLEEP_SECONDS_BETWEEN_CALLS
        config.init_logging()
        logging.info('Bloons TD6 bot initialising')
        logging.debug('OpenCV loaded from {}'.format(cv2.data.haarcascades))

    @property
    def wait_location(self):
        return self._wait_location

    # Clicks
    @staticmethod
    def click_on(img, numClicks=1):
        x = pag.locateCenterOnScreen(img, confidence=config.CLICK_ON_MATCHING_CONFIDENCE)
        if x is None:
            logging.error(f'Cannot find {img} on screen')
            pag.screenshot('{}/debug_{}.png'.format(config.LOGS_DIR, time.time()))
            raise ValueError('Cannot find {} on screen'.format(img))
        pag.click(x, clicks=numClicks)
        return x

    def _start_game(self, fast_forward=True):
        self.click_on(config.BUTTON_GAME_START)
        if fast_forward:
            self.click_on(config.BUTTON_GAME_FAST_FORWARD)

    def _navigate_home(self):
        if self._state == 'HOME': # already home, nothing to do
            return
        elif self._state =='IN_GAME': # In a game, open menu and hit home button
            pdi.press('`')
            self.click_on(config.BUTTON_GAME_TO_HOME)
        elif self._state == 'NAVIGATING':
            logging.info('Failed navigating, fixing page and returning home')
            while not self._is_present(config.BUTTON_MENU_PLAY) or self._is_present(config.BUTTON_EVENT_COLLECT):
                # While navigating back to home, reset start point of beginner maps to p1
                if self._is_present(config.BUTTON_MENU_MAPS_EXPERT):
                    self.click_on(config.BUTTON_MENU_MAPS_EXPERT)
                    self.click_on(config.BUTTON_MENU_MAPS_BEGINNER)
                pdi.press('esc')
            logging.info('Fixed navigate, back to home')
        time.sleep(5)
        if self._is_present(config.BUTTON_EVENT_COLLECT):
            logging.info('Received reward monkeys')
            self.click_on(config.BUTTON_EVENT_COLLECT)
            self._collect_event_rewards()
            pdi.press('esc')
        self._state='HOME'

    def _collect_event_rewards(self):
        logging.info('Collecting reward monkeys')
        num_collected = 0
        for collection_x in config.COLLECTION_XS:
            pag.click((self._offset[0] + collection_x, self._offset[1] + config.COLLECTION_Y))
            pag.click((self._offset[0] + collection_x, self._offset[1] + config.COLLECTION_Y))
            num_collected += 1
            if self._is_present(config.BUTTON_EVENT_CONTINUE):
                break
        self._monkeys_collection_path = '{}/collected_monkeys_{}.png'.format(config.LOGS_DIR, time.time())
        pag.screenshot(self._monkeys_collection_path)
        self._num_collected_monkeys += num_collected
        self.click_on(config.BUTTON_EVENT_CONTINUE)

    def _load_game(self, game_map):
        if config.DO_OPEN_MONKEYS or self._game_counter == 1:
            game_map.navigate_to()
        else:
            self._load_next_game_trick()

    def _load_next_game_trick(self):
        self.click_on(config.BUTTON_GAME_FREEPLAY)
        pag.press('esc')
        pag.press('esc')
        self.click_on(config.BUTTON_GAME_RESTART)
        self.click_on(config.BUTTON_GAME_RESTART_CONFIRM)

    def _game_completed(self):
        if config.DO_OPEN_MONKEYS:
            self._navigate_home()

    # Waits
    def wait_for(self, img, tower=False, do_all_checks=True):
        wait_counter = 0
        changed = False
        while not self._is_present(img):
            wait_counter += 1
            changeOnCheck = self._do_checks(wait_counter, do_all_checks)
            self._use_abilities(wait_counter)
            changed = changeOnCheck or changed
            if tower and wait_counter > 30:
                raise ValueError()
        return changed

    def _wait_for_map_load(self):
        time.sleep(3)
        if self._is_present(config.PROMPT_OVERWRITE):  # Overwriting existing save
            logging.warning('Overwriting save')
            self.click_on(config.BUTTON_OVERWRITE_OK)
        self.wait_for(config.BUTTON_GAME_START, do_all_checks=False)

    def _wait_for_game_completion(self):
        logging.info('Waiting for game to be completed')
        self.wait_for(config.BUTTON_MENU_NEXT_END, do_all_checks=True)
        logging.info('Game completed')
        self.click_on(config.BUTTON_MENU_NEXT_END)

    # Checks
    def _is_present(self, img):
        self._wait_location = pag.locateCenterOnScreen(img, confidence=config.WAIT_FOR_MATCHING_CONFIDENCE)
        return self._wait_location is not None

    def _do_checks(self, wait_counter, do_all_checks=True):
        changed = False
        changed = self._check_level_up(wait_counter) or changed
        if do_all_checks:
            changed = self._check_game_paused(wait_counter) or changed
            changed = self._check_defeated(wait_counter) or changed
        return changed

    def _use_abilities(self, wait_counter):
        if wait_counter % config.ABILITY_COOLDOWN == 0:
            pdi.press('1')
            pdi.press('2')

    def _check_level_up(self, wait_counter):
        if wait_counter % config.CHECK_LEVEL_UP_COUNTER == 0 and self._is_present(config.PROMPT_LEVEL_UP):
            logging.warning('Level up detected - double clicking screen')
            pag.click()
            pag.click()
            self._check_game_paused(config.CHECK_GAME_PAUSED_COUNTER)
            return True

    def _check_game_paused(self, wait_counter):
        if wait_counter % config.CHECK_GAME_PAUSED_COUNTER == 0 and self._is_present(config.BUTTON_GAME_START):
            logging.warning('Game is paused detected - pressing play')
            self._start_game(fast_forward=False)
            return False # Does not change state of game

    def _check_defeated(self, wait_counter):
        if wait_counter % config.CHECK_DEFEATED_COUNTER == 0 and self._is_present(config.PROMPT_DEFEAT):
            logging.error('Defeat detected: starting new game')
            self.wait_for(config.BUTTON_GAME_TO_HOME)
            self.click_on(config.BUTTON_GAME_TO_HOME)
            raise Exception('Failed map, defeated. Rework tower positions')

    def _check_selected_hero(self, hero_images, hero_name):
        for img in hero_images:
            if self._is_present(img):
                logging.debug('Hero {} correctly selected'.format(hero_name))
                return
        logging.error('Incorrect hero expected. Hero required is {}, but was not found'.format(hero_name))
        raise ValueError('Incorrect hero expected. Hero required is {}, but was not found'.format(hero_name))

    # Main
    def main(self, required_hero=None):
        logging.info('Please navigate to the top left corner of the game, you have {} seconds'.format(
            config.START_SLEEP_SECONDS))
        time.sleep(config.START_SLEEP_SECONDS)
        self._offset = pag.position()
        logging.debug('Screen offset set at {}'.format(self._offset))
        if required_hero:
            self._check_selected_hero(config.HERO_SELECTED[required_hero.lower()], required_hero)

    @abstractmethod
    def _play_game(self):
        pass  # Require implementation
