# Generated by Django 2.1.5 on 2019-02-24 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engineering', '0011_remove_projectquote_vendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectbid',
            name='rfq',
            field=models.BooleanField(default=False),
        ),
    ]
