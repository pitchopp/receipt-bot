# Generated by Django 4.2.5 on 2023-09-14 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
