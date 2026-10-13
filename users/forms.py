from allauth.account.forms import (
    LoginForm as _LoginForm,
)
from allauth.account.forms import (
    ResetPasswordForm as _ResetPasswordForm,
)
from allauth.account.forms import (
    SignupForm as _SignupForm,
)

from core.forms import DaisyFormMixin


class LoginForm(DaisyFormMixin, _LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].help_text = self.fields["password"].help_text.replace(
            "<a", '<a class="hover:link"'
        )


class SignupForm(DaisyFormMixin, _SignupForm):
    pass


class ResetPasswordForm(DaisyFormMixin, _ResetPasswordForm):
    pass
