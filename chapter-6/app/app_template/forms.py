from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(
        label="Email",
        max_length=255,
        widget=forms.EmailInput(attrs={"id": "login-email", "class": "input"}),
    )
    password = forms.CharField(
        label="Password",
        max_length=255,
        widget=forms.PasswordInput(attrs={"id": "login-password", "class": "input"}),
    )


class SignupForm(forms.Form):
    first_name = forms.CharField(
        label="First Name",
        max_length=255,
        widget=forms.TextInput(attrs={"id": "signup-first-name", "class": "input"}),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=255,
        widget=forms.TextInput(attrs={"id": "signup-last-name", "class": "input"}),
    )
    email = forms.EmailField(
        label="Email",
        max_length=255,
        widget=forms.EmailInput(attrs={"id": "signup-email", "class": "input"}),
    )
    password = forms.CharField(
        label="Password",
        max_length=255,
        widget=forms.PasswordInput(attrs={"id": "signup-password", "class": "input"}),
    )
    password_confirm = forms.CharField(
        label="Confirm Password",
        max_length=255,
        widget=forms.PasswordInput(
            attrs={"id": "signup-password-confirm", "class": "input"}
        ),
    )
