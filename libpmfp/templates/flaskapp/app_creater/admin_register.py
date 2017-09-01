__all__ = ["create_admin"]

from flask import Flask,url_for
from flask_admin import Admin
from flask_security import (Security,
                            PeeweeUserDatastore)
from model import *
from admin.modelview import *
from flask_admin import helpers as admin_helpers

def create_admin(app: Flask)->Flask:
    admin = Admin(app,
                  base_template='my_master.html')
    admin.add_view(AccountAdmin(Account))
    admin.add_view(Risk_AccountAdmin(Risk_Account))
    admin.add_view(Sub_AccountAdmin(Sub_Account))
    admin.add_view(CustomerAdmin(Customer))
    admin.add_view(Acct_BalanceAdmin(Acct_Balance))
    admin.add_view(SubscriberAdmin(Subscriber))
    admin.add_view(AlarmView(Alarm))
    admin.add_view(PolicyView(Policy))
    admin.add_view(OfferingView(Offering))

    user_datastore = PeeweeUserDatastore(database_proxys.get("accountdb"),User, Role, UserRole)
    security = Security(app, user_datastore)

    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )

    # try:
    #     User.create_table()
    #     Role.create_table()
    #     UserRole.create_table()
    # except Exception as e:
    #     print(e)
    #     pass
    # user_role = Role(name='user')
    # user_role.save()
    # super_user_role = Role(name='superuser')
    # super_user_role.save()
    #
    #account = Account.get(account_id='dlsc')
    #user_role = Role.get(name='user')
    #print(account)
    #user_datastore.create_user(email='dlsc', password='dlsc',roles=[user_role],account=account)
    return app
