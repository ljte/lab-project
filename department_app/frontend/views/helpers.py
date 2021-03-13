from django.contrib import messages


def errors_occurred(request, response):
    if not response.ok:
        messages.error(request, response.json().get("message"))
        return True
    return False
