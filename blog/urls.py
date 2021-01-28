from django.urls import path,include
from .views import *

urlpatterns = [
    path('', IndexPage.as_view(), name='index_page'),
    path('cases/', CasePage.as_view(), name='cases'),
    # path('cases/', cases, name='cases'),
    # path('about/', about, name='about'),
    # path('pricing/', pricing, name='pricing'),
    path('pricing/', PricingPage.as_view(), name='pricings'),
    path('about/', AboutPage.as_view(), name='about'),
    path('blogs/', HistoricalBlogs.as_view(), name='blogs'),
    path('blogs/create_blog/', CreateAndEdiBlogPage.as_view(), name='create_blog'),
    path('blogs/update/<str:slug>/', EdiBlogPage.as_view(), name='update_blog'),
]
