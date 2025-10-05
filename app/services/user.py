from app import database

class UserService:
    def get_all_users(self):
        return database.users_db
 
    def get_user_by_id(self, user_id):
        for u in database.users_db:  # u is a dict
            if u["id"] == user_id:  # works now
                return u
        return None
    
    def create_user(self, user_data):
        new_user = user_data.model_dump() 
        new_user["id"] = database.user_id_counter
        database.users_db.append(new_user)
        database.user_id_counter += 1
        return new_user
    
    def update_user(self, user_id: int, update_data):
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        for key, value in update_data.model_dump(exclude_unset=True).items():
            user[key] = value
        return user
    
    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if not user:
                return False
        database.users_db.remove(user)  # Modifies the actual list
        return True
    
    def update_user_status(self, user_id: int, is_active: bool):
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        if user["is_active"] == is_active:
            return "already_set"
        user["is_active"] = is_active
        return user

    




