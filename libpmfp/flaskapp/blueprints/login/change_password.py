from blueprints.login import login

@login.route('/change_password',methods=["POST"] )
def change_password():
    return "1"
