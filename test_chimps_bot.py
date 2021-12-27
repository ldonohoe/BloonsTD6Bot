import logging
import map
import config 
import time
import pydirectinput as pdi
import pyautogui as pag
from bot import Bot
from tower import Tower
from result import MapResult

class TestChimpsBot(Bot):

    def __init__(self):
        super().__init__()
        self._map = map.HardModeBonusMap(map='inOrder', difficulty='chimps')

    def _load_game(self, game_map):
        self._state = 'NAVIGATING'
        try:
            game_map.navigate_to()
        except ValueError as err:
            pdi.press('esc')
            raise 

    # Single game
    def _play_game(self):
        mapStat = MapResult(self._map._name, self._map._difficulty)
        try:
            self._load_game(self._map)
            self._wait_for_map_load()
            self._state = 'IN_GAME'
            # Skip past chimps info screen
            pdi.press('esc')

            configDir = config.BEGINNER_MAP_FILES.format(self._map._name)
           
            quincy = Tower(self, config.HOTKEY_HERO, f'{configDir}/hero.jpg', None, 'quincy')

            logging.info('Starting game')
            self._start_game()

            dart = Tower(self, config.HOTKEY_TOWER_DART, f'{configDir}/dart.jpg',
                          config.TOWER_DART_UPGRADE, 'dart')

            dart.upgrade(2, 2) # Very quick shots
            dart.upgrade(3, 3) # cbow

            wizard = Tower(self, config.HOTKEY_TOWER_WIZARD, f'{configDir}/wizard.jpg',
                                 config.TOWER_WIZARD_UPGRADE, 'wizard')
            wizard.upgrade(2, 2) # Wall of fire 
            wizard.upgrade(3, 2) # camo
            dart.upgrade(3, 4) # sharp shooter

            druid = Tower(self, config.HOTKEY_TOWER_DRUID, f'{configDir}/druid.jpg',
                                 config.TOWER_DRUID_UPGRADE, 'druid')

            druid.upgrade(1, 2)
            druid.upgrade(2, 3)
            wizard.upgrade(3, 5) # Prince of Darkness
            dart.upgrade(3, 5) # Crossbow Master
            druid.upgrade(2, 5)

            sniper = Tower(self, config.HOTKEY_TOWER_SNIPER, f'{configDir}/sniper.jpg',
                                 config.TOWER_SNIPER_UPGRADE, 'sniper', target='strong')
            sniper.upgrade(3, 2)
            sniper.upgrade(1, 5)

            self._wait_for_game_completion()
            self._game_completed()
            mapStat.result = 'WON'

        except Exception as err:
            mapStat.result = 'FAILED'
            mapStat.cause = err 
            logging.info(f'Failed map: {self._map._name} due to {err}')
            logging.info('Exiting to home screen')
            self._navigate_home()

        finally:
            return mapStat
    def main(self):
        # Init game window and such
        super().main()
        self._game_counter = 0
        total_time = 0
        maps_attempted = 0
        maps_completed = 0
        maps_failed = 0

        completed=[]
        failed=[]

        while True:
            self._state = 'NEW_GAME'
            self._game_counter += 1
            logging.info('---------------')
            logging.info('Starting game {} on {}'.format(self._game_counter, self._map._name))
            initial_time = time.time()
            try:
                self._monkeys_collection_path = None
                gameResult = self._play_game()
            except pag.FailSafeException:
                logging.warning('FailSafe detected, stopping game {}.'.format(self._game_counter))
                exit(1)

            game_time = time.time() - initial_time
            gameResult.time = game_time
            total_time += game_time
            logging.info(
                'Game {} has been completed in {} minutes {} seconds'.format(self._game_counter,
                                                                             int(game_time // 60),
                                                                             int(game_time % 60)))
            logging.info('Total game time in games: {} minutes {} seconds'.format(int(total_time // 60), int(total_time % 60)))
            
            logging.info('Monkeys collected: {}'.format(
                self._monkeys_collection_path) if self._monkeys_collection_path else 'No monkeys collected.')
            logging.info(f'Total monkeys collected: {self._num_collected_monkeys}')
            maps_attempted += 1
            if gameResult.result == 'WON':
                maps_completed += 1
                completed.append(gameResult)
            else:
                maps_failed += 1
                failed.append(gameResult)
            if not self._map.nextMap():
                break

        logging.info('Completed all beginner maps.')
        logging.info('~~~~~~~~~~RESULTS~~~~~~~~~~')
        logging.info(f'Maps Attempted: {maps_attempted}')
        logging.info(f'Maps Beaten: {maps_completed}')
        logging.info(f'Maps Failed {maps_failed}')
        logging.info(f'Total time in game: {total_time}')
        logging.info(f'Average time per game: {total_time/maps_attempted}')
        logging.info(f'Monkeys Collected: {self._num_collected_monkeys}')
        logging.info('------------Map Details----------')
        logging.info('Victories:')
        for mapStats in completed:
            logging.info(f'{mapStats.reportResults()}')

        logging.info('Failures:')
        for mapStats in failed:
            logging.info(f'{mapStats.reportResults()}')


if __name__ == '__main__':
    bot = TestChimpsBot()
    bot.main()
