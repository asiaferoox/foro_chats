from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Page
from .forms import PageForm
from django.core.paginator import Paginator

def home_view(request):
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')

def page_list(request):
    query = request.GET.get('q', '')
    qs = Page.objects.filter(title__icontains=query).order_by('-created_at') if query else Page.objects.all().order_by('-created_at')
    paginator = Paginator(qs, 5)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'pages/list.html', {'page_obj': page_obj, 'query': query})


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, 'pages/detail.html', {'page': page})

def page_list(request):
    pages = Page.objects.all().order_by('-created_at')
    return render(request, 'pages/list.html', {'pages': pages})


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, 'pages/detail.html', {'page': page})


@login_required
def page_create(request):
    form = PageForm(request.POST or None)
    if form.is_valid():
        page = form.save(commit=False)
        page.author = request.user
        page.save()
        messages.success(request, 'Página creada.')
        return redirect('pages:detail', slug=page.slug)
    return render(request, 'pages/form.html', {'form': form})


@login_required
def page_create(request):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.author = request.user
            page.save()
            messages.success(request, 'Página creada correctamente.')
            return redirect('pages:detail', slug=page.slug)
    else:
        form = PageForm()
    return render(request, 'pages/form.html', {'form': form})

@login_required
def page_update(request, slug):
    page = get_object_or_404(Page, slug=slug, author=request.user)
    form = PageForm(request.POST or None, instance=page)
    if form.is_valid():
        form.save()
        messages.success(request, 'Página actualizada.')
        return redirect('pages:detail', slug=page.slug)
    return render(request, 'pages/form.html', {'form': form})

@login_required
def page_delete(request, slug):
    page = get_object_or_404(Page, slug=slug, author=request.user)
    if request.method == 'POST':
        page.delete()
        messages.success(request, 'Página eliminada.')
        return redirect('pages:list')
    return render(request, 'pages/confirm_delete.html', {'page': page})
