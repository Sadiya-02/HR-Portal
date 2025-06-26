from django import forms
from .models import ClientProject

class ProjectForm(forms.ModelForm):
    status = forms.ChoiceField(  
        choices=ClientProject.STATUS_CHOICES,
        required=False  
    )

    class Meta:
        model = ClientProject
        fields = ['title', 'description', 'file', 'status']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  
            self.fields.pop('status', None)