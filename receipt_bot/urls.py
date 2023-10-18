from django.contrib import admin
from django.urls import path
from assistant.views import active_contracts
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', active_contracts, name='active_contracts'),
    # path('generate_receipt/<int:contract_id>/', generate_receipt, name='generate_receipt'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
