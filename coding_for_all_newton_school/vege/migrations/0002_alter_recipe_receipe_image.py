# Generated by Django 4.2 on 2023-04-11 16:02

from django.db import migrations, models
import vege.models


class Migration(migrations.Migration):

    dependencies = [
        ('vege', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='receipe_image',
            field=models.ImageField(upload_to=vege.models.get_image_path),
        ),
    ]