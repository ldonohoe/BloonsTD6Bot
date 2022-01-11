import logging
import map
import config
import pydirectinput as pdi
from bot import Bot
from tower import Tower




class ImpoppableBot(Bot):

    def __init__(self):
        super().__init__()
        self._map = map.HardModeBonusMap('impoppable')

    def _load_game(self):
        try:
            newMap = self._map.findNextMap()
            logging.info(f'Found next bonus map: {self._map._name}')
        except ValueError as err:
            pdi.press('esc')
            raise

    # Single game
    def _play_game(self):
        self._load_game()
        self._wait_for_map_load()
        # Skip past impoppable info screen
        pdi.press('esc')

        configDir = config.BEGINNER_MAP_FILES.format(self._map._name)

        dart = Tower(self, config.HOTKEY_TOWER_DART, f'{configDir}/dart.jpg',
                      config.TOWER_DART_UPGRADE, 'dart')

        dart.upgrade(2, 3)

        logging.info('Starting game')
        self._start_game()

        hero = Tower(self, config.HOTKEY_HERO, f'{configDir}/hero.jpg', None, 'hero')

        wizard = Tower(self, config.HOTKEY_TOWER_WIZARD, f'{configDir}/wizard.jpg',
                             config.TOWER_WIZARD_UPGRADE, 'wizard')
        wizard.upgrade(2, 2)
        wizard.upgrade(3, 5)
        dart.upgrade(3, 5)


        self._wait_for_game_completion()
        self._game_completed()


if __name__ == '__main__':
    bot = ImpoppableBot()
    bot.main()
