from django.contrib import admin
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext as _

from .forms import SendEmailForm

def send_email_view(request):
    if request.method == 'POST':
        form = SendEmailForm(request.POST)
        if form.is_valid():
            send_from = form.cleaned_data['send_from']
            recipients = form.cleaned_data['recipients']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=send_from,
                    recipient_list=[email.strip() for email in recipients.split(',') if email.strip()],
                    fail_silently=False,
                )
                messages.success(request, _('Email sent successfully'))
                return redirect('admin:index')
            except Exception as e:
                messages.error(request, _('Failed to send email: %s') % str(e))
    else:
        form = SendEmailForm()
        
    context = dict(
        admin.site.each_context(request),
        title=_('Send Email'),
        form=form,
    )
    return render(request, 'admin/send_email.html', context)
