from django import forms

from blog.application.forms.user_form_service import UpdateUserForm
from blog.domain.entities.profile import Profile


class FormUpdater:
    @classmethod
    def generateForms(cls, request, user_name):
        if request.method == 'POST' and request.user.username == user_name:
            user_form = UpdateUserForm(request.POST, instance=request.user)
            profile_form = UpdateProfileInfoForm(request.POST, request.FILES, instance=request.user.profile)
            profile_picture_form = UpdateProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)

            if user_form.is_valid():
                user_form.save()

            if profile_form.is_valid():
                profile_form.save()

            if profile_picture_form.is_valid() and not profile_picture_form.fields['picture']:
                profile_picture_form.save(True)

        elif request.user.username == user_name:
            user_form = UpdateUserForm(instance=request.user)
            profile_form = UpdateProfileInfoForm(instance=request.user.profile)
            profile_picture_form = UpdateProfilePictureForm(instance=request.user.profile)
        else:
            user_form = UpdateUserForm()
            profile_form = UpdateProfileInfoForm()
            profile_picture_form = UpdateProfilePictureForm()

        return user_form, profile_form, profile_picture_form


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
