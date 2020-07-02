from django.db import models

class cliente(models.Model):
    nombre=models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    tipo=models.CharField(max_length=50)
    documento=models.IntegerField()
    email=models.CharField(max_length=50)

class telefono (models.Model):
    tipo=models.CharField(max_length=50)
    numero=models.IntegerField()
    t_cliente=models.ForeignKey(cliente,on_delete=models.CASCADE, related_name='t_cliente')

class direccion (models.Model):
    localidad=models.CharField(max_length=100)
    provincia=models.CharField(max_length=100)
    calle=models.CharField(max_length=100)
    numero=models.IntegerField()
    departamento=models.CharField(max_length=50)
    piso=models.IntegerField()
    cp=models.CharField(max_length=50)
    tipo=models.CharField(max_length=100)
    d_cliente=models.ForeignKey(cliente,on_delete=models.CASCADE, related_name='d_cliente')

class producto(models.Model):
    descripcion=models.CharField(max_length=100)
    tipoProduc= models.CharField(max_length=100)

class productoCliente(models.Model):
    id_producto=models.ForeignKey(producto,on_delete=models.CASCADE, related_name='producto')
    id_cliente=models.ForeignKey(cliente,on_delete=models.CASCADE, related_name='cliente')
