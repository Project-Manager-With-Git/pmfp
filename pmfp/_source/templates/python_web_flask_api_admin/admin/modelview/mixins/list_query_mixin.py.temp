__all__ = ["ListQueryMixin","ListQueryMongoMixin"]

from flask_security import current_user

class ListQueryMixin:
    def get_query(self):
        if current_user.has_role('superuser'):
            return self.model.select()
        else:
            return self.model.select().where(self.model.account== current_user.account)

class ListQueryMongoMixin:
    def get_query(self):
        if current_user.has_role('superuser'):
            return self.model.objects
        else:
            return self.model.objects(account_id=current_user.account.account_id)
