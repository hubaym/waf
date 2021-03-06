from django import forms
from django.contrib.auth import get_user_model
from custom_user.userbackend import CustomUserAuth
from classes.neo_classes.usertoneo import UserToNeo

class CustomUserForm(forms.ModelForm):
    """
    Form for registering a new account.
    """
    email = forms.EmailField(widget=forms.TextInput,label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label="Password (again)")

    class Meta:
        model = get_user_model()
        fields = ['email', 'password1', 'password2']

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        self.cleaned_data = super(CustomUserForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(CustomUserForm, self).save(commit=False)
        setattr(user,'username', getattr(user,'email'))
        setattr(user,'email_subs', getattr(user,'email'))
        user.set_password(self.cleaned_data['password1'])
        print(getattr(user,'email'))
        usertoneo = UserToNeo()
        if commit:
            user.save()
            usertoneo.createUserToNeoByEmail(getattr(user,'email'))
        return user