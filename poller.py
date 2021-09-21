from github import Github

class GitAPIPoller:
    def __init__(self, access_token):
        self.token = access_token
        self.git = Github(self.token)

    def getSelfUser(self):
        response = self.git.get_user()
        return response 