# Generated by Django 4.0.4 on 2022-12-24 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_product_author_product_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Availability',
            field=models.CharField(choices=[('Còn Hàng', 'Còn Hàng'), ('Hết Hàng', 'Hết Hàng')], max_length=100, null=True),
        ),
    ]
