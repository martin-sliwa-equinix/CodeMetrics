from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

class Applogic:
    def tokensubmit(self, token, window, git, tray, mainwindow):
        git.connect(token)
        window.hide()

        # Show tray and main window now that token is submitted
        print(git.getSelfUserTeams())
        tray.showtray()
        mainwindow.show()  

    def refresh_repo_display(self, repoUrls, form):
        form.tableRepos.setRowCount(0)
        for x in repoUrls:
            form.tableRepos.insertRow(form.tableRepos.rowCount())
            form.tableRepos.setItem(form.tableRepos.rowCount()-1, 0, QTableWidgetItem(x))

    def add_repo(self, repoUrl, settings, git, form):
        if git.checkValidRepo(repoUrl):
            settings.trackedrepos.append(repoUrl)
            settings.update_settings()
            self.refresh_repo_display(settings.trackedrepos, form)
        else:
            self.popupAlert("ERROR: Repo failed validation", "Ensure repo is \"[username]/[reponame]\" as copied from the end of a repo's URL.")
            self.refresh_repo_display(settings.trackedrepos, form)

    def remove_repo(self,repoIndex, settings, form):
        del settings.trackedrepos[repoIndex]
        settings.update_settings()
        self.refresh_repo_display(settings.trackedrepos, form)

    def popupAlert(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()