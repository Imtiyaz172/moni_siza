# Generated by Django 2.0.3 on 2021-09-22 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0009_auto_20210823_1225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='written',
            name='image',
        ),
        migrations.AddField(
            model_name='written',
            name='pdf',
            field=models.FileField(blank=True, upload_to='pdf/'),
        ),
        migrations.AlterField(
            model_name='written',
            name='ans',
            field=models.FileField(blank=True, upload_to='ans/'),
        ),
    ]
