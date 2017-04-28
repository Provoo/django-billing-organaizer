import account.views
from .models import UserProfile


class SignupView(account.views.SignupView):
    def update_profile(self, form):
        # pass
        UserProfile.objects.create(
            user=self.create_user,
        )
        # profile = self.created_user.profile  # replace with your reverse one-to-one profile attribute
        # profile.some_attr = "some value"
        # profile.save()

    def after_signup(self, form):
        self.update_profile(form)
        super(SignupView, self).after_signup(form)
