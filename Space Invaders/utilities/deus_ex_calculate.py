from multiprocessing import Process, Queue
from random import randint
from time import sleep

from config import cfg


class CalculateDeusExX(Process):

    def __init__(self, q: Queue):
        super().__init__(target=self._calculate_, args=[q])

    def _calculate_(self, q: Queue):
        while 1:
            x_coord = randint(0, cfg.PLAY_WINDOW_WIDTH - 50)
            q.put(x_coord)
            print("putting on queue: x=", x_coord)
            sleep(1)