from github import Github

class GitAPIPoller:
    def __init__(self, access_token):
        self.token = access_token
        self.git = Github(self.token)

    def getSelfUserTeams(self):
        response = self.git.get_user().get_teams()
        responselist = []
        for item in response:
          responselist.append(item)
        return responselist