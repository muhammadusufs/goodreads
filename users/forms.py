from django.core.mail import send_mail
from django.forms import CharField, Form, ModelForm
from users.models import CustomUser

class UserCreation(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()

        
        return user

class UserLogin(Form):
    username = CharField(max_length=180)
    password = CharField(max_length=128)

class UpdateProfile(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_pic']
        