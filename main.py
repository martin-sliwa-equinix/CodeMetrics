from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from appsettings import Config
from poller import GitAPIPoller
from appsettings import Config

from UI.TokenForm import Ui_TokenForm
from UI.Tray import UI_Tray

# Init UI Classes and app
settings = Config()
app = QApplication([])
app.setQuitOnLastWindowClosed(False)
git = GitAPIPoller()

# Applogic functions
def tokensubmit(token, window, git, tray):
    git.connect(token)
    window.hide()

    # Show tray now that token is submitted
    print(git.getSelfUserTeams())
    tray.showtray()

# GUI instantiation
tray = UI_Tray(app)

# Launch token form to input token
tokenwindow = QDialog()
tokenform = Ui_TokenForm()
tokenform.setupUi(tokenwindow)
tokenform.TokenButton.clicked.connect(lambda x: tokensubmit(tokenform.TokenInput.text(), tokenwindow, git, tray))
tokenwindow.show()


app.exec_()