from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import qtawesome as qta

from appsettings import Config
from poller import GitAPIPoller
from appsettings import Config

from UI.TokenForm import Ui_TokenForm

#Init UI Classes and app
settings = Config()
app = QApplication([])
app.setQuitOnLastWindowClosed(False)

# Applogic functions

def tokensubmit(token, window):
    print(token)
    window.hide()

# Launch the tray once token has been confirmed
def trayLaunch():
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

# Launch token form to input token
tokenwindow = QDialog()
tokenform = Ui_TokenForm()
tokenform.setupUi(tokenwindow)
tokenform.TokenButton.clicked.connect(lambda x: tokensubmit(tokenform.TokenInput.text(), tokenwindow))
tokenwindow.show()



# Init git class with token)
git = GitAPIPoller("") #Do not save the token - have import on launch

print(git.getSelfUserTeams())

app.exec_()