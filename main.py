from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import qtawesome as qta

from appsettings import Config
from poller import GitAPIPoller
from appsettings import Config

#Init Classes and app
git = GitAPIPoller("") #Do not save the token - have import on launch
app = QApplication([])
app.setQuitOnLastWindowClosed(False)



#app function definitions - port to class later

#Tray menu design
traymenu = QMenu()

exit = QAction("Exit")
exit.triggered.connect(app.quit)
traymenu.addAction(exit)

#Init Tray
trayicon = qta.icon('fa5s.eye-dropper', color = 'white')
tray = QSystemTrayIcon()
tray.setIcon(trayicon)
tray.setVisible(True)
tray.setContextMenu(traymenu)

print(git.getSelfUserTeams())

app.exec_()