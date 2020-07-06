from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import UserCreationForm
from asesoria.forms import LoginForm
from asesoria.models import cliente as Cli, direccion as Dir
from asesoria.inter_base import retorna_clientes, save_cliente, busca_cliente, busca_direccion, update_cliente, retorna_direcciones, baja_cliente, retorna_clientes_acc
from django.core.files.storage import FileSystemStorage


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
    if request.user.is_authenticated:
        return render(request, "dashboard.html")
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
            nombre=username = request.POST['username']
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
                return render(request,'dashboard.html',{'message':mess,'manager_id':user.id})
            else:
                mess='Usuario invalido'

    # Si llegamos al final renderizamos el formulario
    return render(request, "login.html", {'form': form, 'message':mess})
    #return render(request, "login.html")
def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/login')


def dashboard(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        indice=round(len(retorna_clientes_acc(request.user.id,'A'))/len(retorna_clientes_acc(request.user.id)),2)

        return render(request, "dashboard.html",{'total_clientes':len(retorna_clientes_acc(request.user.id)),
                                                 'clientes_alta':len(retorna_clientes_acc(request.user.id,'A')),
                                                 'clientes_baja':len(retorna_clientes_acc(request.user.id,'B')),
                                                 'indice_gil':indice})


    # En otro caso redireccionamos al login
    return redirect('/login')

def listado(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    lista_cli=retorna_clientes()

    return render(request, 'listado.html', {'lista_cli':lista_cli})

def listadoDir(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    lista_dir=retorna_direcciones()

    return render(request, 'listadoDir.html', {'lista_dir':lista_dir})

def load_foto(request):
    try:
        if request.FILES['MyFile']:
            myfile = request.FILES['MyFile']
            fs = FileSystemStorage()
            filename = fs.save(request.POST['email'] + '.jpg', myfile)
            return  ' (Con foto)!'
    except:
        return ' (Sin foto)!'

def determina_accion(request):
    if request.POST['usuario_busqueda'] != '0':  # Si el campo de busqueda es distinto de 0 traigo cliente consultado
        accion = 'BUSQUEDA'
    else:
        try:
            if request.POST['uid']=='' : # SI uid no esta presente uid es alta y se genera una excepción, si no es modificación
                accion='ALTA'
            else:
                try:
                    aux = request.POST['check_baja']
                    accion = 'BAJA'
                except:
                    accion = 'MODIFICACION'
        except:
            accion = 'ALTA'

    return accion

def cliente(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    resultado='Nuevo Usuario'
    #To do Buscar cliente y trae cliente
    if request.method == "POST":

        check_baja = ''
        status_campos = ''
        accion=determina_accion(request)
        if accion=='BUSQUEDA':#Busca cliente
            cli_res=busca_cliente(request.POST['usuario_busqueda'])
            dir_res=busca_direccion(request.POST['usuario_busqueda'])
            if not dir_res:
                dir_res=[Dir()]
            resultado = 'Modificar usuario'

            status_campos = ''
            if cli_res.estado=='B':
                status_campos='disabled'
                check_baja='checked'
            else:
                 check_baja =''

            foto_cliente =cli_res.email+'.jpg'
            nombre_display = cli_res.nombre + ' ' + cli_res.apellido
            comentario_display = cli_res.comentario

            return render(request, "cliente.html", {'check_baja':check_baja,
                                                    'status_campos':status_campos,
                                                    'comentario_display':comentario_display,
                                                    'nombre_display':nombre_display,
                                                    'foto_cliente':foto_cliente,
                                                    'resultado': resultado,
                                                    'lista_cli':Cli.objects.all(),
                                                    'cli_select':cli_res.id,
                                                    'dir_x_defecto':dir_res[0],
                                                    'cliente_x_defecto':cli_res})

        elif accion=='BAJA':
            try:
                cli_res=baja_cliente(request.POST['uid'])
                status_campos = 'disabled'
                check_baja = 'checked'
                resultado = 'Cliente dado de baja con Exito!'
            except:
                resultado = 'Error en la baja del!'

        elif accion=='MODIFICACION': #MODIFICACION CLIENTE
            try:
                cli_res = update_cliente(request.POST['uid'], request.POST['nombre'], request.POST['apellido'], request.POST['tipo'],
                                           request.POST['documento'], request.POST['email'], request.POST['comentario'],
                                           request.POST['localidad'], request.POST['provincia'], request.POST['calle'],
                                           request.POST['cp'], request.POST['tipo_dir'], request.POST['pais'],
                                           request.POST['fechanac'])
                foto = ''
                if cli_res is not None:
                    foto=load_foto(request)

                dir_res = busca_direccion(cli_res.id)
                foto_cliente = cli_res.email + '.jpg'
                nombre_display = cli_res.nombre + ' ' + cli_res.apellido
                comentario_display = cli_res.comentario
                resultado = 'Cliente actualizado con Exito!'+foto
                return render(request, "cliente.html", {'check_baja': check_baja,
                                                        'status_campos': status_campos,
                                                        'comentario_display': comentario_display,
                                                        'nombre_display': nombre_display,
                                                        'foto_cliente': foto_cliente,
                                                        'resultado': resultado,
                                                        'lista_cli': Cli.objects.all(),
                                                        'cli_select': cli_res.id,
                                                        'cliente_x_defecto': cli_res,
                                                        'dir_x_defecto': dir_res[0]})

            except:
                resultado = 'Error al actualizar cliente!'

        else: #ALTA CLIENTE
            try:
                cli_res=save_cliente(request.POST['nombre'],  request.POST['apellido'], request.POST['tipo'], request.POST['documento'], request.POST['email'], request.POST['comentario'],
                                 request.POST['localidad'], request.POST['provincia'], request.POST['calle'], request.POST['cp'], request.POST['tipo_dir'], request.POST['pais'],request.POST['fechanac'], request.user.id )
                foto=''
                if cli_res is not None:
                    foto=load_foto(request)
                resultado = 'Cliente dado de alta con Exito.'+foto
                dir_res = busca_direccion(cli_res.id)
                foto_cliente = cli_res.email + '.jpg'
                nombre_display=cli_res.nombre+' '+cli_res.apellido
                comentario_display=cli_res.comentario
                return render(request, "cliente.html", {'check_baja':check_baja,
                                                            'status_campos':status_campos,
                                                            'comentario_display':comentario_display,
                                                            'nombre_display':nombre_display,
                                                            'foto_cliente':foto_cliente,
                                                            'resultado': resultado,
                                                            'lista_cli':Cli.objects.all(),
                                                            'cli_select':cli_res.id,
                                                            'cliente_x_defecto':cli_res,
                                                            'dir_x_defecto':dir_res[0]} )

            except:
                resultado = 'Error al intentar dar de alta cliente.'

        return render(request, "cliente.html",
                      {'resultado': resultado, 'lista_cli': Cli.objects.all(), 'cli_select': ''})


    elif request.method == 'GET':

        try:
            aux = request.GET['cliente_id']
            accion='BUSCAR'
        except:
            accion='Nada'

        if accion=='BUSCAR':
            update_cli=busca_cliente(request.GET['cliente_id'])
            update_dir=busca_direccion(request.GET['cliente_id'])

            if not update_dir:
                update_dir=[Dir()]
            resultado = 'Modificar usuario'

            status_campos = ''
            if update_cli.estado=='B':
                status_campos='disabled'
                check_baja='checked'
            else:
                check_baja =''

            foto_cliente =update_cli.email+'.jpg'
            nombre_display = update_cli.nombre + ' ' + update_cli.apellido
            comentario_display = update_cli.comentario

            return render(request, "cliente.html", {'check_baja':check_baja, 'status_campos':status_campos,'comentario_display':comentario_display,'nombre_display':nombre_display, 'foto_cliente':foto_cliente,'resultado': resultado, 'lista_cli':Cli.objects.all(), 'cli_select':update_cli.id,'dir_x_defecto':update_dir[0],'cliente_x_defecto':update_cli})
        else: #No entra por pos primera vez
            return render(request, "cliente.html", { 'resultado': resultado, 'lista_cli':Cli.objects.all(),'cli_select':''})
    else:
        return render(request, "cliente.html",{'resultado': resultado, 'lista_cli': Cli.objects.all(), 'cli_select': ''})



