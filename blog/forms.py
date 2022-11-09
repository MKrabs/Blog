from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms

from blog.models import Profile


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control border-0 bg-transparent'})
    )

    class Meta:
        model = User
        fields = ['username']


class UpdateProfileInfoForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control border-0 h-100',
            'rows': 20,
            'onkeydown': 'activateConfirmButton();',
        }))
    location = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control border-0 h-100',
            'rows': 20,
            'onkeydown': 'activateConfirmButton();',
        }))

    class Meta:
        model = Profile
        fields = ['bio', 'location']


class UpdateProfilePictureForm(forms.ModelForm):
    picture = forms.ImageField(widget=forms.FileInput(
        attrs={
            'class': 'rounded-circle position-absolute bottom-0 end-0 opacity-0 btn',
            'style': 'width: 100%; height: 100%',
            'onchange': 'readURL(this); activateConfirmButton();',
            'accept': '.jpg,.jpeg,.png,.gif'
        }),
        required=False)

    class Meta:
        model = Profile
        fields = ['picture']
