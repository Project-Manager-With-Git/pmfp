from ..model.user import User
from .init import views, jinja


@views.get("/")
@jinja.template('index.html')
async def helloword(request):
    await User.create(name="xjk", age=12)
    await User.create(name="zyf", age=8)
    request['flash']('success message', 'success')
    request['flash']('info message', 'info')
    request['flash']('warning message', 'warning')
    request['flash']('error message', 'error')
    users = await User.select()
    usernames = ",".join([user.name for user in users])
    request['session']['user'] = usernames
    return {'greetings': 'Hello, sanic {}!'.format(",".join(usernames))}
