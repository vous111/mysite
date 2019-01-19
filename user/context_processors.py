# 自定义context_processors
from .forms import LoginForm


def login_modal_form(request):
    return {'login_modal_form': LoginForm()}
