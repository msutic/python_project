from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLabel, QAction, qApp, QPushButton, QDialog, QHBoxLayout, \
    QVBoxLayout


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setFixedSize(970, 600)
        self.setWindowTitle('Space Invaders')
        self.setWindowIcon(QIcon('images/icon.png'))

        self.label0 = QLabel(self)
        self.pixmap = QPixmap('images/background.jpg')
        self.label0.setPixmap(self.pixmap)
        self.label0.resize(970, 600)

        header = QLabel('SPACE INVADERS', self)
        header.setFont(QFont('Arial', 40))
        header.resize(700, 55)
        header.move(250, 10)
        header.setStyleSheet("background-color: white")
        header.setStyleSheet("color: white")

        start_game_label = QLabel('press [space] to start', self)
        start_game_label.setFont(QFont('Arial', 15))
        start_game_label.setStyleSheet('color: gray')
        start_game_label.resize(500, 25)
        start_game_label.move(40, 180)

        quit_label = QLabel('press [q] to quit', self)
        quit_label.setFont(QFont('Arial', 15))
        quit_label.setStyleSheet("color: gray")
        quit_label.resize(500, 25)
        quit_label.move(40, 215)

        self.shortcuts()
        self.buttons()
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def shortcuts(self):
        exit_act = QAction(self)
        exit_act.setShortcut('Q')
        exit_act.triggered.connect(qApp.quit)
        self.addAction(exit_act)

        start_act = QAction(self)
        start_act.setShortcut(' ')
        start_act.triggered.connect(self.start_game_dialog)
        self.addAction(start_act)

    def buttons(self):
        start_button = QPushButton("START")
        start_button.setStyleSheet('background-color: blue')
        quit_button = QPushButton("QUIT")
        quit_button.setStyleSheet('background-color: red')

        start_button.clicked.connect(self.start_game_dialog)
        quit_button.clicked.connect(qApp.quit)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(start_button)
        hbox.addWidget(quit_button)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def start_game_dialog(self):
        self.close()
        self.dialog = QDialog()
        self.dialog.setModal(True)
        self.dialog.setStyleSheet('background-color: black')
        self.dialog.setFixedSize(970, 600)
        self.dialog.setWindowIcon(QIcon('images/icon.png'))
        self.dialog.setWindowTitle('Space Invaders [play mode]')

        self.dialog.btn_start = QPushButton('EXIT')
        self.dialog.btn_start.setStyleSheet('background-color: white')
        self.dialog.btn_start.setFont(QFont('Arial', 20))
        self.dialog.btn_start.setStyleSheet('background-color: transparent')
        self.dialog.btn_start.setStyleSheet('color: gray')
        self.dialog.btn_start.clicked.connect(self.close_start_game)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.dialog.btn_start)
        self.dialog.setLayout(hbox1)

        self.dialog.exec()

    def close_start_game(self):
        self.dialog.close()
        self.show()
