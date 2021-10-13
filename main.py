from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from appsettings import Config
from poller import GitAPIPoller
from appsettings import Config
from Applogic import Applogic

from UI.TokenForm import Ui_TokenForm
from UI.Tray import UI_Tray
from UI.MainForm import Ui_MainWindow

# Init UI Classes and app
settings = Config()
app = QApplication([])
app.setQuitOnLastWindowClosed(False)
git = GitAPIPoller()
applogic = Applogic()

# Token input instantiation
tokenwindow = QDialog()
tokenform = Ui_TokenForm()
tokenform.setupUi(tokenwindow)
tokenform.TokenButton.clicked.connect(lambda: applogic.tokensubmit(tokenform.TokenInput.text(), tokenwindow, git, tray, mainwindow))
tokenwindow.show()

# Main window instantiation and hookup
mainwindow = QTabWidget()
mainform = Ui_MainWindow()
mainform.setupUi(mainwindow)
applogic.refresh_repo_display(settings.trackedrepos, mainform)
mainform.ButtonAddRepo.clicked.connect(lambda: applogic.add_repo(mainform.TextboxAddRepo.text(), settings, git, mainform))


# Tray instantiation
tray = UI_Tray(app, mainwindow)

app.exec_()