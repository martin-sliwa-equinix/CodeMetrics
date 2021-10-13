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

    def checkValidRepo(self, URL):
        try:
            self.git.get_repo(URL)
            return True
        except:
            print("Error finding repo")
            return False



    def checkValidUser(self):
        print("TODO")