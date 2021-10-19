from github import Github

class GitAPIPoller:
    def __init__(self):
        print("git instantiated")

    def connect(self, token):
        self.token = token
        self.git = Github(self.token)
        self.user = self.git.get_user()
        self.user.login

    def getSelfUserTeams(self):
        #Displays the 
        response = self.git.get_user().get_teams()
        responselist = []
        for item in response:
          responselist.append(item)
        return responselist

    def checkValidRepo(self, URL):
        try:
            self.git.get_repo(URL)
            return True
        except:
            print("Error finding repo")
            return False

    def checkValidUser(self):
        print("TODO")
        return True 

    def get_all_repo_commits(self, repo):
        #This function will return all of the commits on all branches for supplied repos
        commits = []
        branches = repo.get_branches()
        [commits.append(repo.get_commits(branch.commit.sha)) for branch in branches]

        return commits

    def get_repo_commit_stats(self, repo, commit):
        #This function will return the additions and deletions of a given commit in a repo
        additions, deletions = 0,0
        repo.get_commit(commit).stats

        return additions,deletions

