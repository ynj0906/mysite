from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from django.core import validators

# Create your models here


class CustomUserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self,email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser')is not True:
            raise ValueError('Superuser must have is_superuser=True')


class CustomUser(AbstractUser):
    class Meta(AbstractUser.Meta):
        db_table = "custom_user"

    email = models.EmailField('メールアドレス', unique=True)
    age = models.IntegerField("年齢", blank=True, null=True)

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS =[]

    objects = CustomUserManager()


class Category(models.Model):
    category = models.CharField(
        verbose_name="カテゴリー",
        max_length=200,
        null=True,
    )

    def __str__(self):
        return self.category


class Tag(models.Model):

    name = models.CharField('タグ', max_length=30)


    def __str__(self):
        return self.name



class Item(models.Model):


    SEX_CHOICES = (
        (1, '男性'),
        (2, '女性'),
    )

    name = models.CharField(
        verbose_name='名前',
        max_length=200,
    )
    age = models.IntegerField(
        verbose_name='年齢',
        validators=[validators.MinValueValidator(1)]
    )
    sex = models.IntegerField(
        verbose_name='性別',
        choices=SEX_CHOICES,
        default=1
    )
    memo = models.TextField(
        verbose_name='備考',
        max_length=300,
        blank=True
    )

    photo = models.ImageField(
        verbose_name="フォト",
        blank = True,
        null=True
    )

    aa=models.CharField(
        verbose_name='てすと',
        max_length=200,
        null=True

    )

    created_at = models.DateTimeField(
        verbose_name='登録日',
        auto_now_add=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True
    )

    tag = models.ManyToManyField(
        Tag,
        verbose_name="たぐ",
        null=True

    )





    # 以下は管理サイト上の表示設定
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'アイテム'
        verbose_name_plural = 'アイテム'
