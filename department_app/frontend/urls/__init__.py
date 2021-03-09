from .departments_urls import urlpatterns as dep_urls
from .employees_urls import urlpatterns as emp_urls

urlpatterns = [
    *dep_urls,
    *emp_urls,
]
