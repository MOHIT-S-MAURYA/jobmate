from django import forms
from .models import Skill, WorkerSkill

class WorkerSkillForm(forms.Form):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-checkbox h-5 w-5 text-blue-600'
        }),
        required=False
    )

    def __init__(self, *args, **kwargs):
        worker = kwargs.pop('worker', None)
        super().__init__(*args, **kwargs)
        if worker:
            self.fields['skills'].initial = worker.skills.all()