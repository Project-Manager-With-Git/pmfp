__all__ = ["AccessibleMixin"]

from flask_security import current_user
from flask import url_for, request, abort, redirect


class AccessibleMixin:

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        else:
            return True

        # if current_user.has_role('superuser'):
        #     return True

        # return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))
