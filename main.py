from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Backend.appsettings import Config
from Backend.poller import GitAPIPoller
from Backend.appsettings import Config
from Backend.Applogic import Applogic, Graphlogic
from Backend.Sqlitedb import DBHandler

from UI.TokenForm import Ui_TokenForm
from UI.Tray import UI_Tray
from UI.MainForm import Ui_MainWindow

# Init UI Classes and App classes
settings = Config()
app = QApplication([])
app.setQuitOnLastWindowClosed(False)
git = GitAPIPoller()
applogic = Applogic(git)
graphlogic = Graphlogic(git)
dbhandler = DBHandler()

# Token input instantiation
tokenwindow = QDialog()
tokenform = Ui_TokenForm()
tokenform.setupUi(tokenwindow)
tokenform.TokenButton.clicked.connect(lambda: applogic.tokensubmit(tokenform.TokenInput.text(), tokenwindow, tray, mainwindow, graphlogic, settings.get_settings_repos()))
tokenwindow.show()

# Main window instantiation and hookup
mainwindow = QTabWidget()
mainform = Ui_MainWindow()
mainform.setupUi(mainwindow)
applogic.refresh_repo_display(settings.trackedrepos, mainform)
mainform.ButtonAddRepo.clicked.connect(lambda: applogic.add_repo(mainform.TextboxAddRepo.text(), settings, mainform))
mainform.ButtonRemoveRepo.clicked.connect(lambda: applogic.remove_repo(mainform.tableRepos.currentRow(), settings, mainform))
mainform.buttonSyncRepos.clicked.connect(lambda: applogic.populateDB(dbhandler, git, settings.trackedrepos))


# Tray instantiation
tray = UI_Tray(app, mainwindow)

app.exec_()