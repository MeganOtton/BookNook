# Generated by Django 4.2.19 on 2025-03-18 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0003_alter_profile_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='birthdate_author',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('Child', 'Child Reader'), ('Adult', 'Adult Reader'), ('Author', 'Author')], default='Adult', max_length=10),
        ),
    ]
