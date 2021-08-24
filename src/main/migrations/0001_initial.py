# Generated by Django 2.2.20 on 2021-04-26 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('EveAssets', '0002_auto_20210426_0216'),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('salesTax', models.FloatField()),
                ('brokersFee', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.Character')),
            ],
        ),
        migrations.CreateModel(
            name='MarketPriceEstimator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrackingListTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('orderCount', models.IntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Character')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EveAssets.Station')),
            ],
        ),
        migrations.CreateModel(
            name='TrackingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('orderCount', models.IntegerField()),
                ('template', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.TrackingListTemplate')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TrackedItemTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EveAssets.Item')),
                ('trackingListTemplate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='main.TrackingListTemplate')),
            ],
        ),
        migrations.CreateModel(
            name='TrackedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EveAssets.Item')),
                ('trackingList', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.TrackingList')),
            ],
        ),
        migrations.CreateModel(
            name='NaiveIndustryEstimate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instalationCost', models.DecimalField(decimal_places=2, max_digits=30)),
                ('marketPrice', models.DecimalField(decimal_places=2, max_digits=30)),
                ('quantityInStock', models.IntegerField(default=0)),
                ('quantityProducing', models.IntegerField(default=0)),
                ('maxDailyProduction', models.IntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EveAssets.Item')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Character')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EveAssets.Station')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='main.Inventory')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EveAssets.Item')),
            ],
        ),
    ]
