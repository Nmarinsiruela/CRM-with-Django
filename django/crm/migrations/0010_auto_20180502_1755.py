# Generated by Django 2.0.4 on 2018-05-02 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0009_auto_20180502_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='photo',
            field=models.ImageField(default='img_folder/default.png', help_text='Optional', upload_to='img_folder/'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='surname',
            field=models.CharField(max_length=50),
        ),
    ]