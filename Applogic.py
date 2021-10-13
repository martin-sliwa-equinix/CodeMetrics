class Applogic:
    def tokensubmit(self, token, window, git, tray, mainwindow):
        git.connect(token)
        window.hide()

        # Show tray and main window now that token is submitted
        print(git.getSelfUserTeams())
        tray.showtray()
        mainwindow.show()  

    def refresh_repo_display(self, repoUrls, form):
        form.tableRepos.clearContents()
        [form.tableRepos.insertRow(x) for x in repoUrls]

    def add_repo(self, repoUrl):
        print("TODO")
        self.refresh_repo_display()

    def remove_repo(self, repoUrl):
        print("TODO")