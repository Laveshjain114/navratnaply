from django import forms
from .models import Inquiry


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'phone', 'product', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your full name',
                'id': 'id_name',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+91 00000 00000',
                'id': 'id_phone',
            }),
            'product': forms.Select(attrs={
                'id': 'id_product',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Describe the quantity, size, finish or anything else you need...',
                'id': 'id_message',
                'rows': 4,
            }),
        }