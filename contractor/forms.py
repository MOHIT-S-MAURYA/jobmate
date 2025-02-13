from django import forms
from .models import Job, WorkRequest

class JobCreationForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'wage', 'required_skills']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600'}),
            'wage': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600'}),
            'required_skills': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600', 'rows': 3}),
        }

class WorkRequestForm(forms.ModelForm):
    class Meta:
        model = WorkRequest
        fields = ['job', 'message']
        widgets = {
            'job': forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600'}),
            'message': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        contractor = kwargs.pop('contractor', None)
        super().__init__(*args, **kwargs)
        if contractor:
            self.fields['job'].queryset = Job.objects.filter(contractor=contractor, status='open')
            self.fields['job'].label_from_instance = lambda obj: obj.title