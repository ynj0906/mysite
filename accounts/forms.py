from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Item, Tag, CustomUser


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username','email')


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)


class ItemForm(forms.ModelForm):



    class Meta:
        model = Item
        fields = ('name', 'age', 'sex', 'memo', 'tag', 'photo')
        widgets = {
                    'name': forms.TextInput(attrs={'placeholder':'記入例：山田　太郎'}),
                    'age': forms.NumberInput(attrs={'min':1}),
                    'sex': forms.RadioSelect(),
                    'memo': forms.Textarea(attrs={'rows':4}),

                  }