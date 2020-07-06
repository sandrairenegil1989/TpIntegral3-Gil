from asesoria.models import cliente as Cli, direccion as Dir

def retorna_clientes():
    return Cli.objects.all()

def retorna_clientes_acc(accm_id, estado_cli = None):
    if estado_cli is None:
        return Cli.objects.filter(acount_manager=accm_id)
    else:
        return Cli.objects.filter(acount_manager=accm_id, estado=estado_cli)

def retorna_direcciones():
    return Dir.objects.all()

def busca_cliente(id_cliente):
    return Cli.objects.get(pk=id_cliente)

def busca_direccion(id_cliente):
    return Dir.objects.filter(d_cliente=id_cliente)

def baja_cliente(id_cliente):
    cli=busca_cliente(id_cliente)
    cli.estado='B'
    cli.save()
    return cli

def update_cliente(id_cliente, nombre, apellido, tipo, documento , email, comentario,
                  localidad,provincia,calle,cp,tipo_dir, pais, fechanac):

    cli = busca_cliente(id_cliente)
    try:
        cli.nombre = nombre
        cli.apellido = apellido
        cli.tipo = tipo
        cli.documento = documento
        cli.fechanac = fechanac
        cli.email = email
        cli.comentario = comentario
        cli.save()

        update_direccion(id_cliente,localidad,provincia,calle,cp,tipo_dir, pais, cli)
        return cli
    except:
        return cli


def update_direccion(id_cliente,localidad,provincia,calle,cp,tipo_dir, pais, cli):
    try:
        dire=Dir.objects.filter(d_cliente=cli)
        dire.delete()

        dire_new=Dir()
        dire_new.d_cliente=cli
        dire_new.localidad=localidad
        dire_new.provincia=provincia
        dire_new.calle    =calle
        dire_new.cp       =cp
        dire_new.tipo     =tipo_dir
        dire_new.pais     =pais
        dire_new.save()
    except:
        return False

    return True


def lista_direccion(id_cliente):
    return busca_direccion(id_cliente)[0]

def save_cliente(nombre, apellido, tipo, documento , email, comentario,
                  localidad,provincia,calle,cp,tipo_dir, pais, fechanac, id_acc_manager):
    try:
        cli=Cli()
        cli.nombre    =nombre
        cli.apellido  =apellido
        cli.tipo      =tipo
        cli.estado='A'
        cli.documento =documento
        cli.fechanac  =fechanac
        cli.email     =email
        cli.comentario=comentario
        cli.acount_manager=id_acc_manager
        cli.save()

        if not save_direccion(localidad,provincia,calle,cp,tipo_dir, pais, cli):
            return cli
    except:
        return None

    return cli

def save_direccion(localidad,provincia,calle,cp,tipo, pais, clie):
    try:
        dire=Dir()
        dire.localidad=localidad
        dire.provincia=provincia
        dire.calle    =calle
        dire.cp       =cp
        dire.tipo     =tipo
        dire.pais     =pais
        dire.d_cliente=clie
        dire.save()
    except:
        return False

    return True
