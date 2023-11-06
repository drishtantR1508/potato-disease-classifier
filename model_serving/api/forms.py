from django import forms

class UploadImageForm(forms.Form):
    image = forms.ImageField()
    class Meta():
        
        fields=('image')
        widgets={
            'image':forms.FileInput(attrs={'class':"form-control img zoom"}),
            
        }
