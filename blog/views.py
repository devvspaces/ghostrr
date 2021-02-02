import time

from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView, FormView
from django.urls import reverse

from .models import Blogs
from .forms import CreateBlogForm, EditLimitForm
from .utils import call_gpt, get_limit_for_level

# Create your views here.
# def home (request):
#     return render (request,'blog/home.html')

# def about (request):
#     return render (request,'blog/about.html')

# def cases (request):
#     return render (request,'blog/cases.html')

# def pricing (request):
#     return render (request,'blog/pricing.html')


class IndexPage(TemplateView):
    template_name = 'blog/index.html'
    extra_context = {
        'title': 'Home'
    }
    
    def get_context_data(self, *args, **kwargs):
        context = self.extra_context

        return context

class TermsPage(TemplateView):
    template_name = 'blog/terms.html'
    extra_context = {
        'title': 'Terms and Conditions'
    }

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


class HistoricalBlogs(LoginRequiredMixin, ListView):
    template_name = 'blog/blogs.html'
    extra_context = {
        'title': 'Historical Blogs'
    }
    model = Blogs
    context_object_name = 'blogs'
    paginate_by = 4

    def get_queryset(self, *args, **kwargs):
        results = self.model.objects.filter(profile=self.request.user.profile)

        return results

    def get_context_data(self, *args, **kwargs):
        context = self.extra_context

        # Get the data for blogs
        data = self.get_queryset()
        data_count = data.count()

        # Get the page num query
        page_num = self.request.GET.get('page')

        # if page num is not there default page_num variable to one to use for paginator
        if not page_num:
            page_num = 1
        page_obj = Paginator(data, self.paginate_by)
        current_data = page_obj.page(page_num)
        context['page_obj'] = current_data
        context['total_blogs'] = data.count()
        if data_count > 1:
            context['blog_plural_or_not'] = 'blogs'
        elif data_count == 1:
            context['blog_plural_or_not'] = 'blog'

        context[self.context_object_name] = current_data

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        # Get the search query
        search_query = self.request.GET.get('search')

        # If search query is available we want to filter queryset results
        if search_query:
            data = self.get_queryset().filter(title__contains = search_query)
            data_count = data.count()
            context[self.context_object_name] = data
            context['page_obj'] = 0
            context['total_blogs'] = data_count
            if data_count > 1:
                context['blog_plural_or_not'] = 'blogs'
            elif data_count == 1:
                context['blog_plural_or_not'] = 'blog'

        return render(request, self.template_name, context)


class CreateAndEdiBlogPage(LoginRequiredMixin, FormView):
    template_name = 'blog/edit.html'
    extra_context = {
        'title': 'Create Blog'
    }
    form_class = CreateBlogForm
    
    def get_context_data(self, *args, **kwargs):
        context = self.extra_context

        form = self.get_form_class()
        context['form'] = form()

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        return render(request, self.template_name, context)
    
    def post(self, *args, **kwargs):
        request = self.request

        if request.is_ajax():
            # time.sleep(3)
            # Inputing data in form to validate
            # Copyin request.POST
            default_post = request.POST.copy()
            default_post['pk'] = request.user.pk

            form = self.get_form_class()
            form = form(default_post)

            if form.is_valid():
                # Check if user have enough credit to use the api
                user_credit = request.user.profile.credit

                # Set returning data
                data_return = {
                    'title': 'Enter the title you want for this blog here',
                    'sentence': 'Describe the blog you want to generate here',
                    'copy_length': 'Enter the length of copy you want',
                }

                if user_credit > 0:
                    # Use api to generate text
                    title = form.cleaned_data.get('title')
                    sentence = form.cleaned_data.get('sentence')
                    copy_length = form.cleaned_data.get('copy_length')

                    # Analyze the response length
                    if copy_length == 1:
                        copy_length = 500
                    else:
                        copy_length = 1000

                    try:
                        response_data = call_gpt(sentence, copy_length)

                        texts = response_data['choices'][0]['text']
                    except:
                        texts = ''
                        data_return['error_message'] = 'We could not generate your text for you please try again'
                        return JsonResponse(data_return, status=200)

                    # This means if the data returned is not greater than 50% of the sentence length
                    # required by the user, this should not run
                    if len(texts) > 10:
                        # Reduce user request on succefull call of api
                        request.user.profile.credit = user_credit - 1
                        request.user.profile.save()

                        # Combine the title and sentence
                        total_text = title + '       ' + sentence + '       '
                        data_return['text'] = total_text + texts
                    else:
                        data_return['text'] = ''
                        data_return['error_message'] = 'Your text generation was not completed, please try again'
                    
                    return JsonResponse(data_return, status=200)
                else:
                    # Setting text to zero tells the browser that this user has no more credits
                    data_return['text'] = ''
                    data_return['error_message'] = 'You have no more credits, buy more credits to generate more contents'
                    return JsonResponse(data_return, status=200)
            
            return JsonResponse({'errors': form.errors}, status=400)

        
        form = self.get_form_class()
        default_post = request.POST.copy()
        default_post['pk'] = request.user.pk
        form = form(default_post)

        if form.is_valid():
            blog = form.save()
            
            # Set the user profile
            blog.profile = request.user.profile
            blog.save()

            messages.success(request, 'Your blog has been successfully created')
            return redirect('account')
        
        context = self.get_context_data()
        context['form'] = form

        return render(request, self.template_name, context)


