from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='summary_short',
            field=models.TextField(blank=True, null=True),
        ),
    ]
