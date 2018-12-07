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
    class FileFieldForm(forms.Form):
        file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


    class Meta:
        model = Item
        fields = ('name', 'age', 'sex', 'memo', 'tag', 'photo')
        widgets = {
                    'name': forms.TextInput(attrs={'placeholder':'記入例：山田　太郎'}),
                    'age': forms.NumberInput(attrs={'min':1}),
                    'sex': forms.RadioSelect(),
                    'memo': forms.Textarea(attrs={'rows':4}),

                  }
    def save(self, commit=True):
            # 全てのアップロードファイルを取得
            upload_files = self.files.getlist('file')

            # このモデルフォーム自体は、あくまで1つのモデルインスタンスと紐づきます。
            # アップロードされたファイルのうち、どれか1つをフォームに紐づけつつ
            # 残りのファイルは今ここでUploadFile.objects.createで作成する。
            self.instance.file = upload_files[0]
            other_files = upload_files[1:]
            for file in other_files:
                Item.objects.create(file=file)  # 残りのファイル作成
            return super().save(commit)