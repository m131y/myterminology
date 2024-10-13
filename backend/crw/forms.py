from django import forms
from .models import Search_list
from .models import dict

class SearchForm(forms.ModelForm):
    class Meta:
        model = Search_list
        fields = (
            'id',
            'search_word',
            'search_pos',
        )

class dictForm(forms.ModelForm):
    class Meta:
        model = dict
        fields = (
            'id',
            'title',
            'description',
            'description2',
            'original_word',
            'korean_word',
            'synonym',
            'translations',
            'word_level',
        )
