class UserService:
    def __init__(self, repository):
        self.repo = repository
        
    def register_user(self, user_id, name):
        user = {"id": user_id, "name": name}
        self.repo.save(user)
        
    def get_user(self, user_id):
        return self.repo.find(user_id)

    def list_users(self):
        return self.repo.list_users()
