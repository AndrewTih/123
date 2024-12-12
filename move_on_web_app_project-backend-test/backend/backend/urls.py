"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from backend import settings
from django.conf.urls.static import static
from move_on.views import get_energy, tasks_complete, WalkViewSet, get_statistics, log_js_errors, check_unfinished, \
    main_page, get_tasks, stepometer, claim_daily_bonus, streak_history, global_statistics
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.urls import get_resolver


schema_view = get_schema_view(
    openapi.Info(
        title="MoveOn API",
        default_version='v1',
        description="API для управления прогулками, заданиями и статистикой.",
    ),
    public=True,
)

router = DefaultRouter()
router.register(r'walks', WalkViewSet, basename='walk')


urlpatterns = [
    path('', main_page, name='main_page'),
    path('admin/', admin.site.urls),
    path('energy/<int:telegram_id>/', get_energy, name='get_energy'),
    path('tasks/', get_tasks, name='get_tasks'),
    path('tasks/<int:task_id>/complete/', tasks_complete, name='tasks_complete'),
    path('streak/history/<int:telegram_id>/', streak_history, name='streak_history'),
    path('bonus/claim/<int:telegram_id>/', claim_daily_bonus, name='claim_daily_bonus'),
    # path('stepometer/', stepometer, name='stepometer'),
    path('statistics/<int:telegram_id>/', get_statistics, name='get_statistics'),
    path('global-statistics/<int:telegram_id>/', global_statistics, name='global_statistics'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs.<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-formatted'),
    path('webapp-test/', TemplateView.as_view(template_name='webapp_test.html')),
    path('api/walk/check_unfinished/', check_unfinished, name='check_unfinished'),
    path('log_js_errors/', log_js_errors, name='js_logs_view'),
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)