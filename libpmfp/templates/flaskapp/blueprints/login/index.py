from blueprints.login import login
@login.route('/',methods=["GET","POST"] )
def index():
    return "1"
