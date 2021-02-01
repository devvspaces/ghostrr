from django.urls import path,include
from .views import *

urlpatterns = [
    path('', IndexPage.as_view(), name='index_page'),
    path('terms/', TermsPage.as_view(), name='terms'),
    path('cases/', CasePage.as_view(), name='cases'),
    path('pricing/', PricingPage.as_view(), name='pricings'),
    path('about/', AboutPage.as_view(), name='about'),
    path('blogs/', HistoricalBlogs.as_view(), name='blogs'),
    path('edit_limit/', EditLimitPage.as_view(), name='edit_limit'),
    path('blogs/create_blog/', CreateAndEdiBlogPage.as_view(), name='create_blog'),
    path('blogs/update/<str:slug>/', EdiBlogPage.as_view(), name='update_blog'),
    path('blogs/delete/<str:slug>/', DeleteBlog.as_view(), name='delete_blog'),
]