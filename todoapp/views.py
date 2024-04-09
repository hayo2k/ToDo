from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import TodoList, Category


class TodoListView(ListView):
    model = Category
    template_name = 'todoapp/index.html'


class ItemListView(ListView):
    model = TodoList
    template_name = 'todoapp/category.html'

    def get_queryset(self):
        return TodoList.objects.filter(category_id=self.kwargs['list_id'])

    def get_context_data(self):
        context = super().get_context_data()
        context['category'] = Category.objects.get(id=self.kwargs['list_id'])
        return context


class ListCreate(CreateView):
    model = Category
    fields = ['name']

    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        context['name'] = 'Add new category'
        return context



class ItemCreate(CreateView):
    model = TodoList
    fields = ['category', 'title', 'content', 'end_date']

    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        category = Category.objects.get(id=self.kwargs['list_id'])
        initial_data['category'] = category
        return initial_data

    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        category = Category.objects.get(id=self.kwargs['list_id'])
        context['category'] = category
        context['title'] = 'Create a new item'
        return context

    def get_success_url(self):
        return reverse('list', args=[self.object.category_id])


class ItemUpdate(UpdateView):
    model = TodoList
    fields = ['category', 'title', 'content', 'end_date']



    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context['category'] = self.object.category
        context['name'] = 'Edit item'
        return context

    def get_success_url(self):
        return reverse('list', args=[self.object.category_id])


class ListDelete(DeleteView):
    model = Category
    success_url = reverse_lazy("index")


class ItemDelete(DeleteView):
    model = TodoList

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.object.category
        return context