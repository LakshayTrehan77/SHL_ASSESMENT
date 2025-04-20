from django.urls import path
from .views import HealthCheckView, RecommendView

app_name = 'recommend_api'

urlpatterns = [
    # GET  /api/health/      → HealthCheckView
    path('api/health/',    HealthCheckView.as_view(),   name='health'),
    # POST /api/recommend/   → RecommendView
    path('api/recommend/', RecommendView.as_view(),    name='recommend'),
]
