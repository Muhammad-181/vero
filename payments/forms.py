# forms.py
from django import forms
from .models import Fee, FeeAmount, Level, Payment

# class PaymentForm(forms.Form):
#     fee = forms.ModelChoiceField(queryset=Fee.objects.all(), empty_label="Select Fee")


# class PaymentForm(forms.Form):
#     fee = forms.ModelChoiceField(
#         queryset=Fee.objects.all(),
#         empty_label="Select Fee",
#         widget=forms.Select(attrs={
#             'class': 'form-control form-control-sm', 
#             'autocomplete': 'on',
#             'id': 'demo-foo-search',
#             }),  # Set attrs directly in the widget
#     )



class PaymentForm(forms.ModelForm):
    fee = forms.ModelChoiceField(
        queryset=Fee.objects.all(),
        empty_label="Select Fee",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_fee'})
    )
    level = forms.ModelChoiceField(
        queryset=Level.objects.none(),  # Initially empty
        empty_label="Select Level",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_level'})
    )

    class Meta:
        model = Payment
        fields = ['fee', 'level']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'fee' in self.data:  # Check if fee is selected in the request data
            try:
                fee_id = int(self.data.get('fee'))
                self.fields['level'].queryset = Level.objects.filter(feeamount__fee_id=fee_id).distinct()
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:  # Check if the form is bound to an existing instance
            self.fields['level'].queryset = self.instance.fee.feeamount_set.all().values_list('level', flat=True)




# class PaymentForm(forms.ModelForm):
#     class Meta:
#         model = Fee
#         fields = [
#                 'name', 
#                   'amount', 
                  
#                   ]
        
        
#     def __init__(self, *args, **kwargs):
#         super(PaymentForm, self).__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'

