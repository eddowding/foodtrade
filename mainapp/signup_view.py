from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.edit import FormView
from allauth.account.views import (CloseableSignupMixin,
                             RedirectAuthenticatedUserMixin)
from allauth.account.utils import (get_next_redirect_url, complete_signup,
                    get_login_redirect_url, perform_login,
                    passthrough_next_redirect_url)
from classes.Tags import Tags
from mainapp.forms import SignupForm
from allauth.account.views import SignupView

class MySignupView(SignupView):
    form_class = SignupForm

    def form_valid(self, form):
        print ' print bhayo ', self.request.user

        user = form.save(self.request.user)
        return complete_signup(self.request, user,
                               app_settings.EMAIL_VERIFICATION,
                               self.get_success_url())

    def get_context_data(self, **kwargs):
        form = kwargs['form']
        form.fields["email"].initial = self.request.session \
            .get('account_verified_email', None)
        ret = super(SignupView, self).get_context_data(**kwargs)
        login_url = passthrough_next_redirect_url(self.request,
                                                  reverse("account_login"),
                                                  self.redirect_field_name)
        redirect_field_name = self.redirect_field_name
        redirect_field_value = self.request.REQUEST.get(redirect_field_name)
        ret.update({"login_url": login_url,
                    "redirect_field_name": redirect_field_name,
                    "redirect_field_value": redirect_field_value})
        tags = Tags()
        ret['all_tags'] = tags.get_tags()
        return ret

signup = MySignupView.as_view()