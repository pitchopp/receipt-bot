# Generated by Django 4.2.5 on 2023-09-14 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0003_contract_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='apartment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assistant.apartment'),
        ),
    ]
