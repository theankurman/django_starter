from allauth.account.forms import (
    LoginForm as _LoginForm,
    SignupForm as _SignupForm,
    ResetPasswordForm as _ResetPasswordForm,
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
