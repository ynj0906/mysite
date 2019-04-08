from django.conf.urls import url
from . import views
from django.urls import path, include, re_path
from .views import ItemFilterView, ItemDetailView, ItemCreateView, ItemUpdateView, ItemDeleteView, AddTagView, TagView
app_name = "accounts"

urlpatterns =[

    path('', ItemFilterView.as_view(), name='index'),
    path('create', ItemCreateView.as_view(), name='create'),
    path('detail/<int:pk>/', ItemDetailView.as_view(), name='detail'),


    path('update/<int:pk>/', ItemUpdateView.as_view(), name='update'),
    # 削除画面
    path('delete/<int:pk>/', ItemDeleteView.as_view(), name='delete'),
    path('add_tag', AddTagView.as_view(), name='add_tag'),
    path('tag/<int:pk>', TagView.as_view(), name='tag'),
    path('signup/', views.SignupView.as_view(), name='signup'),

    path("hello/", views.Hello.as_view(), name="hello"),


    #url(r"^/%", views.LoginView.as_view(), name="context")
]