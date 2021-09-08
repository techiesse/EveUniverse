from django import forms

from .models import Blueprint

class ItemSearchForm(forms.Form):
    itemName = forms.CharField(label = "Item")


class BlueprintSearchForm(forms.Form):
    searchTerm = forms.CharField(label = "Blueprint Name")


class BlueprintForm(forms.ModelForm):
    class Meta:
        model = Blueprint
        fields = [
            'item',
            'runOutputCount',
            'runCicleTime',
            'maxProductionLimit',
        ]
