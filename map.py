import logging
import math
import config
from bot import Bot


class Map:

    def __init__(self, name):
        if name == 'bonusMap':
            self._name = None
        elif name == 'inOrder':
            self._mapNum = 1
            self._name = config.BEGINNER_MAPS[0][0][0]
        else:
            self._mapNum = 0
            self._name = name

    def _log_navigation(self):
        logging.info('Navigating to map {}'.format(self._name))


class HardModeBonusMap(Map):

    def __init__(self, map='bonusMap', difficulty='standard'):
        self._difficulty=difficulty
        super().__init__(map)

    def findNextMap(self):
        logging.info('Finding next bonus map')
        Bot.click_on(config.BUTTON_MENU_PLAY)
        bonusMap = None
        mapPage = 1
        while bonusMap is None:
            try:
                bonusMap = Bot.click_on(config.BUTTON_MENU_BONUS_MAP)
            except ValueError:
                logging.debug('Bonus map not found, checking next page')
                Bot.click_on(config.BUTTON_MENU_MAPS_BEGINNER)
                mapPage += 1
        Bot.click_on(config.BUTTON_MENU_HARD_DIFF)
        if self._difficulty == 'standard':
            Bot.click_on(config.BUTTON_MENU_STANDARD_MODE)
        elif self._difficulty == 'impoppable':
            Bot.click_on(config.BUTTON_MENU_IMPOPPABLE_MODE)
        elif self._difficulty == 'chimps':
            Bot.click_on(config.BUTTON_MENU_CHIMPS_MODE)


        # Reconcile click to a map
        logging.debug('Found bonus map at {}'.format(bonusMap))
        mapName = self.getMapNameFromCoords(bonusMap, mapPage)
        self._name = mapName
        return mapName

    def getMapNameFromCoords(self, mapCoords, mapPage):
        mapCol = math.floor((mapCoords.x - config.MAP_GRID_OFFSET_X) / (config.MAP_TILE_SIZE_X+config.MAP_TILE_SPACING_X))
        mapRow = math.ceil((mapCoords.y - config.MAP_GRID_OFFSET_Y) / (config.MAP_TILE_SIZE_Y+config.MAP_TILE_SPACING_Y))

        logging.info(f'Bonus map on page {mapPage}, at pos {mapCol}, {mapRow}')

        mapList = config.BEGINNER_MAPS[mapPage-1]

        mapName = mapList[mapRow-1][mapCol-1]
        return mapName

    def nextMap(self): 
        if self._mapNum < 19:
            self._mapNum += 1
            mapPage = math.ceil(self._mapNum / 6)
            pageRow = math.ceil((self._mapNum % 6) / 3)
            pageCol = (self._mapNum % 6) % 3
            self._name = config.BEGINNER_MAPS[mapPage-1][pageRow-1][pageCol-1]
            logging.info(f'Next map is {self._name} on page {mapPage} at {pageCol}, {pageRow}')
            return True
        else:
            logging.info('All maps attempted')
            return False

    def navigate_to(self):
        self._log_navigation()
        configDir = config.BEGINNER_MAP_FILES.format(self._name)
        Bot.click_on(config.BUTTON_MENU_PLAY)
        mapPage = math.ceil(self._mapNum / 6)
        if mapPage > 1:
            Bot.click_on(config.BUTTON_MENU_MAPS_BEGINNER, numClicks=mapPage-1)
        Bot.click_on(f'{configDir}/map.jpg')
        Bot.click_on(config.BUTTON_MENU_HARD_DIFF)
        if self._difficulty == 'standard':
            Bot.click_on(config.BUTTON_MENU_STANDARD_MODE)
        elif self._difficulty == 'impoppable':
            Bot.click_on(config.BUTTON_MENU_IMPOPPABLE_MODE)
        elif self._difficulty == 'chimps':
            Bot.click_on(config.BUTTON_MENU_CHIMPS_MODE)

class DarkCastleMap(Map):

    def __init__(self):
        super().__init__('Dark Castle')

    def navigate_to(self):
        self._log_navigation()
        Bot.click_on(config.BUTTON_MENU_PLAY)
        Bot.click_on(config.BUTTON_MENU_MAPS_EXPERT)
        Bot.click_on(config.BUTTON_MENU_MAPS_EXPERT) # Temporary fix, should parameterize map finding
        Bot.click_on(config.MAPS_DARK_CASTLE)
        Bot.click_on(config.BUTTON_MENU_EASY_DIFF)
        Bot.click_on(config.BUTTON_MENU_STANDARD_MODE)
