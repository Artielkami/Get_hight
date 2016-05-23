from django import forms


class UploadForm(forms.Form):
    file = forms.FileField()


class SearchWay(forms.Form):
    departure = forms.CharField(max_length=3)
    destination = forms.CharField(max_length=3)
