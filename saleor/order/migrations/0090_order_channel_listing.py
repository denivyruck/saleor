# Generated by Django 3.1 on 2020-08-19 07:58

import django.db.models.deletion
from django.db import migrations, models
from django.utils.text import slugify


def add_channel_slug(apps, schema_editor):
    Channel = apps.get_model("channel", "Channel")
    Order = apps.get_model("order", "Order")

    channels_dict = {}

    for order in Order.objects.iterator():
        currency = order.currency
        channel = channels_dict.get(currency)

        if not channel:
            name = f"Channel {currency}"
            channel, _ = Channel.objects.get_or_create(
                currency_code=currency, defaults={"name": name, "slug": slugify(name)},
            )
            channels_dict[currency] = channel

        order.channel = channel

        order.save(update_fields=["channel"])


class Migration(migrations.Migration):

    dependencies = [
        ("channel", "0001_initial"),
        ("order", "0089_auto_20200902_1249"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="channel",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="orders",
                to="channel.channel",
            ),
        ),
        migrations.RunPython(add_channel_slug),
        migrations.AlterField(
            model_name="order",
            name="channel",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="orders",
                to="channel.channel",
            ),
        ),
        migrations.AlterField(
            model_name="order", name="currency", field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name="orderline",
            name="currency",
            field=models.CharField(max_length=3),
        ),
    ]
