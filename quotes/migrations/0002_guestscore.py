# Generated by Django 4.2.5 on 2023-10-02 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuestScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('book_quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quotes.bookquote')),
                ('user_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sessions.session')),
            ],
        ),
    ]
