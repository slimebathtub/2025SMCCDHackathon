# Generated by Django 5.2 on 2025-04-25 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0004_rename_advisors_clubinfo_advisor_email_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clubinfo',
            old_name='advisor',
            new_name='advisors',
        ),
        migrations.RenameField(
            model_name='clubinfo',
            old_name='advisor_email',
            new_name='advisors_email',
        ),
    ]
