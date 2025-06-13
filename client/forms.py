from django import forms
from .models import ClientProject

class ProjectForm(forms.ModelForm):
    status = forms.ChoiceField(  # Explicitly declare (not just in Meta)
        choices=ClientProject.STATUS_CHOICES,
        required=False  # Only if you allow blank status
    )

    class Meta:
        model = ClientProject
        fields = ['title', 'description', 'file', 'status']  # Include status

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # Hide for new projects
            self.fields.pop('status', None)