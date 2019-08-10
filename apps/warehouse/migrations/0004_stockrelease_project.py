# Generated by Django 2.1.5 on 2019-04-02 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('engineering', '0017_project_logistics_bidding'),
        ('warehouse', '0003_stockrelease'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockrelease',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='engineering.Project'),
            preserve_default=False,
        ),
    ]
