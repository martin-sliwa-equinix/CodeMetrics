from github import Github

class GitAPIPoller:
    def __init__(self):
        print("git instantiated")

    def connect(self, token):
        self.token = token
        self.git = Github(self.token)

    def getSelfUserTeams(self):
        response = self.git.get_user().get_teams()
        responselist = []
        for item in response:
          responselist.append(item)
        return responselist

    def checkValidRepo(self):
        return True

    def checkValidUser(self):
        print("TODO")