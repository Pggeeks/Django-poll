from django import forms
from django.contrib.auth.models import User
from .models import Question_Model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate


class Poll_Form(forms.ModelForm):
    choice1 = forms.CharField(
        label="Option 1",
        max_length=100,
        min_length=1,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    choice2 = forms.CharField(
        label="Option 2",
        max_length=100,
        min_length=1,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    choice3 = forms.CharField(
        label="Option 3",
        max_length=100,
        min_length=1,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    choice4 = forms.CharField(
        label="Option 4",
        max_length=100,
        min_length=1,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Question_Model
        fields = ["question", "choice1", "choice2", "choice3", "choice4"]
        widgets = {
            "question": forms.Textarea(
                attrs={"class": "form-control", "rows": 5, "cols": 20}
            ),
        }

    def __init__(self, *args, **kwargs):
        """
        Call to ModelForm constructor
        and add width and height attribute
        """
        super(Poll_Form, self).__init__(*args, **kwargs)
        self.fields["choice1"].widget.attrs["style"] = "width:200px; height:40px;"
        self.fields["choice2"].widget.attrs["style"] = "width:200px; height:40px;"
        self.fields["choice3"].widget.attrs["style"] = "width:200px; height:40px;"
        self.fields["choice4"].widget.attrs["style"] = "width:200px; height:40px;"


class loginform(AuthenticationForm):
    username = forms.EmailField(
        required=True,
        label="email",
        widget=forms.EmailInput(attrs={"placeholder": "E-mail"}),
    )
    password = forms.CharField(
        max_length=20, widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def clean(self):
        email = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        user = None
        try:
            user = User.objects.get(email=email)
            raise forms.ValidationError("error message 1")
        except Exception as e:
            try:
                user_login = authenticate(username=user.username, password=password)
            except Exception:
                user_login = None
            if user_login is not None:
                return user_login
            else:
                raise forms.ValidationError("error message 1") from e


class Register(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "First Name"})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Last Name"})
    )
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "E-mail"}))
    username = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "Username"})
    )
    password1 = forms.CharField(
        max_length=20, widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password2 = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(attrs={"placeholder": "Re-type Password"}),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):
        usr_email = self.cleaned_data["email"]
        usr = None
        try:
            usr = User.objects.get(email=usr_email)
        except Exception:
            return usr_email
        if usr is not None:
            raise forms.ValidationError("email alredy exsist")
