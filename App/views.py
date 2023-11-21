from django.urls import reverse_lazy
from .models import Task
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here


class Login(LoginView):
    template_name = "App/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("list")


class Register(FormView):
    template_name = "App/register.html"
    redirect_authenticated_user = True
    form_class = UserCreationForm
    success_url = reverse_lazy("list")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("list")
        return super(Register, self).get(*args, **kwargs)


class Logout(LogoutView):
    next_page = "login"


class List(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "TODO"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["TODO"] = context["TODO"].filter(user=self.request.user)
        context["Count"] = context["TODO"].filter(complete_status=False).count()

        search_value = self.request.GET.get("search") or ""
        if search_value:
            context["TODO"] = context["TODO"].filter(title__icontains=search_value)
        context["search_value"] = search_value
        return context


class Detail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "Task"
    template_name = "App/detail.html"


class Create(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "description", "complete_status"]
    template_name = "App/create.html"
    success_url = reverse_lazy("list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Create, self).form_valid(form)


class Update(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["title", "description", "complete_status"]
    template_name = "App/update.html"
    success_url = reverse_lazy("list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Update, self).form_valid(form)


class Delete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "Task"
    template_name = "App/delete.html"
    success_url = reverse_lazy("list")
