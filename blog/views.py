from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify
from blog.models import Blog


class BlogCreateView(PermissionRequiredMixin, CreateView):
    """Класс создания статьи блога"""
    model = Blog
    permission_required = 'blog.add_blog'
    fields = ('title', 'content', 'preview', 'is_published',)
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(PermissionRequiredMixin, UpdateView):
    """Класс редактирования статьи блога"""
    permission_required = 'blog.change_blog'
    model = Blog
    fields = ('title', 'content', 'preview', 'is_published',)

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:blogs', args=[self.kwargs.get('pk')])


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    """Класс удаления статьи блога"""
    permission_required = 'blog.delete_blog'
    model = Blog
    success_url = reverse_lazy('blog:list')


class BlogListView(ListView):
    """Класс просмотра списка статей блога"""
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    """Класс просмотра статьи блога"""
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object