# Generated by Django 2.1.5 on 2019-04-05 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compliance', '0011_auto_20190405_0402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helpissue',
            name='solution',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='helpissue',
            name='status',
            field=models.CharField(default='Unresolved', max_length=255),
        ),
    ]
