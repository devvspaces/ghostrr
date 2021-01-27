from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
def home (request):
    return render (request,'blog/home.html')

def about (request):
    return render (request,'blog/about.html')

def cases (request):
    return render (request,'blog/cases.html')

def pricing (request):
    return render (request,'blog/pricing.html')


class IndexPage(TemplateView):
    template_name = 'blog/index.html'

class CasePage(TemplateView):
    template_name = 'blog/case.html'
    extra_context = {
        'title': 'Case studies'
    }

class PricingPage(TemplateView):
    template_name = 'blog/pricings.html'
    extra_context = {
        'title': 'Pricing'
    }

class AboutPage(TemplateView):
    template_name = 'blog/about_us.html'
    extra_context = {
        'title': 'About us'
    }