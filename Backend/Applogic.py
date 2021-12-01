from datetime import date
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
import pandas as pd

class Applogic:
    def __init__(self, git):
        self.git = git

    def tokensubmit(self, token, window, tray, mainwindow, graphlogic, repos, dbhandler):
        try:
            self.git.connect(token)

            window.hide()

            # Show tray and main window now that token is submitted
            #graphlogic.set_initial_data(repos)
            tray.showtray()
            mainwindow.show()  
        except:
            self.popupAlert("ERROR: Git has failed to connect. Check your credentials.")



    def refresh_repo_display(self, repoUrls, form):
        form.tableRepos.setRowCount(0)
        for x in repoUrls:
            form.tableRepos.insertRow(form.tableRepos.rowCount())
            form.tableRepos.setItem(form.tableRepos.rowCount()-1, 0, QTableWidgetItem(x))

    def add_repo(self, repoUrl, settings, form):
        if self.git.checkValidRepo(repoUrl):
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

    def update_repo_commit_graph(self):
        print("TODO")

    def popupAlert(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()



class Graphlogic:
    def __init__(self, git):
        self.git = git

        #Init the data frames used in graphs
        self.graphdata_codedensity = pd.DataFrame()

    def get_data(self, type=None):
        if type == None:
            print("No data type specified")
        elif type == "codedensity":
            return self.graphdata_codedensity

    def set_initial_data(self, repos):
        #Pull down all data for initial load up
        print("repos to check are")
        print(repos)
        self.graphdata_codedensity = self.get_graphdata_codedensity(repos)
        print(self.graphdata_codedensity)

    def get_graphdata_codedensity(self, repos):
        #Return a constructed dataframe of the following format:
        # Reponame | Date of commit | commits added + subtracted
        repo_list = self.git.get_all_repos(repos)

        data = []
        for repo_obj in repo_list:
            print(repo_obj.name)
            repoName = repo_obj.name
            commits = self.git.get_repo_commits_all_branches(repo_obj)
            print("commits is")
            print(commits)

            #Construct the data frame:
            for commit in commits:
                print("commit is")
                print(commit)
                commitstats = commit.stats
                commitdate = commitstats.last_modified
                commitchanges = commitstats.additions + commitstats.deletions
                data.append([repoName, commitdate, commitchanges])


        return pd.DataFrame(data)