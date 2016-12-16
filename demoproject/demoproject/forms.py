# -*- coding: utf-8 -*-

from django import forms


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    
class FileListForm(forms.Form):
    file_id = forms.CharField(
        label='Select a file'
    )    
    