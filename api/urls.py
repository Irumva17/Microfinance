from django.urls import include, path
from rest_framework import routers
from api.views import MicrofinanceViewSet

router = routers.DefaultRouter()
router.register(r'microfinances', MicrofinanceViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]