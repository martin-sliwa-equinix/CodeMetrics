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
        #[form.tableRepos.insertRow(x) for x in repoUrls]

    def add_repo(self, repoUrl, settings, git, form):
        if git.checkValidRepo():
            settings.trackedrepos.append(repoUrl)
            settings.update_settings()
            self.refresh_repo_display(settings.trackedrepos, form)
        else:
            self.popupAlert("ERROR", "Repo failed validation check. Ensure repo URL is correct.")

    def remove_repo(self,repoIndex, form):
        print("TODO")

    def popupAlert(self, title, message):
        msg = QMessageBox
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.critical)
        msg.exec_()


    def remove_repo(self, repoUrl):
        print("TODO")