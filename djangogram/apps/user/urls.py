from django.urls import path
from .views import UserDetailView, UserListView, UserSettingsView, UserLoginView, UserSignUpView, UserLogoutView, \
    UserSignupVerifySuccessView, UserSignupVerifyInvalidView, UserSignupVerifyView

urlpatterns = [
    path('', UserListView.as_view(), name='users'),
    path('<int:pk>', UserDetailView.as_view(), name='user'),
    path('settings/', UserSettingsView.as_view(), name='user-settings'),

    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('signup/verify/<uidb64>/<token>', UserSignupVerifyView.as_view(), name='signup-verify'),
    path('signup/verify/success', UserSignupVerifySuccessView.as_view(), name='signup-verify-success'),
    path('signup/verify/invalid', UserSignupVerifyInvalidView.as_view(), name='signup-verify-invalid'),
    path('logout', UserLogoutView.as_view(), name='logout'),
]
