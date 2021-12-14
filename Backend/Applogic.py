from datetime import date
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
import pandas as pd
from dateutil import parser

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
            self.popupAlert("ERROR", "Git has failed to connect. Check your credentials.")

    def refresh_repo_display(self, repoUrls, form):
        form.tableRepos.setRowCount(0)
        for x in repoUrls:
            form.tableRepos.insertRow(form.tableRepos.rowCount())
            form.tableRepos.setItem(form.tableRepos.rowCount()-1, 0, QTableWidgetItem(x))

    def add_repo(self, repoUrl, settings, form):
        if self.git.checkValidRepo(repoUrl):
            newtrackedrepos = settings.trackedrepos
            newtrackedrepos.append(repoUrl)

            if len(set(newtrackedrepos)) == len(newtrackedrepos):
                #If true, there are no detected duplicates
                settings.trackedrepos = newtrackedrepos
                settings.update_settings()
                self.refresh_repo_display(settings.trackedrepos, form)
            else:
                #Duplicate has been detected, do not commit. Throw error
                self.popupAlert("ERROR", "This repo is already tracked. Please ensure this repo is not already tracked.")

        else:
            self.popupAlert("ERROR", "Repo failed validation. Ensure repo is \"[username]/[reponame]\" as copied from the end of a repo's URL.")

    def remove_repo(self, dbhandler, git, repoIndex, settings, form):
        repo_fullname = str(settings.trackedrepos[repoIndex])

        #Delete item from GUI object
        del settings.trackedrepos[repoIndex]

        #Remove commits and repo from database
        commit_shas = dbhandler.get_commit_sha_by_repo_fullname(repo_fullname)
        [dbhandler.remove_commit_by_commit_sha(sha) for sha in commit_shas]
        dbhandler.remove_branch_by_repo_fullname(repo_fullname)
    

        #Update saved settings and GUI
        settings.update_settings()
        self.refresh_repo_display(settings.trackedrepos, form)

    def popupAlert(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()

    def populateDB(self, dbhandler, git, repos):
        
        repo_list = self.git.get_all_repos(repos)
        
        
        for repo_obj in repo_list:
            branches = git.get_repo_branches(repo_obj)
            

            for branch in branches:
                #Pull comparison of all existing shas
                all_commit_shas = [sha[0] for sha in dbhandler.get_all_commit_shas()]

                #Populate branches table
                dbhandler.insert_branch((repo_obj.name, branch.name, repo_obj.full_name))

                commits = git.get_commits_by_branch(repo_obj, branch)
                print("Original length: " + str(commits.totalCount))
                commits = [commit for commit in commits if commit.sha not in all_commit_shas]
                print("Pruned length: " + str(len(commits)))


                for commit in commits:
                    if hasattr(commit.committer, "login"): 
                        committer = commit.committer.login
                    else: 
                        committer = "None"
                    
                    last_modified = git.get_repo_commit_last_modified(repo_obj, commit)

                    repo_stats = git.get_repo_commit_stats(repo_obj, commit)
                    values = [commit.sha, parser.parse(last_modified).date().isoformat(), repo_stats.additions, repo_stats.deletions, committer, branch.name]
                    dbhandler.insert_commit(values)

#TODO: I just realized that commits have a One:Many relationship with branches. This changes everything.        


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

    def get_graphdata_codedensity(self, dbhandler):
        #Return a constructed dataframe of the following format:
        # Reponame | Date of commit | commits added + subtracted
        data = dbhandler.get_graphdata_codedensity()

        dataframe = pd.DataFrame(data, columns=["Repo Name", "Date", "Lines Modified"])
        
        return dataframe