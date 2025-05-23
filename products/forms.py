from django import forms
from .models import ProductReview


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} Stars')
                                                 for i in range(1, 6)]),
            'review_text': forms.Textarea(attrs={'rows': 3}),
        }
