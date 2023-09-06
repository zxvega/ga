from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, pre_save, post_save, post_delete

# Create your models here.

class Type(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated = models.DateTimeField(auto_now=True, verbose_name='Modificado')
    title = models.CharField(max_length=255, default='', verbose_name='Tipo de Vehiculo')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'

class State(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated = models.DateTimeField(auto_now=True, verbose_name='Modificado')
    title = models.CharField(max_length=255, default='', verbose_name='Estado')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

class Location(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated = models.DateTimeField(auto_now=True, verbose_name='Modificado')
    title = models.CharField(max_length=255, default='', verbose_name='Ubicacion')
    active = models.BooleanField(default=True,verbose_name='Activo')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated = models.DateTimeField(auto_now=True, verbose_name='Modificado')
    title = models.CharField(max_length=255, default='', verbose_name='Marca')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated = models.DateTimeField(auto_now=True, verbose_name='Modificado')
    name = models.CharField(max_length=255, verbose_name='Nombre')
    last_name = models.CharField(max_length=255, verbose_name='Apellido')
    document = models.IntegerField(verbose_name='Documento de Identidad', blank=True, null=True )
    addres = models.CharField(max_length=255, blank=True, null=True, verbose_name='Dirección')
    telephone = models.IntegerField(verbose_name='Telefono')

    def __str__(self):
        return self.name + ' ' + self.last_name

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated = models.DateTimeField(auto_now=True, verbose_name='Modificado')
    title = models.CharField(max_length=255, default='', verbose_name='Descripcion')
    detail = models.CharField(max_length=255, default='', verbose_name='Detalles')
    serie = models.CharField(max_length=255, default='', verbose_name='Chasis', unique=True)
    model = models.CharField(max_length=255, default='', verbose_name='Modelo')
    year = models.IntegerField(verbose_name='Año')
    color = models.CharField(max_length=255, default='', verbose_name='Color')
    type = models.ForeignKey(Type, related_name='vehicles',blank=True, null=True ,on_delete=models.PROTECT,verbose_name='Tipo')
    brand = models.ForeignKey(Brand, related_name='vehicles',blank=True, null=True ,on_delete=models.PROTECT,verbose_name='Marca')
    location = models.ForeignKey(Location, related_name='vehicles',blank=True, null=True, on_delete=models.PROTECT,verbose_name='Ubicacion')
    state = models.ForeignKey(State, related_name='vehicles',blank=True, null=True, on_delete=models.PROTECT,verbose_name='Estado')
    customer = models.ForeignKey(Customer, related_name='vehicles',blank=True, null=True ,on_delete=models.PROTECT,verbose_name='Propietario')
    available = models.BooleanField(default=True,verbose_name='Disponible')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated = models.DateTimeField(auto_now=True, verbose_name='Modificado')
    user = models.ForeignKey(User,related_name='employees', on_delete=models.PROTECT,verbose_name='Usuario')
    department = models.ForeignKey(Location, related_name='employees',blank=True, null=True, on_delete=models.PROTECT,verbose_name='Ubicacion')

    def __str__(self):
        return str(self.user.first_name) + ' ' +str(self.user.last_name) 

    class Meta:
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'

class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated = models.DateTimeField(auto_now=True, verbose_name='Modificado')
    date = models.DateField(verbose_name='Fecha')
    vehicle = models.ForeignKey(Vehicle, related_name='sales',blank=True, null=True ,on_delete=models.PROTECT,verbose_name='Vehiculo')
    customer = models.ForeignKey(Customer, related_name='sales',blank=True, null=True, on_delete=models.PROTECT,verbose_name='Cliente')
    seller = models.ForeignKey(Employee, related_name='sales',blank=True, null=True, on_delete=models.PROTECT,verbose_name='Vendedor')

    def __str__(self):
        return 'Venta: ' + str(self.id)

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

class Move(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated = models.DateTimeField(auto_now=True, verbose_name='Modificado')
    applicant = models.CharField(max_length=255, default='', verbose_name='Solicitante')
    reason = models.CharField(max_length=255, default='', verbose_name='Motivo')    
    date = models.DateField(verbose_name='Fecha')
    destination_location = models.ForeignKey(Location, related_name='moves',blank=True, null=True, on_delete=models.PROTECT,verbose_name='Destino')

    def __str__(self):
        return 'Movimiento: ' + str(self.id)

    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'

class MoveDetail(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated = models.DateTimeField(auto_now=True, verbose_name='Modificado')
    move = models.ForeignKey(Move, related_name='move_detail',blank=True, null=True ,on_delete=models.CASCADE,verbose_name='Movimiento')
    vehicle = models.ForeignKey(Vehicle, related_name='move_detail',blank=True, null=True ,on_delete=models.PROTECT,verbose_name='Vehiculo')
    source_location = models.ForeignKey(Location, related_name='move_detail',blank=True, null=True, on_delete=models.PROTECT,verbose_name='Origen')

    def __str__(self):
        return 'Detalle: ' + str(self.id)

    class Meta:
        verbose_name = 'Detalle'
        verbose_name_plural = 'Detalles'

# Señales Sale 

@receiver(post_save, sender=Sale)
def set_vehicle_sold(sender, created, instance, **kwargs):
    if created:
        vehicle = Vehicle.objects.get(id=instance.vehicle.id)
        vehicle.customer = instance.customer
        vehicle.location = None
        vehicle.available = False
        vehicle.save()

# Señales Usuario

@receiver(post_save, sender=User)
def set_employee(sender, created, instance, **kwargs):
    if created:
        employee = Employee()
        employee.user = instance        
        employee.save()

# Señales Detalle del Movimiento

@receiver(post_save, sender=MoveDetail)
def update_vehicle_move(sender, created, instance, **kwargs):
    if created:
        vehicle = Vehicle.objects.get(id=instance.vehicle.id)
        instance.source_location = vehicle.location
        instance.save()
        vehicle.location = instance.move.destination_location
        vehicle.save()

@receiver(post_delete, sender=MoveDetail)
def update_vehicle_move_reverse(sender, instance, **kwargs):
    vehicle = Vehicle.objects.get(id=instance.vehicle.id)
    vehicle.location = instance.source_location
    vehicle.save()
