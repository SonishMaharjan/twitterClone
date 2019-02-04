from django import forms
from .models import Tweet
from .validators import validate_content
class TweetModelForm(forms.ModelForm):
    content = forms.CharField(label="",widget=forms.Textarea(
        attrs={"placeholder":"Your message.","class":"form-control"}))

    class Meta:
        model = Tweet
        fields = ["content"]
        #exclude = ["user",]
    #use to validata data
    # def clean_(fieldName)
    # def clean_content(self):
    #     content = self.cleaned_data.get("content")
    #     print(content)
    #     if content =="abc":
    #         raise forms.ValidationError("Cannot be abc")
    #     return content
