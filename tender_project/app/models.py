from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Proposal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you want to associate proposals with users
    proposal_id = models.AutoField(primary_key=True) # Unique constraint to ensure each proposal has a unique ID
    title = models.CharField(max_length=255)
    companyName = models.CharField(max_length=255)
    proposalSummary = models.TextField(max_length=1500)
    projectPlanning = models.TextField(max_length=2200)
    financing = models.TextField(max_length=2550)
    contactName = models.CharField(max_length=255)
    contactEmail = models.EmailField()
    contactPhoneNo = models.CharField(max_length=20)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Section(models.Model):
    proposal = models.ForeignKey(Proposal, related_name='sections', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    order = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.proposal.title}"

