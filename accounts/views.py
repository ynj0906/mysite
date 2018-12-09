from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from .models import Item, Tag
from .forms import ItemForm, TagForm, SignupForm
from django.urls import reverse_lazy

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, DetailView
from datetime import datetime
from django_filters.views import FilterView
from .filters import ItemFilter
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.views.generic import Createview

# Create your views here.
class SignupView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class Hello(View):
    def get(self,request):
        context = {"message": "helloWorld"}
        times = datetime.now()
        time = {"time": times}
        return TemplateResponse(request, "hello.html", time)

hello = Hello.as_view()


class AddTagView(CreateView):

    model = Item
    form_class = TagForm
    success_url = reverse_lazy('accounts:create')


class TagView(ListView):
    model = Item
    form_class = TagForm

    def get_queryset(self):
        queryset = Item.objects.all().filter(tag__pk=self.kwargs['pk'])
        return queryset

class ItemFilterView(LoginRequiredMixin, FilterView):
    model = Item
    filterset_class = ItemFilter
    template_name = "accounts/item_filter.html"

    # デフォルトの並び順を新しい順とする
    queryset = Item.objects.all().order_by('-created_at')


    # クエリ未指定の時に全件検索を行うために以下のオプションを指定（django-filter2.0以降）
    strict = False

    # pure_pagination用設定
    paginate_by = 2
    object = Item

    # 検索条件をセッションに保存する or 呼び出す
    def get(self, request, **kwargs):
        if request.GET:
            request.session['query'] = request.GET
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)

index = ItemFilterView.as_view()


# 詳細画面
class ItemDetailView( LoginRequiredMixin, DetailView):
    model = Item

detail = ItemDetailView.as_view()

# 登録画面
class ItemCreateView(LoginRequiredMixin,CreateView):
    model = Item
    form_class = ItemForm
    template_name = "accounts/item_form.html"
    success_url = reverse_lazy("accounts:index")

create = ItemCreateView.as_view()



# 更新画面
class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('accounts:index')

update = ItemUpdateView.as_view()





class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('accounts:index')

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

delete = ItemDeleteView.as_view()



"""
class LoginView(View):
    def get(self, request):
        context = {"form": LoginForm()}
        return render(request, "account/login.html", context)

    def post(self, request):
        #リクエストからのフォームを生成
        form = LoginForm(request.POST)
        #バリデーション（ユーザーの認証も泡あせて実施）
        if not form.is_valid():
            return render(request, "accounts/login.html", context)

        #オブジェクトをフォームから取得
        user = form.get_user()

        #ログイン処理（取得したUserオブジェクトをセッションに保存＆userデータを更新）
        auth_login(request, user)

        return redirect(reverse(""))
loginview = LoginView.as_view()
"""