# Generated by Django 4.2.3 on 2023-07-14 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Perfil', '0002_conta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='banco',
            field=models.CharField(choices=[('NU', 'Nubank'), ('CE', 'Caixa Economica')], max_length=2),
        ),
    ]