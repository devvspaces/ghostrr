# Generated by Django 3.1.5 on 2021-02-02 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210201_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='sentence',
            field=models.TextField(),
        ),
    ]