# Generated by Django 5.1.6 on 2025-02-21 07:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={},
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('subject', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('image', models.ImageField(upload_to='courses/%Y/%m/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='courses.category')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
