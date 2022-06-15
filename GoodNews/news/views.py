from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# импорт дженериков для представлений: Список обьектов, один объект, создание, редактирование и удаление объекта
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# импорт миксина для проверки аутентификации
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

from .forms import PostForm
from .models import Post, Category  # импорт нашей модели
from .filters import PostFilter  # импорт нашего фильтра


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'post_list.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'post_list'
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-creation_date'
    # поставим постраничный вывод в десять элемент
    paginate_by = 1
    # добавляем форм класс, чтобы получать доступ к форме через метод POST
    form_class = PostForm

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами, что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # вписываем наш фильтр (PostFilter) в контекст
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        #context['categories'] = Category.objects.all()
        #context['form'] = PostForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return PostFilter(self.request.GET, queryset=queryset).qs

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)

# дженерик для создания объекта
class PostCreateView(CreateView):
    template_name = 'news/add.html'
    form_class = PostForm


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView, LoginRequiredMixin):
    """
    Класс для редактирования публикации (объекта класса 'Post').
    Создан на основе дженерика 'UpdateView'.
    """
    template_name = 'news/add.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        """
        Метод get_object мы используем вместо queryset, чтобы получить информацию об объекте,
        который мы собираемся редактировать.
        """
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

# дженерик для удаления товара
class PostDeleteView(DeleteView):
    """
    Класс для удаления публикации (объекта класса 'Post').
    Создан на основе дженерика 'DeleteView'.
    """
    template_name = 'news/delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

class Search(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'search_list'
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-creation_date'
    # поставим постраничный вывод в десять элемент
    paginate_by = 10

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами, что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # вписываем наш фильтр (PostFilter) в контекст
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return PostFilter(self.request.GET, queryset=queryset).qs



class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной публикации
    model = Post
    # Используем другой шаблон — post_detail.html
    template_name = 'news/post_detail.html'
    # Название объекта, в котором будет выбранная пользователем публикация
    context_object_name = 'post_detail'

# Create your views here.