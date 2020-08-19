from django import forms


# class HomeForm(forms.ModelForm):
#     def __str__(self):
#         return self.fields
#
#     class Meta:
#         model = HomeModel
#         fields = [
#             'name',
#         ]
#         labels = {
#             'name': ''
#         }
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'textfield1'})
#         }


class ProductForm(forms.Form):
    title = forms.CharField(label='Title No', max_length=20,
                            widget=forms.TextInput(attrs={
                                'placeholder': "Enter Product title"
                            }))
    describe = forms.CharField(required=False, initial="No describe",
                               widget= forms.Textarea(attrs={
                                   'rows': 10,
                                   'cols': 20
                               }))
    price = forms.DecimalField(initial=00.00)

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if "abc" in title:
            return title
        else:
            raise forms.ValidationError('Title Not entered')