from django.urls import path
from . import views

urlpatterns = [
    path("", views.endpoints),
    path("advocates/", views.advocate_list, name="advocates"),
    # path("advocates/<str:username>/", views.AdvocateDetail.as_view()),
    path("advocates/<str:username>/", views.advocate_detail),
    path("companies/", views.company_list),
]
