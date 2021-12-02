from datetime import date
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
import pandas as pd

class Applogic:
    def __init__(self, git):
        self.git = git

    def tokensubmit(self, token, window, tray, mainwindow, graphlogic, repos):
        try:
            self.git.connect(token)

            window.hide()

            # Show tray and main window now that token is submitted
            #graphlogic.set_initial_data(repos)
            tray.showtray()
            mainwindow.show()  
        except:
            #TODO: This doesnt seem to be working?
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

    def populateDB(self, dbhandler, git, repos):
        
        repo_list = self.git.get_all_repos(repos)
        
        for repo_obj in repo_list:
            #TODO: Check if this repo already exists in db in case of dupe repos
            #TODO: Also find method to see if repo data is newer than what we have
            branches = git.get_repo_branches(repo_obj)

            for branch in branches:
                #Populate branches table
                dbhandler.insert_branch((repo_obj.name, branch.name))

                commits = git.get_commits_by_branch(repo_obj, branch)

                for commit in commits:
                    #TODO: Check if commitsha already exists in db before doing this
                    if hasattr(commit.committer, "login"): 
                        committer = commit.committer.login
                    else: 
                        committer = "None"
                    
                    repo_stats = git.get_repo_commit_stats(repo_obj, commit)
                    values = [commit.sha, commit.last_modified, repo_stats.additions, repo_stats.deletions, committer, branch.name]
                    dbhandler.insert_commit(values)

            


#Contains all dataframe and graph related calculations
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

    #TODO: Probably rewrite this entire thing using DB data now
    def get_graphdata_codedensity(self, repos, dbhandler):
        #Return a constructed dataframe of the following format:
        # Reponame | Date of commit | commits added + subtracted
        data = dbhandler.get_graphdata_codedensity()
        
        return pd.DataFrame(data)

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