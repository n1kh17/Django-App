from django.urls import path
from .views.users import UserAPI
from .views.accounts import AccountAPI
from .views.views import users_view, accounts_view

urlpatterns = [
    # ✅ API Endpoints
    path('api/users/', UserAPI.as_view()),  
    path('api/users/<int:user_id>/', UserAPI.as_view()),  
    path('api/accounts/', AccountAPI.as_view()),  
    path('api/accounts/<int:account_id>/', AccountAPI.as_view()),  

    # ✅ Frontend Views (For Web UI)
    path('users/', users_view, name='users'),  
    path('accounts/', accounts_view, name='accounts'),  
]
