from django import forms
from django.contrib.auth.hashers import make_password
from .models import Users

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Create a password"}),
        min_length=8, label="Password (min. 8 characters)"
    )
    class Meta:
        model = Users
        fields = ["account_number","name","phone_number","password","amount","gender","age","dob","address"]
        widgets = {
            "account_number": forms.TextInput(attrs={"class":"form-control","placeholder":"Account number","maxlength":"18"}),
            "name": forms.TextInput(attrs={"class":"form-control","placeholder":"Full name"}),
            "phone_number": forms.TextInput(attrs={"class":"form-control","placeholder":"Phone number"}),
            "amount": forms.NumberInput(attrs={"class":"form-control","min":"0","step":"0.01"}),
            "gender": forms.Select(attrs={"class":"form-control"}),
            "age": forms.NumberInput(attrs={"class":"form-control","min":"18","max":"120"}),
            "dob": forms.DateInput(attrs={"class":"form-control","type":"date"}),
            "address": forms.Textarea(attrs={"class":"form-control","rows":3,"placeholder":"Address"}),
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        raw_password = self.cleaned_data.get("password")
        if raw_password:
            user.password = make_password(raw_password)
        if commit:
            user.save()
        return user
