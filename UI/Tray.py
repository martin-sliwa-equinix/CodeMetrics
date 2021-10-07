from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import qtawesome as qta


class UI_Tray():
    def __init__(self, app):
        #Tray menu design
        self.traymenu = QMenu()

        #Tray action connect
        self.exit = QAction("Exit")
        self.exit.triggered.connect(app.quit)
        self.traymenu.addAction(self.exit)

        #Init Tray
        self.trayicon = qta.icon('fa5s.eye-dropper', color = 'white')
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.trayicon)

    def showtray(self):
        self.tray.setVisible(True)
        self.tray.setContextMenu(self.traymenu)