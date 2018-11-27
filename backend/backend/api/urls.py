from django.conf.urls import url, include

import backend.api.views as views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'company', views.CompanyInfo, basename='company')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'search', views.SearchSymbol.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
