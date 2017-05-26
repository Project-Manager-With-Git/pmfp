
from blueprints.login import login
@login.route('/add_account',methods=["POST"] )
def add_account():
    return "1"
