# Generated by Django 3.0.5 on 2020-04-29 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finder', '0006_savedproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='savedproduct',
            name='product_off_id',
        ),
        migrations.AddField(
            model_name='savedproduct',
            name='saved_product',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='finder.Product'),
        ),
    ]
