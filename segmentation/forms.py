#-*-coding:utf-8-*-
from django import forms

FILE_SIZE_LIMIT = 400  # KB


class segForm(forms.Form):
    box = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'style': 'width:500px'}),
        label=("Input any sentence or text"))
    upload_file = forms.FileField(
        required=False,
        label=("Or upload a text file (optional)"),
        help_text="File size limit: %d KB" %
        FILE_SIZE_LIMIT)

    def clean_upload_file(self):
        file_size_limit = FILE_SIZE_LIMIT * 1024
        upload_file = self.cleaned_data['upload_file']
        if upload_file is None:
            return upload_file
        if upload_file.content_type != 'text/plain':
            raise forms.ValidationError('You have to upload a text file')

        if upload_file.size > file_size_limit:
            raise forms.ValidationError(
                'Please keep the file size under %d KB. Current size is %.1f KB.' %
                (FILE_SIZE_LIMIT, upload_file.size / 1000.0))
        box = ''
        for chunk in upload_file.chunks():
            box += chunk
        try:
            box.decode('utf-8')
        except BaseException:
            raise forms.ValidationError('File should be encoded in utf-8')
        return box
