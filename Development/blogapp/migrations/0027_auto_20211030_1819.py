# Generated by Django 2.0.3 on 2021-10-30 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0026_auto_20211030_1658'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classes_on_year',
            old_name='year',
            new_name='years',
        ),
    ]
