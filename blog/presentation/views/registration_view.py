from django.contrib import messages
from django.shortcuts import redirect, render

from blog.application.forms.user_form_service import CreateUserForm


class RegistrationView:

    @classmethod
    def register_page(cls, request):
        if request.user.is_authenticated:
            return redirect('home')

        form_data = request.POST if request.method == 'POST' else None
        user = cls.register_user(form_data)

        if user:
            messages.success(request, 'Success!')
            return redirect('login')

        context = {
            'form': CreateUserForm(),
        }
        return render(request, 'registration/register.html', context)

    @classmethod
    def register_user(cls, form_data):
        form = CreateUserForm(form_data)
        if form.is_valid():
            user = form.save()
            return user
        return None
