from asesoria.models import cliente as Cli, direccion as Dir

def retorna_clientes():
    return Cli.objects.all()

def save_cliente(nombre, apellido, tipo, documento , email, comentario,
                  localidad,provincia,calle,cp,tipo_dir, pais, fechanac):
    try:
        cli=Cli()
        cli.nombre    =nombre
        cli.apellido  =apellido
        cli.tipo      =tipo
        cli.documento =documento
        cli.fechanac  =fechanac
        cli.email     =email
        cli.comentario=comentario
        cli.save()

        if not save_direccion(localidad,provincia,calle,cp,tipo_dir, pais, cli):
            return False
    except:
        return False
    return True

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
