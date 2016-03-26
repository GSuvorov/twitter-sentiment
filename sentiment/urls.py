from django.conf.urls import url

from . import views

urlpatterns = [
	url(r"^$", views.page_index, name="index"),
	url(r"^result/$", views.page_result, name="result"),
	url(r"^details/$", views.page_details, name="details"),
]