class EdiBlogPage(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'blog/edit.html'
    extra_context = {
        'title': 'Edit blog',
        'update': '1'
    }
    form_class = CreateBlogForm

    def test_func(self, *args, **kwargs):
        user = self.request.user

        # Get slug from request and get blog instance
        slug = self.kwargs.get('slug')
        blog = get_object_or_404(Blogs, slug=slug)

        if user == blog.profile.user:
            return True
        return False
        
    
    def get_context_data(self, *args, **kwargs):
        context = self.extra_context

        # Get slug from request and get blog instance
        slug = self.kwargs.get('slug')
        blog = get_object_or_404(Blogs, slug=slug)

        form = self.get_form_class()

        default_post = self.request.POST.copy()
        default_post['title'] = blog.title
        default_post['sentence'] = blog.sentence
        default_post['copy_length'] = blog.copy_length
        default_post['copy_text'] = blog.copy_text
        default_post['pk'] = self.request.user.pk

        form = form(default_post)

        context['form'] = form
        context['blog'] = blog

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        return render(request, self.template_name, context)
    
    def post(self, *args, **kwargs):
        request = self.request

        if request.is_ajax():
            # time.sleep(3)
            # Inputing data in form to validate
            # Copyin request.POST
            default_post = request.POST.copy()
            default_post['pk'] = request.user.pk

            form = self.get_form_class()
            form = form(default_post)

            if form.is_valid():
                # Check if user have enough credit to use the api
                user_credit = request.user.profile.credit

                # Set returning data
                data_return = {
                    'title': 'Enter the title you want for this blog here',
                    'sentence': 'Describe the blog you want to generate here',
                    'copy_length': 'Select the length of copy you want',
                }

                if user_credit > 0:
                    # Use api to generate text
                    title = form.cleaned_data.get('title')
                    sentence = form.cleaned_data.get('sentence')
                    copy_length = form.cleaned_data.get('copy_length')

                    # Analyze the response length
                    if copy_length == 1:
                        copy_length = 500
                    else:
                        copy_length = 1000

                    try:
                        response_data = call_gpt(sentence, copy_length)

                        texts = response_data['choices'][0]['text']
                    except:
                        texts = ''
                        data_return['error_message'] = 'We could not generate your text for you please try again'
                        return JsonResponse(data_return, status=200)

                    # This means if the data returned is not greater than 50% of the sentence length
                    # required by the user, this should not run
                    if len(texts) > 10:
                        # Reduce user request on succefull call of api
                        request.user.profile.credit = user_credit - 1
                        request.user.profile.save()

                        # Combine the title and sentence
                        total_text = title + '       ' + sentence + '       '
                        data_return['text'] = total_text + texts
                    else:
                        data_return['text'] = 0
                        data_return['error_message'] = 'Your text generation was not completed, please try again'
                    
                    return JsonResponse(data_return, status=200)
                else:
                    # Setting text to zero tells the browser that this user has no more credits
                    data_return['text'] = 0
                    data_return['error_message'] = 'You have no more credits, buy more credits to generate more contents'
                    return JsonResponse(data_return, status=200)
            
            return JsonResponse({'errors': form.errors}, status=400)


        form = self.get_form_class()
        default_post = request.POST.copy()
        default_post['pk'] = request.user.pk
        form = form(default_post)

        if form.is_valid():
            updated_blog = form.save()

            # Get slug from request and get blog instance
            slug = self.kwargs.get('slug')
            blog = get_object_or_404(Blogs, slug=slug)
            
            # Set the user profile
            blog.title = updated_blog.title
            blog.sentence = updated_blog.sentence
            blog.copy_length = updated_blog.copy_length
            blog.copy_text = updated_blog.copy_text
            blog.save()
            
            messages.success(request, 'Your blog has been successfully updated')
            return redirect(reverse('update_blog', kwargs={'slug': slug}))
        
        context = self.get_context_data()
        context['form'] = form

        return render(request, self.template_name, context)


class DeleteBlog(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'blog/blogs.html'
    extra_context = {
        'title': 'Delete blog'
    }

    def test_func(self, *args, **kwargs):
        user = self.request.user

        # Get slug from request and get blog instance
        slug = self.kwargs.get('slug')
        blog = get_object_or_404(Blogs, slug=slug)

        if user == blog.profile.user:
            return True
        return False

    def get(self, request, *args, **kwargs):
        # Get slug from request and get blog instance
        slug = self.kwargs.get('slug')
        blog = get_object_or_404(Blogs, slug=slug)

        blog.delete()
        
        messages.success(request, 'Your blog has been successfully deleted')
        return redirect('account')


class EditLimitPage(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'blog/edit_limit.html'
    extra_context = {
        'title': 'Edit Limit',
    }
    form_class = EditLimitForm

    def test_func(self, *args, **kwargs):
        user = self.request.user

        if user.is_staff:
            return True
        return False

    def get_context_data(self, *args, **kwargs):
        context = self.extra_context
        form = self.get_form_class()
        default_post = self.request.POST.copy()
        default_post['free_limit'] = get_limit_for_level('1')
        default_post['pro_limit'] = get_limit_for_level('2')
        default_post['enterprise_limit'] = get_limit_for_level('3')

        context['form'] = form(default_post)

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        return render(request, self.template_name, context)
    
    def post(self, *args, **kwargs):
        request = self.request

        form = self.get_form_class()
        form = form(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully user limits')
            return redirect('edit_limit')
        
        
        context = self.get_context_data()
        context['form'] = form

        return render(request, self.template_name, context)