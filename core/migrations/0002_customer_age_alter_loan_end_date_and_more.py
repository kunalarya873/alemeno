# Generated by Django 5.1.3 on 2024-11-28 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='age',
            field=models.IntegerField(default=20),
        ),
        migrations.AlterField(
            model_name='loan',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
