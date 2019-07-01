from django.urls import path
from django.conf.urls import url
from simulator import views
from .views import start_simul


urlpatterns = [
    url(r'^start_simul/$', start_simul, name='start-simul')
]
