# Generated by Django 2.0.3 on 2021-10-21 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0018_auto_20211021_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='board_on_year',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blogapp.subject'),
        ),
    ]
