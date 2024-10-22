from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LibroCreateForm, LoginForm, RegistroForm, AutorForm, StockUpdateForm
from .models import Libro, Autor, Genero, LibroFisico

class IndexPage(TemplateView):
    template_name = 'main/mainPage/index.html'


# Clase para iniciar sesión de usuario
class LoginPage(LoginView):
    template_name = 'main/mainPage/login.html'
    form_class = LoginForm
    
    def get_success_url(self):
        return reverse_lazy('index')
    

# Clase para registrar un nuevo usuario
class SigninPage(CreateView):
    form_class = RegistroForm
    template_name = 'main/mainPage/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

    
    
# Clase para cerrar sesión de usuario
class LogoutPage(LogoutView):
    next_page = 'index'


# Clase para listar libros
class LibroSearchView(ListView):
    model = Libro
    template_name = 'main/mainPage/buscar_libros.html'
    context_object_name = 'libros'

    def get_queryset(self):
        queryset = Libro.objects.all()
        titulo = self.request.GET.get('titulo')
        isbn = self.request.GET.get('isbn')
        autor_id = self.request.GET.get('autor')
        genero_id = self.request.GET.get('genero')

        # Filtros de búsqueda
        if titulo:
            queryset = queryset.filter(titulo__icontains=titulo)
        if isbn:
            queryset = queryset.filter(isbn__icontains=isbn)
        if autor_id:
            queryset = queryset.filter(autor__id=autor_id)
        if genero_id:
            queryset = queryset.filter(generos__id=genero_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['autores'] = Autor.objects.all()
        context['generos'] = Genero.objects.all()
        return context
    

# Clase ver detalles del libro
class LibroDetailView(DetailView):
    model = Libro
    template_name = 'main/mainPage/detalle_libro.html'
    context_object_name = 'libro'


#Clase para listar autores
class ListarAutorView(ListView):
    model = Autor
    template_name = 'main/autor/listar_autor.html'
    context_object_name = 'autores'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Autor.objects.filter(nombre__icontains=query)
        return Autor.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        for autor in context['autores']:
            autor.cantidad_libros = autor.libros.count()

        return context

#Clase para añadir autor
class AutorCreateView(CreateView):
    form_class = AutorForm
    template_name = 'main/autor/add_autor.html'
    success_url = reverse_lazy('listar_autores')  

    def form_valid(self, form):
        return super().form_valid(form)


#Clase para editar autor
class AutorUpdateView(UpdateView):
    model = Autor
    form_class = AutorForm
    template_name = 'main/autor/edit_autor.html'
    success_url = reverse_lazy('listar_autores')  


#Clase para eliminar autor
class AutorDeleteView(DeleteView):
    model = Autor
    template_name = 'main/autor/delete_autor.html'
    success_url = reverse_lazy('listar_autores') 


#Clase para listar géneros
class ListarGeneroView(ListView):
    model = Genero
    template_name = 'main/genero/listar_genero.html'
    context_object_name = 'generos'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Genero.objects.filter(nombre__icontains=query)
        return Genero.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


#Clase para crear género
class GeneroCreateView(CreateView):
    model = Genero
    fields = ['nombre'] 
    template_name = 'main/genero/add_genero.html'
    success_url = reverse_lazy('listar_generos')

    def form_valid(self, form):
        return super().form_valid(form)


# Clase para editar género
class GeneroUpdateView(UpdateView):
    model = Genero
    fields = ['nombre']  
    template_name = 'main/genero/edit_genero.html'
    success_url = reverse_lazy('listar_generos')


# Clase para eliminar género
class GeneroDeleteView(DeleteView):
    model = Genero
    template_name = 'main/genero/delete_genero.html'
    success_url = reverse_lazy('listar_generos')


#Clase para listar libros
class ListarLibroView(ListView):
    model = Libro
    template_name = 'main/libro/listar_libro.html'
    context_object_name = 'libros'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            libros_por_titulo = Libro.objects.filter(titulo__icontains=query)
            libros_por_autor = Libro.objects.filter(autor__nombre__icontains=query)
            return libros_por_titulo | libros_por_autor
        return Libro.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

#Clase para añadir libro
class LibroCreateView(CreateView):
    form_class = LibroCreateForm
    template_name = 'main/libro/add_libro.html'
    success_url = reverse_lazy('listar_libros')  

    def form_valid(self, form):
        libro = form.save()

        if libro.formato == 'Físico':
            LibroFisico.objects.create(libro=libro, stock=10)

        return super().form_valid(form)
  

# Clase para editar libro
class LibroUpdateView(UpdateView):
    model = Libro
    form_class = LibroCreateForm
    template_name = 'main/libro/edit_libro.html'
    success_url = reverse_lazy('listar_libros')


# Clase para eliminar libro
class LibroDeleteView(DeleteView):
    model = Libro
    template_name = 'main/libro/delete_libro.html'
    success_url = reverse_lazy('listar_libros')


# Clase para aumentar stock
class AumentarStockView(View):
    def post(self, request, libro_id):
        libro_fisico = get_object_or_404(LibroFisico, libro_id=libro_id)
        libro_fisico.stock += 1  
        libro_fisico.save()
        return redirect('listar_libros')  


# Clase para disminuir stock
class DisminuirStockView(View):
    def post(self, request, libro_id):
        libro_fisico = get_object_or_404(LibroFisico, libro_id=libro_id)
        if libro_fisico.stock > 0:
            libro_fisico.stock -= 1  
            libro_fisico.save()
        return redirect('listar_libros')
    

# Clase para carrito
class CarritoPage(TemplateView):
    template_name = 'main/cesta/carrito.html'
