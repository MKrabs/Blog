from django.contrib import messages
from django.shortcuts import redirect, render

from blog.application.user_form_service import CreateUserForm


class RegistrationView:

    def register_page(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        form_data = request.POST if request.method == 'POST' else None
        user = self.register_user(form_data)

        if user:
            messages.success(request, 'Success!')
            return redirect('login')

        context = {
            'form': CreateUserForm(),
        }
        return render(request, 'registration/register.html', context)

    def register_user(self, form_data):
        form = CreateUserForm(form_data)
        if form.is_valid():
            user = form.save()
            return user
        return None
