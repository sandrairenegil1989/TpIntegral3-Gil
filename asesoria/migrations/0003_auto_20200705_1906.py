# Generated by Django 3.0.7 on 2020-07-05 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asesoria', '0002_cliente_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='acount_manager',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.CharField(max_length=200),
        ),
    ]
