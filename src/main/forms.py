from django import forms


class ItemSearchForm(forms.Form):
    itemName = forms.CharField(label = "Item")
