from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _


class FarmingConcretePasswordResetForm(PasswordResetForm):

    def save(self, domain_override=None,
             email_template_name='registration/password_reset_email.txt',
             html_email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             request=None):
        """
        Generates a one-use only link for resetting password and sends to the user
        """
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        active_users = UserModel._default_manager.filter(
            email__iexact=email, is_active=True)
        for user in active_users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            if not user.has_usable_password():
                continue
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            subject = _("Password reset on %s") % site_name
            text_content = loader.render_to_string(email_template_name, c)
            html_content = loader.render_to_string(html_email_template_name, c)
            msg = EmailMultiAlternatives(subject, text_content, None, [user.email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
