from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit,Hidden
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    captcha=ReCaptchaField(widget=ReCaptchaV3,label='')
   

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username',
            'password',
            
            Submit('submit', 'Login', css_class='btn btn-primary mt-3')
        )





from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.core.exceptions import ValidationError
from .models import CustomUser

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    captcha=ReCaptchaField(widget=ReCaptchaV3,label='')
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password', 'SecurityQuestion', 'SecurityQuestionAnswer']
        widgets = {
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
        }
        labels = {
            'confirm_password': 'Confirm Password',
        }

        # Set required=True for all fields
        widgets = {
            field: forms.TextInput(attrs={'required': 'true'})
            for field in fields
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-8'
        self.helper.layout = Layout(
            'username',
            'email',
            'password',
            'confirm_password',
            'SecurityQuestion',
            'SecurityQuestionAnswer',
            Submit('submit', 'Sign Up', css_class='btn-primary')
        )

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        email = cleaned_data.get("email")

        existing_user = CustomUser.objects.filter(email=email).exists()
        if existing_user:
            self.add_error('email', "An account with this email already exists.")
            raise ValidationError("An account with this email already exists.")

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        min_length = 8

        try:
            if password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match")
                raise ValidationError("Passwords do not match")

            if len(password) < min_length:
                raise ValidationError("Password must be at least 8 characters long.")

            if not any(char.isupper() for char in password):
                raise ValidationError("Password must contain at least one uppercase letter.")

            if not any(char.islower() for char in password):
                raise ValidationError("Password must contain at least one lowercase letter.")

            if not any(char.isdigit() for char in password):
                raise ValidationError("Password must contain at least one digit.")
        except:
             raise ValidationError("Password fields seems empty")

        return cleaned_data

class VerifyCodeForm(forms.Form):
    code = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'class': 'form-control'}))
    captcha=ReCaptchaField(widget=ReCaptchaV3,label='')
    def __init__(self, *args, **kwargs):
                super(VerifyCodeForm, self).__init__(*args, **kwargs)
                self.helper = FormHelper()
                self.helper.form_method = 'post'
                self.helper.layout = Layout(
                    'code',
                    Submit('submit', 'Verify Code', css_class='btn btn-primary mt-3')
                )



