# Generated by Django 2.2.7 on 2019-12-02 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20191130_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blogtypename',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='blog_blog', to='blog.BlogType'),
        ),
    ]
