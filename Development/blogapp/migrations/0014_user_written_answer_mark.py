# Generated by Django 2.0.3 on 2021-10-13 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0013_auto_20211003_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_written_answer',
            name='mark',
            field=models.FloatField(blank=True, default=0),
        ),
    ]