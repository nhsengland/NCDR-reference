# Generated by Django 2.1.7 on 2019-02-15 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("ncdr", "0005_create_first_version")]

    operations = [
        migrations.AddField(
            model_name="database",
            name="version",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="databases",
                to="ncdr.Version",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="user",
            name="current_version",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="ncdr.Version",
            ),
        ),
    ]
