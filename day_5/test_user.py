from user import UserService

# The Fake Repository
class FakeUserRepository:
    def __init__(self):
        self.users = {} 
        
    def save(self, user):
        self.users[user['id']] = user
        
    def find(self, user_id):
        return self.users.get(user_id)
        
    def list_users(self):
        return list(self.users.values())


def test_user_service_saves_and_finds_users():
    repo = FakeUserRepository()
    service = UserService(repo)
    
    service.register_user(1, "John Doe")
    service.register_user(2, "Jane Doe")

    assert service.get_user(1) == {"id": 1, "name": "John Doe"}
    assert service.get_user(2) == {"id": 2, "name": "Jane Doe"}
    assert service.list_users() == [{"id": 1, "name": "John Doe"}, {"id": 2, "name": "Jane Doe"}]