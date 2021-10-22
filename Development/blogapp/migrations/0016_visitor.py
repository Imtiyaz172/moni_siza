# Generated by Django 2.0.3 on 2021-10-13 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0015_auto_20211013_2229'),
    ]

    operations = [
        migrations.CreateModel(
            name='visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(blank=True, default=0)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Visitor',
                'verbose_name_plural': 'Visitor',
            },
        ),
    ]