# Generated by Django 2.0.3 on 2021-10-21 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0019_board_on_year_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board_on_year',
            name='subject',
        ),
        migrations.AddField(
            model_name='prev_year_ques',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blogapp.subject'),
        ),
    ]
