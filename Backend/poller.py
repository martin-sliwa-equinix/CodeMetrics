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

    def get_repo(self, URL):
        #Return a single repo object when requested by URL
        return self.git.get_repo(URL)

    def get_all_repos(self, URLs):
        #Return a list of all repo objects requested by list of URLs
        repo_objects = []
        for URL in URLs:
            repo_objects.append(self.git.get_repo(URL))
        return repo_objects

    def get_repo_branches(self, repo):
        #This will return branch objects for the provided repo object
        return repo.get_branches()

    def get_commits_by_branch(self, repo, branch):
        #This function will return all of the commits objects associated with a given branch object
        return repo.get_commits(branch.commit.sha)

    def get_repo_commits_by_branch(self, repo):
        #This function will return all of the commit objects on all branches for a supplied repo
        branch_commits = []
        branches = repo.get_branches()
        [branch_commits.append(repo.get_commits(branch.commit.sha)) for branch in branches]
        
        #returns commits[branch n][commit n]
        return branch_commits

    def get_repo_commits_all_branches(self, repo):
        #This function will return all of the commit objects on a repo, collapsing branches
        branch_commits = []
        branches = repo.get_branches()
        [branch_commits.append(repo.get_commits(branch.commit.sha)) for branch in branches]

        commits = []
        for branch_commit in branch_commits:
            #This will return an object with all the commits for this branch. Must further loop to get each commit.
            for commit in branch_commit:
                commits.append(commit)
            
        #returns commits[commit n]
        return commits

    def get_repo_commit_stats(self, repo, commit):
        #This function will return the additions and deletions of a given commit in a repo
        stats = repo.get_commit(commit.sha).stats

        return stats

