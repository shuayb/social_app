from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm

# For Image
from PIL import Image
import sys
from io import BytesIO
from uuid import uuid4
from django.core.files.uploadedfile import InMemoryUploadedFile

User = get_user_model()


class UserAuthenticationForm(AuthenticationForm):
    # Todo add captcha
    # captcha = ReCaptchaField(attrs={
    #     'theme': 'clean',
    # })
    # For django its username because the user
    # model considers email as login username
    def clean_username(self):
        cd = self.cleaned_data
        return cd['username'].lower()

    error_messages = {
        'invalid_login': "Please enter a correct %(username)s and password.",
        'inactive': "This account is inactive."
    }


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput,
                               # min_length=8,
                               )

    password2 = forms.CharField(label='Repeat Password',
                                widget=forms.PasswordInput,
                                # min_length=8,
                                )

    class Meta:
        model = get_user_model()
        fields = ('email', 'username')

    def clean(self):
        super(UserRegistrationForm, self).clean()

        try:
            dummy = self.cleaned_data['password']
            dummy = self.cleaned_data['password2']
        except KeyError:
            raise forms.ValidationError("")

        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')

        if cd['password'] == cd['username']:
            raise forms.ValidationError('Password can\'t be same as username.')

        return self.cleaned_data

    def clean_password2(self):
        cd = self.cleaned_data
        password_validation.validate_password(self.cleaned_data.get('password2'))
        return cd['password2']

    def clean_password(self):
        cd = self.cleaned_data
        password_validation.validate_password(self.cleaned_data.get('password'))
        return cd['password']

    def clean_username(self):
        cd = self.cleaned_data
        return cd['username'].lower()

    def clean_email(self):
        cd = self.cleaned_data
        return cd['email'].lower()


class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',
                  'name',
                  'email',
                  'bio',
                  'website',
                  'location',
                  'avatar')  # Note that we didn't mention user field here.

        widgets = {
            'avatar': forms.FileInput(attrs={
                'accept': 'image/*',  # TODO this is not an actual validation! don't rely on that!
                'id': 'id_avatar'
            })
        }

    def clean_avatar(self):
        image_field = self.cleaned_data.get('avatar')
        # Fixing name
        # image_field.name = '{}.{}'.format(uuid4().hex,
        #                                   image_field.name.split('.')[1])

        if image_field:
            image = Image.open(image_field).convert('RGB')
            w, h = image.size
            # Divide the image by half, if it is too large
            # Todo: Use a client-side image resizer
            if w > 1000 or h > 1000:
                image = image.resize((int(w / 2), int(h / 2)), Image.ANTIALIAS)
                output = BytesIO()

                # Save the new image output
                image.save(output, format='JPEG', quality=80)
                output.seek(0)

                # change imagefield to newly modified
                image_field = InMemoryUploadedFile(output,
                                                   'ImageField', "%s.jpg" % image_field.name.split('.')[0],
                                                   'image/jpeg',
                                                   sys.getsizeof(image),
                                                   None)
                return image_field
            else:
                return image_field

    # def save(self, user=None):
    #     pass
    #     user_profile = super(UpdateUserProfileForm, self).save(commit=False)
    #     if user:
    #         user_profile.user = user
    #     user_profile.save()
    #     return user_profile
