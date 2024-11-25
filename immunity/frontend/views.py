from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from user_api.models import *


class LoginPageView(LoginView):
    """
    Переопределение страницы авторизации.
    """

    redirect_authenticated_user = True


class DashBoardPageView(TemplateView):
    """
    Отображение страницы дашборда в корне веб-приложения.
    """

    template_name = "pages/dashboard.html"

    def get_context_data(self, **kwargs):
        """
        Инициализация переменных в контексте по умолчанию.
        """

        context = super().get_context_data(**kwargs)

        # context['navbar_user_global_object'] = self.request.user

        return context


class ApplicationPageView(TemplateView):
    """
    Отображение списка приложений.
    """

    template_name = "pages/applications.html"

    def get_context_data(self, **kwargs):
        """
        Инициализация переменных в контексте по умолчанию.
        """

        context = super().get_context_data(**kwargs)

        context["applications"] = Application.objects.filter(
            user=self.request.user
        ).order_by("created_at")

        return context


class ApplicationDetailPageView(DetailView):
    """
    Отображение конкретного приложения.
    """

    template_name = "pages/application_detail.html"
    model = Application
    slug_field = "id"

    def get_context_data(self, **kwargs):
        """
        Инициализация переменных в контексте по умолчанию.
        """

        context = super().get_context_data(**kwargs)

        context["application"] = Application.objects.get(id=self.kwargs["slug"])

        context_list = Context.objects.filter(
            application=context["application"]
        ).order_by("created_at")
        control_flows = ControlFlow.objects.filter(context__in=context_list)

        context["requests"] = Request.objects.filter(context__in=context_list)
        context["responses"] = Response.objects.filter(context__in=context_list)
        context["code"] = CodeExecution.objects.filter(control_flow__in=control_flows)
        context["errors"] = Error.objects.filter(control_flow__in=control_flows)

        return context
