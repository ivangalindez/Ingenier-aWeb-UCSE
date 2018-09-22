from django.utils import timezone
from .models import Post
from django.shortcuts import render , redirect, render_to_response, get_object_or_404
from .forms import PostForm, UserForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.views import generic
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
import random
import os, string
from django.core.context_processors import csrf
import hashlib, datetime, random
from blog.models import ConfirmacionForm


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
        form = UserForm()
    return render(request, 'blog/post_login.html', {'form': form})

class post_registro(View):
    form_class = RegisterForm
    #muestro el form
    def get(self,request):
        form = self.form_class(None)
        return render(request, 'blog/post_registro.html', {'form': form})
    #lo controlo
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            if not User.objects.filter(username=form.cleaned_data['username']).exists():
                if not User.objects.filter(email=form.cleaned_data['email']).exists():
                    if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                    
                        user = form.save(commit=False)
                        username = form.cleaned_data['username']
                        email = form.cleaned_data['email']
                        password1 = form.cleaned_data['password1']
                        password2 = form.cleaned_data['password2']
                        nombre = form.cleaned_data['nombre']
                        apellido = form.cleaned_data['apellido']

                        user = User.objects.create_user(username=username, password=password1,email=email,first_name=nombre,last_name=apellido)
                        user.is_active = False
                        
                    
                        N = 20
                        token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))           
                        usr_confirmacion = ConfirmacionForm(usuario = user, activacion_token = token)

                        email_subject   = 'Comunidad Bateros'
                        email_body      = "Hola %s!, Gracias por registrarte. Para activar tu cuenta haga clíck en el siguiente link: http://127.0.0.1:8000/post/portada/%s" % (nombre, token)
                        send_mail(email_subject,email_body, 'comunidadbateros@gmail.com',[email] )

                        user.save()
                        usr_confirmacion.save()

                        messages.success(request, "El usuario se ha registrado con exito. Vefique su casilla de correo")
                        
                        
                    else:
                        messages.success(request, "Las contraseñas ingresadas no son iguales")
                else:
                    messages.success(request, "El correo ingresado ya esta asociado a una cuenta")
            else:
                messages.success(request, "El Usuario ingresado ya se encuentra registrado.")
        return render(request, 'blog/post_registro.html')

def post_portada(request):
    return render(request, 'blog/post_portada.html', {'form': form})

@login_required
def logout(request):
    logout(request)
    return redirect('post_portada')


def post_confirmar(request, activacion_token):
    if request.user.is_authenticated():
        HttpResponseRedirect('blog/post_portada.html')
    confirmacion  = get_object_or_404(ConfirmacionForm, activacion_token = activacion_token )    
    user = confirmacion.user
    user.is_active = True
    user.save()
    return render(request, 'blog/post_portada.html')






