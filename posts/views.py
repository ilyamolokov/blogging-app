from django.http import HttpResponse, Http404
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import PostForm
# Create your views here.

@login_required
def posts_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "New post was successfully created")
        return redirect(instance.get_absolute_url())
    context = {'form': form}
    return render(request, 'post_create.html', context)

def posts_detail(request, id=None):
    today = timezone.now().date()
    obj = get_object_or_404(Post, id=id)
    if obj.publish > today or obj.draft:
        raise Http404
    context = {
        'obj': obj,
    }
    return render(request, 'post_detail.html', context)

def posts_list(request):
    today = timezone.now().date()
    queryset = Post.objects.active()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)

        ).distinct()
    paginator = Paginator(queryset, 10)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    queryset = paginator.get_page(page)

    context = {'queryset':queryset, "page_request_var":page_request_var, 'today':today}
    return render(request, 'post_list.html', context)

@login_required
def posts_update(request, id=None):
    obj = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully updated")
        return redirect(obj.get_absolute_url())
    context = {
        'obj': obj,
        'form':form
    }
    return render(request, 'post_form.html', context)
@login_required
def posts_delete(request, id=None):
    obj = get_object_or_404(Post, id=id)
    obj.delete()
    messages.success(request, "Post was successfully deleted")
    return redirect('posts:list')

@login_required
def posts_drafts(request):
    today = timezone.now().date()
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)

        ).distinct()
    paginator = Paginator(queryset, 10)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    queryset = paginator.get_page(page)

    context = {'queryset':queryset, "page_request_var":page_request_var, 'today': today}
    return render(request, 'post_drafts.html', context)
