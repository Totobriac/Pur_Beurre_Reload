# Generated by Django 3.0.5 on 2020-04-20 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finder', '0002_product_off_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='product',
            name='nutrition_grade',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='picture',
            field=models.URLField(max_length=2000),
        ),
    ]
