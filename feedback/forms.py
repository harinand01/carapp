from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    rating = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)], widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
