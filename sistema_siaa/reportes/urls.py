from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_reportes, name='lista_reportes'),
    path('nuevo/', views.crear_reporte, name='crear_reporte'),
    path('alumno/<int:alumno_id>/', views.detalle_alumno, name='detalle_alumno'),
    path('eliminar/<int:id>/', views.eliminar_reporte, name='eliminar_reporte'),
]