from django.db import models
from django.db.models import Sum

from cohort.models import BaseModel, User

"""
Here we store copies of gitlab issues to query them more easily.
These are refreshed using celery.
"""


class GitlabIssue(BaseModel):
    iid = models.IntegerField(unique=True)
    STATE_CHOICES = [
        ('opened', 'Opened'),
        ('closed', 'Closed'),
    ]
    state = models.CharField(max_length=6, choices=STATE_CHOICES)
    labels = models.TextField()
    gitlab_created_at = models.DateTimeField()
    gitlab_updated_at = models.DateTimeField(null=True)
    gitlab_closed_at = models.DateTimeField(null=True)

    title = models.TextField()
    description = models.TextField(blank=True)

    votes_positive_sum = models.IntegerField(default=0)
    votes_neutral_sum = models.IntegerField(default=0)
    votes_negative_sum = models.IntegerField(default=0)
    votes_total_sum = models.IntegerField(default=0)


class Vote(BaseModel):
    issue = models.ForeignKey(GitlabIssue, on_delete=models.CASCADE, related_name='vote_issues')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vote_users')

    VOTE_CHOICES = [
        (1, 'Positive vote'),
        (0, 'Neutral vote'),
        (-1, 'Negative vote'),
    ]
    vote = models.IntegerField(choices=VOTE_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['issue', 'user'], name='unique_together_issue_user'),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        issue_votes = Vote.objects.filter(issue=self.issue.uuid)
        self.issue.votes_positive_sum = issue_votes.filter(vote=1).aggregate(Sum('vote'))
        self.issue.votes_neutral_sum = issue_votes.filter(vote=0).aggregate(Sum('vote'))
        self.issue.votes_negative_sum = issue_votes.filter(vote=-1).aggregate(Sum('vote'))
        self.issue.votes_total_sum = self.issue.votes_positive_sum - self.issue.votes_negative_sum
        self.issue.save()
