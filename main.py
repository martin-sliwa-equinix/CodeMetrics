from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from appsettings import Config
from poller import GitAPIPoller
from appsettings import Config

from UI.TokenForm import Ui_TokenForm
from UI.Tray import UI_Tray
from UI.MainForm import Ui_MainWindow

# Init UI Classes and app
settings = Config()
app = QApplication([])
app.setQuitOnLastWindowClosed(False)
git = GitAPIPoller()

# Applogic functions
def tokensubmit(token, window, git, tray):
    git.connect(token)
    window.hide()

    # Show tray and main window now that token is submitted
    print(git.getSelfUserTeams())
    tray.showtray()
    mainwindow.show()

# Token input instantiation
tokenwindow = QDialog()
tokenform = Ui_TokenForm()
tokenform.setupUi(tokenwindow)
tokenform.TokenButton.clicked.connect(lambda: tokensubmit(tokenform.TokenInput.text(), tokenwindow, git, tray))
tokenwindow.show()

# Main window instantiation
mainwindow = QTabWidget()
mainform = Ui_MainWindow()
mainform.setupUi(mainwindow)

# Tray instantiation
tray = UI_Tray(app, mainwindow)

app.exec_()