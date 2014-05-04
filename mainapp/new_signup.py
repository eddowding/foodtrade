from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView

from allauth.account.views import (CloseableSignupMixin,
                             RedirectAuthenticatedUserMixin)
from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.forms import DisconnectForm, SignupForm
from allauth.socialaccount import helpers

from classes.Tags import Tags

class SignupView(RedirectAuthenticatedUserMixin, CloseableSignupMixin,
                 FormView):
    form_class = SignupForm
    template_name = 'socialaccount/signup.html'

    def dispatch(self, request, *args, **kwargs):
        self.sociallogin = SocialLogin.deserialize(request.session.get('socialaccount_sociallogin'))
        if not self.sociallogin:
            return HttpResponseRedirect(reverse('account_login'))
        return super(SignupView, self).dispatch(request, *args, **kwargs)

    def is_open(self):
        return get_adapter().is_open_for_signup(self.request,
                                                self.sociallogin)

    def get_form_kwargs(self):
        ret = super(SignupView, self).get_form_kwargs()
        ret['sociallogin'] = self.sociallogin
        ret.update({
            'request': self.request
            })
        return ret

    def form_valid(self, form):
        form.save(self.request)
        return helpers.complete_social_signup(self.request,
                                              self.sociallogin)

    def get_context_data(self, **kwargs):
        ret = super(SignupView, self).get_context_data(**kwargs)
        ret.update(dict(site=Site.objects.get_current(),
                        account=self.sociallogin.account))
        tags = Tags()
        ret['all_tags'] = tags.get_tags()
        # print type(self.sociallogin.account)
        #ret['user'] = SocialAccount.objects.get(user__id = request.user.id)
        return ret

    def get_authenticated_redirect_url(self):
        return reverse(connections)

signup = SignupView.as_view()

