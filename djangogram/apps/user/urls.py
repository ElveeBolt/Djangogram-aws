from django.urls import path, include
from .views import UserDetailView, UserListView, UserSettingsView, UserLoginView, UserSignUpView, UserLogoutView, \
    UserSignupVerifySuccessView, UserSignupVerifyInvalidView, UserSignupVerifyView, UserFriendListView, UserFriendActionView

urlpatterns = [
    path('', UserListView.as_view(), name='users'),
    path('<int:pk>', UserDetailView.as_view(), name='user'),
    path('settings/', UserSettingsView.as_view(), name='user-settings'),
    path('friends/', UserFriendListView.as_view(), name='user-friends'),
    path('friends/<int:pk>/action', UserFriendActionView.as_view(), name='user-friend-action'),

    path('login/', UserLoginView.as_view(), name='login'),
    path('social-login/', include('social_django.urls', namespace='social')),
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('signup/verify/<uidb64>/<token>', UserSignupVerifyView.as_view(), name='signup-verify'),
    path('signup/verify/success', UserSignupVerifySuccessView.as_view(), name='signup-verify-success'),
    path('signup/verify/invalid', UserSignupVerifyInvalidView.as_view(), name='signup-verify-invalid'),
    path('logout', UserLogoutView.as_view(), name='logout'),
]
