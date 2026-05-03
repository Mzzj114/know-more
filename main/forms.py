from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class SendEmailForm(forms.Form):
    send_from = forms.EmailField(label=_('From'), required=True, initial=settings.DEFAULT_FROM_EMAIL)
    recipients = forms.CharField(label=_('Recipients'), required=True, help_text=_('Separate recipients with commas'))
    subject = forms.CharField(label=_('Subject'), max_length=255, required=True)
    message = forms.CharField(label=_('Message'), widget=forms.Textarea(attrs={'class': 'vLargeTextField'}), required=True)
