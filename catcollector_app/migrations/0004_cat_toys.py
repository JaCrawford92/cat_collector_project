# Generated by Django 5.0.4 on 2024-05-04 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catcollector_app', '0003_toy_alter_feeding_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='cat',
            name='toys',
            field=models.ManyToManyField(to='catcollector_app.toy'),
        ),
    ]
