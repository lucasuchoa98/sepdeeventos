# Generated by Django 2.2 on 2020-07-07 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventodef', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='upload',
            field=models.FileField(upload_to=''),
        ),
    ]
