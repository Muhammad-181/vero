# forms.py
from django import forms
from .models import StudentProfile, Faculty, Department
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# class StudentProfileForm(forms.ModelForm):
#     class Meta:
#         model = StudentProfile
#         fields = [
#             'first_name',
#             'last_name',
#             'other_names',
#             'admission_year',
#             'department',
#             'phone_number',
#             'inst_email',
#         ]
       
        
#     def __init__(self, *args, **kwargs):
#         super(StudentProfileForm, self).__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'
#             field.required = True  # Make all fields required except the hidden one

#     def save(self, commit=True):
#         instance = super(StudentProfileForm, self).save(commit=False)
#         instance.account_completed = True  # Set account_completed to True when the form is saved
#         if commit:
#             instance.save()
#         return instance


class StudentProfileForm(forms.ModelForm):
    faculty = forms.ModelChoiceField(
        queryset=Faculty.objects.all(),
        empty_label="Select Faculty",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_faculty'})
    )

    class Meta:
        model = StudentProfile
        fields = [
            'first_name',
            'last_name',
            'other_names',
            'admission_year', 
            'faculty',
            'department', 
            'phone_number',
            'inst_email',
        ] 

    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.required = True

        self.fields['department'].queryset = Department.objects.none()
        self.fields['department'].widget.attrs['id'] = 'id_department'

        if 'faculty' in self.initial:
            try:
                faculty_id = int(self.initial['faculty'])
                self.fields['department'].queryset = Department.objects.filter(faculty_id=faculty_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.faculty:
            self.fields['department'].queryset = self.instance.faculty.department_set.all()

    def save(self, commit=True):
        instance = super(StudentProfileForm, self).save(commit=False)
        instance.account_completed = True
        if commit:
            instance.save()
        return instance 

    
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control btn bgPrimary'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfilePictureForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control btn bgPrimary'
    # profile_image = forms.ImageField(
    #     label='Change Profile Picture', 
    #     required=False, 
    #     widget=forms.FileInput(
    #         attrs={'class': 'form-control btn bgPrimary'}
    #         )
    #         )




class LoginForm(forms.Form):
    matric = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your matric no',
            'required': 'required',
        }),
        label="matric number"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'required': 'required',
        }),
        label="Password"
    )


# class RegistrationForm(forms.Form):
#     username = forms.CharField(
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Enter your username',
#             'required': 'required',
#         }),
#         label="Username"
#     )
#     email = forms.EmailField(
#         widget=forms.EmailInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Enter your email',
#             'required': 'required',
#         }),
#         label="Email"
#     )

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email=email).exists():
#             raise ValidationError("This email is already in use.")
#         return email

# forms.py

class RegisterForm(forms.Form):
    matric = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your matric number',
            'required': 'required',
        }),
        label="Matric Number"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'required': 'required',
        }),
        label="Email"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'required': 'required',
        }),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repeat your password',
            'required': 'required',
        }),
        label="Repeat Password"
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")

        return cleaned_data

    def clean_matric(self):
        matric = self.cleaned_data.get("matric")
        if User.objects.filter(username=matric).exists():
            raise ValidationError("A user with this matric number already exists")
        return matric

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists")
        return email


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'required': 'required',
        }),
        label="Email"
    )