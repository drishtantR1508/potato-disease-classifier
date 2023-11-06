from django.urls import path,include
from . import views
urlpatterns = [
    path('predict',views.PredictAPIView.as_view())
]