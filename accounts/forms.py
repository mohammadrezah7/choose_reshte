
from django import forms
from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,
)
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator


class RegisterForm(forms.Form):

    username = forms.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(
                5,
                "نام کاربری باید حداقل ۵ کاراکتر باشد."
            )
        ]
    )

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    def clean_password(self):
        password = self.cleaned_data.get("password")
        username = self.cleaned_data.get("username")

        if not password:
            raise forms.ValidationError(
                "وارد کردن رمز عبور الزامی است."
            )

        
        if len(password) < 8:
            raise forms.ValidationError(
                "رمز عبور باید حداقل ۸ کاراکتر باشد."
            )

        
        if password.isdigit():
            raise forms.ValidationError(
                "رمز عبور نمی‌تواند فقط شامل عدد باشد."
            )

       
        common_passwords = {
            "123456",
            "12345678",
            "123456789",
            "1234567890",
            "password",
            "password123",
            "qwerty",
            "qwerty123",
            "admin",
            "admin123",
            "11111111",
            "00000000",
            "123123123",
            "abcdefgh",
            "abcdefghi",
        }

        if password.lower() in common_passwords:
            raise forms.ValidationError(
                "این رمز عبور بسیار ساده و قابل حدس است. "
                "لطفاً رمز قوی‌تری انتخاب کنید."
            )

        # مشابه بودن با نام کاربری
        if username:
            username_lower = username.lower()
            password_lower = password.lower()

            if (
                password_lower == username_lower
                or username_lower in password_lower
            ):
                raise forms.ValidationError(
                    "رمز عبور نباید با نام کاربری یکسان یا بیش از حد مشابه باشد."
                )

        return password

