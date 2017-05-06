import account.views
from .models import UserProfile
from .form import SignupForm


class SignupView(account.views.SignupView):
    form_class = SignupForm

    def update_profile(self, form):

        UserProfile.objects.create(
            user=self.create_user,
            first_name=form.cleaned_data("first_name"),
            last_name=form.cleaned_data("last_name"),
            birthdate=form.cleaned_data("birthdate")
        )

    def after_signup(self, form):
        self.update_profile(form)
        super(SignupView, self).after_signup(form)

    # profile = self.created_user.profile  # replace with your reverse one-to-one profile attribute
    # profile.some_attr = "some value"
    # profile.save()
