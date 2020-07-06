from django.db import models

from core import settings


class cliente(models.Model):
    fechanac = models.DateField()
    nombre=models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    tipo=models.CharField(max_length=50)
    documento=models.CharField(max_length=50)
    email=models.CharField(max_length=200)
    estado=models.CharField(max_length=1)
    comentario=models.CharField(max_length=500, default='-')
    acount_manager=models.CharField(max_length=200)

class telefono (models.Model):
    tipo=models.CharField(max_length=50)
    numero=models.IntegerField()
    t_cliente=models.ForeignKey(cliente,on_delete=models.CASCADE, related_name='t_cliente')

class direccion (models.Model):
    localidad=models.CharField(max_length=100)
    provincia=models.CharField(max_length=100)
    calle=models.CharField(max_length=100)
    cp=models.CharField(max_length=50)
    tipo=models.CharField(max_length=100)
    pais=models.CharField(max_length=100)
    d_cliente=models.ForeignKey(cliente,on_delete=models.CASCADE, related_name='d_cliente')

class producto(models.Model):
    descripcion=models.CharField(max_length=100)
    tipoProduc= models.CharField(max_length=100)

class productoCliente(models.Model):
    id_producto=models.ForeignKey(producto,on_delete=models.CASCADE, related_name='producto')
    id_cliente=models.ForeignKey(cliente,on_delete=models.CASCADE, related_name='cliente')

