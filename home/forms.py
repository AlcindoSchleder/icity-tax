"""
Create captcha field on all home forms
"""
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible


class HomeCaptchaForm(forms.Form):
    captcha = ReCaptchaField(label='Eu sou um humano:')
