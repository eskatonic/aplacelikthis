from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    # widget overrides the default HTML (input) element:
    comments = forms.CharField(required=False, widget=forms.Textarea)