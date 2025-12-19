from allauth.account.forms import LoginForm as _LoginForm, SignupForm as _SignupForm

from core.forms import DaisyFormMixin


class LoginForm(DaisyFormMixin, _LoginForm):
    pass


class SignupForm(DaisyFormMixin, _SignupForm):
    pass
