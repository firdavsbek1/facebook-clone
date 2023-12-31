# Generated by Django 4.2.4 on 2023-08-13 06:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0010_review_up_vote_review_vote_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upvotes', to='posts.review')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upvotes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DownVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='down_votes', to='posts.review')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='down_votes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='upvote',
            constraint=models.UniqueConstraint(fields=('user', 'comment'), name='OneLikeOneUpVotePerUser'),
        ),
        migrations.AddConstraint(
            model_name='downvote',
            constraint=models.UniqueConstraint(fields=('user', 'comment'), name='OneLikeOneDownVotePerUser'),
        ),
    ]
