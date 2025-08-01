from django.urls import path

from .views import user_detail_view, user_redirect_view, user_update_view, CustomTokenObtainPairView, GoogleLoginView

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('auth/google/', GoogleLoginView.as_view(), name='google_login'),
]
