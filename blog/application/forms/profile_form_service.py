from django import forms

from blog.domain.entities.profile import Profile


class UpdateProfileInfoForm(forms.ModelForm):
    bio = forms.CharField(required=False, widget=forms.Textarea(
        attrs={
            'class': 'form-control border-0 h-100',
            'rows': 20,
            'onkeydown': 'activateConfirmButton();',
            'maxlength': Profile._meta.get_field('bio').max_length,
            'placeholder': 'Tell us about yourself...',
        }))
    location = forms.CharField(required=False, widget=forms.Textarea(
        attrs={
            'class': 'form-control border-0 h-100',
            'rows': 20,
            'onkeydown': 'activateConfirmButton();',
            'maxlength': Profile._meta.get_field('location').max_length,
            'placeholder': 'Where are you from?',
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
