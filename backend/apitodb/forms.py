from django import forms
from .models import Word, Result


class SearchForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = (
            'word',
            'word_type',
            'definition',
            'pos',
        )

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = (
            'resultword',
        )