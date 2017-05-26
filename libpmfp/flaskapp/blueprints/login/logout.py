from blueprints.login import login

@login.route('/logout', methods=["POST"])
def logout():
    return "1"
