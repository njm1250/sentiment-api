from django.db import models

class Subreddits(models.Model):
    subreddit_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        db_table = 'subreddits'