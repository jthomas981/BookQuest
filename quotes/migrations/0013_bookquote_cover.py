# Generated by Django 4.2.5 on 2023-11-11 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0012_guestscore_duration_savedscores_durations_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookquote',
            name='cover',
            field=models.ImageField(blank=True, default='default.png', upload_to=''),
        ),
    ]
