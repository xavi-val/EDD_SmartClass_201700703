"""Fase2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from Fase2.views import *
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', home_page),
    path('admin/', admin.site.urls),
    path('carga/', cargaMasiva),
    path('pruebas/',pruebas),
    path('reporte/',reportes),
    path('estudiante/',crud_estudiantes),
    path('recordatorios/',crud_recordatorios),
    path('cursosEstudiantes/',crud_cursosEstudiante),
    path('cursosPensum/',crud_cursosPensum),
    path('prerequisito/',pre_requisitos),
    path('graficarApuntes/',graficar_apuntes),
    path('crearApuntes/',agregar_apunte),
    path('verApuntes/',ver_apunte),
]
