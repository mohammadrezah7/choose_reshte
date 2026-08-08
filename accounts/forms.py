from django import forms
from django.core.validators import MinLengthValidator

class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=200, 
        validators=[MinLengthValidator(5)]
    )
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(
                    "رمز عبور و تکرار رمز عبور یکسان نیستند."
                )

        return cleaned_data