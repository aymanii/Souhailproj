# Generated by Django 5.0.6 on 2024-07-02 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_visite_remarques_alter_visite_dossierpatient'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='checking',
            field=models.BooleanField(default=False),
        ),
    ]
