from django.urls import path,include
from .views import *

urlpatterns = [
    path('', IndexPage.as_view(), name='index_page'),
    path('cases/', CasePage.as_view(), name='cases'),
    # path('cases/', cases, name='cases'),
    # path('about/', about, name='about'),
    # path('pricing/', pricing, name='pricing'),
    path('pricing/', PricingPage.as_view(), name='pricings'),
    path('about_us/', AboutPage.as_view(), name='about'),
]
