from django.utils import timezone
from .models import Post
from .forms import PostForm, UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  login, authenticate, get_user_model
from django.views import generic
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render , redirect, get_object_or_404
from blog.models import ConfirmacionForm



def post_portada(request):
    if request.method == "POST":
        form = PostForm(request.POST)
    else:
        form = PostForm()
    return render(request, 'blog/post_portada.html', {'form': form})


def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})


def post_login(request):

    url_next = request.GET.get('next', None) 
    if request.method == "POST":
        form = UserForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if url_next is not None:
                return HttpResponseRedirect(url_next)
            else:
                return HttpResponseRedirect('/') 
        else:
            messages.success(request, "Usuario/contraseña ingresado invalido") 
    else:
        form = UserForm(request.POST)
    return render(request, 'blog/post_login.html', {'form': form})




def post_confirmar(request, activacion_token):
    if request.user.is_authenticated():
        HttpResponseRedirect('blog/post_portada.html')
    confirmacion  = get_object_or_404(ConfirmacionForm, activacion_token = activacion_token )    
    user = confirmacion.user
    user.is_active = True
    user.save()
    return render(request, 'blog/post_portada.html', {'form': form})