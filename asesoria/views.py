from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import UserCreationForm
from asesoria.forms import LoginForm

def register(request):
    # Creamos el formulario de autenticación vacío
    form = UserCreationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = UserCreationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():

            # Creamos la nueva cuenta de usuario
            user = form.save()

            # Si el usuario se crea correctamente
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "register.html", {'form': form})

def login(request):
    mess=None
    form = LoginForm()
    # Creamos el formulario de autenticación vacío
    #form = AuthenticationForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        mess = 'Entro Pos'
        # Añadimos los datos recibidos al formulario
        #form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            mess = 'Form valido'
            # Recuperamos las credenciales validadas
            #username = form.cleaned_data['username']
            #password = form.cleaned_data['password']
            username = request.POST['username']
            password = request.POST['password']
            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                mess = 'Usu valido'
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                mess = 'Usuario validado'
                return render(request,'welcome.html',{'message':mess})
            else:
                mess='Usuario invalido'

    # Si llegamos al final renderizamos el formulario
    return render(request, "login.html", {'form': form, 'message':mess})
    #return render(request, "login.html")
def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')

def welcome(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "welcome.html")
    # En otro caso redireccionamos al login
    return redirect('/login')
