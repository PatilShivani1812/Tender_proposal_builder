# proposals/forms.py
from django import forms
from .models import Proposal, Section
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ['title', 'companyName', 'proposalSummary', 'projectPlanning', 'financing', 'contactName', 'contactEmail', 'contactPhoneNo']

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['proposal','name', 'order']