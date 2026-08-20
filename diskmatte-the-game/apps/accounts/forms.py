from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class RegisterForm(UserCreationForm):
    """UserCreationForm with Bootstrap styling and Swedish labels/help text."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].label = "Användarnamn"
        self.fields["username"].help_text = (
            "150 tecken eller färre. Endast bokstäver, siffror och @/./+/-/_."
        )
        self.fields["password1"].label = "Lösenord"
        self.fields["password1"].help_text = (
            "Lösenordet får inte vara för likt din övriga information, "
            "måste vara minst 8 tecken, får inte vara ett vanligt lösenord "
            "och får inte bara bestå av siffror."
        )
        self.fields["password2"].label = "Bekräfta lösenord"
        self.fields["password2"].help_text = "Ange samma lösenord igen för verifiering."

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class LoginForm(AuthenticationForm):
    """AuthenticationForm with Bootstrap styling and Swedish labels."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].label = "Användarnamn"
        self.fields["password"].label = "Lösenord"

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
