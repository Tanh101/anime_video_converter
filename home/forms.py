from django import forms

class UploadForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'hidden'}))

    def clean_file(self):
        file = self.cleaned_data['file']
        allowed_content_types = ['video/mp4', 'video/mov']

        if file:
            if file.content_type not in allowed_content_types:
                raise forms.ValidationError('File type is not supported. Only mp4 and mov are supported.')

            if file.size > 100000000:  # 100 MB
                raise forms.ValidationError('File too large. Size should not exceed 100 MB.')

        return file

