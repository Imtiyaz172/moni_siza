# Generated by Django 2.0.3 on 2021-10-31 05:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0028_user_answer_mark'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_mark_count',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(default=0)),
                ('status', models.BooleanField(default=False)),
                ('subjectchapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogapp.subjectchapter')),
                ('user_reg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogapp.user_reg')),
            ],
            options={
                'verbose_name': 'user_mark_count',
                'verbose_name_plural': 'user_mark_count',
            },
        ),
    ]