from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import HomeCaptchaForm

# Create your views here.


class HomePageView(TemplateView):

    def get(self, request):
        proto = 'https://'
        if request.META['SERVER_PROTOCOL'] and request.META['SERVER_PROTOCOL'][0:5] == 'HTTP/':
            proto = 'http://'
        server = proto + request.META['HTTP_HOST']
        data = {'captcha_form': HomeCaptchaForm, 'host_url':  server}
        return render(request, 'index.html', data)


class AboutPageView(TemplateView):
    template_name = 'about.html'