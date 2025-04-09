# Generated by Django 5.1.3 on 2025-04-09 19:02

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfumeria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=8)),
                ('genero', models.CharField(choices=[('H', 'Hombre'), ('M', 'Mujer'), ('U', 'Unisex')], max_length=1)),
                ('imagen', models.ImageField(upload_to='perfumerias/')),
                ('stock', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=6)),
                ('tipo_pan', models.CharField(blank=True, choices=[('TRADICIONAL', 'Tradicional'), ('INTEGRAL', 'Integral'), ('SIN_GLUTEN', 'Sin Gluten')], max_length=15, null=True)),
                ('imagen', models.ImageField(upload_to='bagueteria/')),
                ('disponible', models.BooleanField(default=True)),
                ('ingredientes', models.TextField(blank=True)),
                ('tiempo_preparacion', models.IntegerField(blank=True, help_text='Tiempo en minutos', null=True)),
                ('destacado', models.BooleanField(default=False)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Producto(bagueteria)',
            },
        ),
        migrations.CreateModel(
            name='ProductoEstudio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('categoria', models.CharField(choices=[('ficcion', 'Ficción'), ('no_ficcion', 'No Ficción'), ('educativo', 'Educativo'), ('ciencia', 'Ciencia'), ('historia', 'Historia'), ('fantasia', 'Fantasía'), ('romance', 'Romance'), ('arte', 'Arte'), ('misterio', 'Misterio'), ('infantil', 'Infantil')], max_length=100)),
                ('imagen', models.ImageField(upload_to='productos_estudio/')),
            ],
            options={
                'verbose_name_plural': 'Libreria',
            },
        ),
        migrations.CreateModel(
            name='ProductoMarket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('categoria', models.CharField(choices=[('ALIMENTOS', 'Alimentos'), ('BEBIDAS', 'Bebidas'), ('LIMPIEZA', 'Limpieza'), ('OTROS', 'Otros')], max_length=10)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=6)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='market/')),
                ('fecha_ingreso', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-fecha_ingreso'],
            },
        ),
        migrations.CreateModel(
            name='ProyectoConstruccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('ubicacion', models.CharField(max_length=200)),
                ('fecha_inicio', models.DateField()),
                ('fecha_estimada_fin', models.DateField()),
                ('estado', models.CharField(choices=[('PLANIFICACION', 'En planificación'), ('CONSTRUCCION', 'En construcción'), ('FINALIZADO', 'Finalizado'), ('ENTREGADO', 'Entregado')], default='PLANIFICACION', max_length=15)),
                ('imagen_principal', models.ImageField(upload_to='construccion/')),
                ('presupuesto', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='Viaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('pais', models.CharField(choices=[('ES', 'España'), ('FR', 'Francia'), ('IT', 'Italia'), ('DE', 'Alemania'), ('PT', 'Portugal'), ('MX', 'México'), ('AR', 'Argentina'), ('CL', 'Chile'), ('CO', 'Colombia'), ('PE', 'Perú'), ('US', 'Estados Unidos'), ('CA', 'Canadá'), ('BR', 'Brasil'), ('JP', 'Japón'), ('CN', 'China'), ('AU', 'Australia'), ('IN', 'India'), ('EG', 'Egipto'), ('ZA', 'Sudáfrica'), ('GR', 'Grecia')], default='ES', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('telefono', models.CharField(blank=True, max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pedido', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('PREPARACION', 'En preparación'), ('LISTO', 'Listo para recoger'), ('ENTREGADO', 'Entregado'), ('CANCELADO', 'Cancelado')], default='PENDIENTE', max_length=15)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('notas', models.TextField(blank=True, null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Pedido(bagueteria)',
            },
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=6)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=8)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='app_centroonline_ventura.pedido')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_centroonline_ventura.producto')),
            ],
            options={
                'verbose_name_plural': 'Detalle de pedido (bagueteria)',
            },
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(choices=[('TOYOTA', 'Toyota - Ventura'), ('HONDA', 'Honda - Ventura'), ('FORD', 'Ford - Ventura'), ('CHEVROLET', 'Chevrolet - Ventura'), ('BMW', 'BMW - Ventura'), ('TESLA', 'Tesla - Ventura'), ('HYUNDAI', 'Hyundai - Ventura')], max_length=10)),
                ('modelo', models.CharField(max_length=100)),
                ('año', models.IntegerField()),
                ('tipo', models.CharField(choices=[('SEDAN', 'Sedán'), ('SUV', 'SUV'), ('PICKUP', 'Pickup'), ('DEPORTIVO', 'Deportivo'), ('ELECTRICO', 'Eléctrico'), ('HIBRIDO', 'Híbrido')], max_length=10)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=12)),
                ('kilometraje', models.IntegerField()),
                ('color', models.CharField(max_length=30)),
                ('transmision', models.CharField(choices=[('AUTOMATICO', 'Automático'), ('MANUAL', 'Manual'), ('CVT', 'CVT')], max_length=10)),
                ('motor', models.CharField(max_length=50)),
                ('potencia', models.IntegerField(help_text='Caballos de fuerza')),
                ('descripcion', models.TextField()),
                ('imagen_principal', models.ImageField(upload_to='vehiculos/')),
                ('disponible', models.BooleanField(default=True)),
                ('fecha_ingreso', models.DateTimeField(default=django.utils.timezone.now)),
                ('destacado', models.BooleanField(default=False)),
                ('reservado', models.BooleanField(default=False)),
                ('fecha_reserva', models.DateTimeField(blank=True, null=True)),
                ('reservado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Vehículos',
                'ordering': ['-fecha_ingreso'],
            },
        ),
        migrations.CreateModel(
            name='TestDrive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_solicitud', models.DateTimeField(auto_now_add=True)),
                ('fecha_test', models.DateTimeField()),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('CONFIRMADO', 'Confirmado'), ('COMPLETADO', 'Completado'), ('CANCELADO', 'Cancelado')], default='PENDIENTE', max_length=10)),
                ('notas', models.TextField(blank=True, null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_centroonline_ventura.vehiculo')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=15)),
                ('direccion', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('comentarios', models.TextField(blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_centroonline_ventura.vehiculo')),
            ],
            options={
                'verbose_name': 'Reserva de vehículo',
                'verbose_name_plural': 'Reservas de vehículos',
                'ordering': ['-fecha_creacion'],
            },
        ),
    ]
