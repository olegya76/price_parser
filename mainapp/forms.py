from django import forms


class RozetkaForm(forms.Form):
    searchField = forms.CharField(label = 'Поиск')


class SearchForm(forms.Form):
    searchField = forms.CharField(label = 'Поиск')
