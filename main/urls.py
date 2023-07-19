from django.urls import path

from main.apps import MainConfig
from main.views import contacts, ProductDetailView, ProductListView, BlogListView, BlogDetailView, BlogCreateView, \
    BlogUpdateView, BlogDeleteView, toggle_activity

app_name = MainConfig.name


urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('contacts/', contacts, name='contacts'),
    path('<int:pk>/product/', ProductDetailView.as_view(), name='product'),
    path('blog/', BlogListView.as_view(), name='list'),
    path('<int:pk>/veiw/', BlogDetailView.as_view(), name='view'),
    path('blog/create/', BlogCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
    path('activity/<int:pk>/', toggle_activity, name='toggle_activity'),
]
