from Database import Storage

# Here needs to be added a process that is going to calculate new x,y coordinates of every active
# movable object (bullets, aliens, spaceships)

# Send data to thread via pipe
# from thread, make communication with singleplayer.py where graphics will be updated
# use pyqtSlot and pyqtSignal, along with QThread

class MovementHandler:

    def __init__(self):
        pass
    '''
        def calculate_new_positions(self, storage: Storage):

        for bullet in storage.get_bullets():
            bullet.move_up()

    '''

