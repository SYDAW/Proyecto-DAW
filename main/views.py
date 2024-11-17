from django.contrib import messages
from django.db.models import Q
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import AccessMixin
from django.db.models import Avg, Count
from django.conf import settings
from django.utils import timezone
from .forms import *
from .models import *
from django.contrib.auth import update_session_auth_hash



#Clase mixin que redirige al login
class LoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

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


# Clase para listar libros con filtros
class LibroSearchView(ListView):
    model = Libro
    template_name = 'main/mainPage/buscar_libros.html'
    context_object_name = 'libros'

    def get_queryset(self):
        queryset = Libro.objects.all()
        query = self.request.GET.get('q', '').strip()  

        if query:
            # Busca en título, autor (nombre), géneros (nombre) y ISBN
            queryset = queryset.filter(
                Q(titulo__icontains=query) |
                Q(autor__nombre__icontains=query) |
                Q(generos__nombre__icontains=query) |
                Q(isbn__icontains=query)
            ).distinct() 

        return queryset

    

# Clase ver detalles del libro
class LibroDetailView(DetailView):
    model = Libro
    template_name = 'main/mainPage/detalle_libro.html'
    context_object_name = 'libro'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        libro = self.get_object()

        # Calcular la media de valoraciones y la cantidad de valoraciones
        media_valoraciones = libro.reseñas.aggregate(promedio=Avg('valoracion'))['promedio'] or 0
        cantidad_valoraciones = libro.reseñas.aggregate(total=Count('id'))['total'] or 0

        context['media_valoraciones'] = round(media_valoraciones, 1)  # Redondear a un decimal
        context['cantidad_valoraciones'] = cantidad_valoraciones

        formato = self.request.GET.get('formato', 'Fisico')
        context['formato_seleccionado'] = formato
        context['precio'] = self.get_precio_by_formato(libro, formato)

        return context

    def get_precio_by_formato(self, libro, formato):
        if formato == 'Digital':
            return libro.digital.precio if libro.digital else 0
        return libro.fisico.precio if libro.fisico else 0


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
        form.instance.imagen = self.request.FILES.get('imagen')
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
        #form.instance.imagen = self.request.FILES.get('imagen')
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
class CarritoPage(LoginRequiredMixin, ListView):
    model = ItemCarrito
    template_name = 'main/cesta/carrito.html'
    context_object_name = 'items'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            carrito_usuario = Carrito.objects.filter(usuario=self.request.user).first()
            if carrito_usuario:
                return ItemCarrito.objects.filter(carrito=carrito_usuario)
        return ItemCarrito.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Cálculo del total del carrito
        total_carrito = 0  # Inicializa el total en 0
        for item in context['items']:
            if item.formato == 'Fisico':
                total_carrito += item.producto.fisico.precio * item.cantidad
            elif item.formato == 'Digital':
                total_carrito += item.producto.digital.precio * item.cantidad
        
        # Cálculo del total de productos
        total_productos = sum(item.cantidad for item in context['items'])
        
        # Agregar al contexto
        context['total_carrito'] = total_carrito
        context['total_productos'] = total_productos
        return context

    
# Vista para añadir producto al carrito
class añadirLibroCarrito(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        libro = get_object_or_404(Libro, pk=self.kwargs['pk'])
        formato = request.POST.get('formato')  # Recibe el formato del formulario

        # Verifica que el formato sea uno de los permitidos
        if formato not in ['Fisico', 'Digital']:
            return redirect('carrito')

        # Crear o conseguir el carrito del usuario
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

        # Crear o conseguir el item en el carrito basado en el formato
        item_carrito, created = ItemCarrito.objects.get_or_create(
            carrito=carrito,
            producto=libro,
            formato=formato
        )

        # Actualizar cantidad
        if not created:
            item_carrito.cantidad += 1
        else:
            item_carrito.cantidad = 1

        item_carrito.save()
        return redirect('carrito')


# Clase para aumentar cantidad del producto en el carrito
class AumentarProductoCarrito(View):
    def post(self, request, pk):
        item = get_object_or_404(ItemCarrito, pk=pk)
        
        if isinstance(item.producto, LibroFisico):
            if item.cantidad < item.producto.fisico.stock:
                item.cantidad += 1
                item.save()
            else:
                pass
        else:
            item.cantidad += 1
            item.save()

        return redirect('carrito') 

#Clase para restar producto en el carrito
class RestarProductoCarrito(View):
    def post(self, request, pk):
        item = get_object_or_404(ItemCarrito, pk=pk)
        
        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()
        else:
            item.delete()

        return redirect('carrito')

#Clase para eliminar un producto ya añadido a la compra
class EliminarProductoCarrito(View):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        item = get_object_or_404(ItemCarrito, pk=item_id, carrito__usuario=request.user)
        item.delete()

        return redirect('carrito')
    
#Clase para vaciar el carrito entero
class LimpiarCarrito(View):
    def post(self, request, *args, **kwargs):
        carrito = Carrito.objects.get(usuario=request.user)
        carrito.items.all().delete()

        return redirect('carrito')


# Clase para ver todas las reseñas
class VerReseñas(ListView):
    model = Reseña
    template_name = 'main/comentarios/reseña.html'
    context_object_name = 'reseñas'
    
    def get_queryset(self):
        # Filtrar las reseñas por el libro usando la pk
        libro_id = self.kwargs.get('pk')
        return Reseña.objects.filter(libro_id=libro_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        libro_id = self.kwargs.get('pk')

        # Obtener el objeto `Libro` para calcular las estadísticas
        libro = Libro.objects.get(pk=libro_id)

        # Calcular la media de valoraciones y la cantidad de valoraciones
        media_valoraciones = libro.reseñas.aggregate(promedio=Avg('valoracion'))['promedio'] or 0
        cantidad_valoraciones = libro.reseñas.aggregate(total=Count('id'))['total'] or 0

        context['media_valoraciones'] = round(media_valoraciones, 1)  # Redondear a un decimal
        context['cantidad_valoraciones'] = cantidad_valoraciones
        
        return context
    
# Vistas para editar el perfil de usuario
class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = 'main/perfil/perfil.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = PasswordChangeForm(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, "¡Contraseña actualizada exitosamente!")  
            return redirect('perfil')
        
        messages.error(request, "Hubo un error al cambiar la contraseña.")
        return render(request, self.template_name, {'form': password_form})
        
# Clase para editar perfil
class EditarPerfilView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'main/perfil/editar-perfil.html'
    success_url = reverse_lazy('perfil')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
# Clase para ver tarjetas
class TarjetaListCreateView(LoginRequiredMixin, View):
    template_name = 'main/perfil/tarjeta/ver-tarjetas.html'
    success_url = reverse_lazy('ver_tarjetas')

    def get(self, request, *args, **kwargs):
        tarjetas = Tarjeta.objects.filter(usuario=request.user)
        form = TarjetaForm()
        return render(request, self.template_name, {'tarjetas': tarjetas, 'form': form})

    def post(self, request, *args, **kwargs):
        form = TarjetaForm(request.POST)
        if form.is_valid():
            nueva_tarjeta = form.save(commit=False)
            # Calcula y asigna la fecha de caducidad a partir de mes y año
            mes = int(form.cleaned_data['mes_caducidad'])
            año = int(form.cleaned_data['año_caducidad'])
            nueva_tarjeta.caducidad = date(año, mes, 1)  
            nueva_tarjeta.usuario = request.user
            nueva_tarjeta.save()
            return redirect(self.success_url)
        tarjetas = Tarjeta.objects.filter(usuario=request.user)
        return render(request, self.template_name, {'tarjetas': tarjetas, 'form': form})

# Clase para editar una tarjeta
class TarjetaUpdateView(LoginRequiredMixin, UpdateView):
    model = Tarjeta
    form_class = TarjetaForm
    template_name = 'main/perfil/tarjeta/editar-tarjeta.html'
    success_url = reverse_lazy('ver_tarjetas')

# Clase para eliminar un tarjeta
class TarjetaDeleteView(LoginRequiredMixin, DeleteView):
    model = Tarjeta
    template_name = 'main/perfil/tarjeta/eliminar-tarjeta.html'
    success_url = reverse_lazy('ver_tarjetas')


# Clase para ver y crear direcciones
class DireccionListCreateView(LoginRequiredMixin, View):
    template_name = 'main/perfil/direccion/ver-direcciones.html'
    success_url = reverse_lazy('ver_direcciones')

    def get(self, request, *args, **kwargs):
        direcciones = Direccion.objects.filter(user=request.user)
        form = DireccionForm()
        return render(request, self.template_name, {'direcciones': direcciones, 'form': form})

    def post(self, request, *args, **kwargs):
        form = DireccionForm(request.POST)
        if form.is_valid():
            nueva_direccion = form.save(commit=False)
            nueva_direccion.user = request.user
            nueva_direccion.save()
            return redirect(self.success_url)
        direcciones = Direccion.objects.filter(user=request.user)
        return render(request, self.template_name, {'direcciones': direcciones, 'form': form})


# Clase para editar direccion
class DireccionUpdateView(LoginRequiredMixin, UpdateView):
    model = Direccion
    form_class = DireccionForm
    template_name = 'main/perfil/direccion/editar-direccion.html'
    success_url = reverse_lazy('perfil')

# Clase para eliminar direccion
class DireccionDeleteView(LoginRequiredMixin, DeleteView):
    model = Direccion
    template_name = 'main/perfil/direccion/eliminar-direccion.html'
    success_url = reverse_lazy('perfil')


# Clase para hacer el porceso Checkout
class CheckoutView(View):
    template_name = 'main/compra/checkout.html'

    def get(self, request, *args, **kwargs):
        carrito = get_object_or_404(Carrito, usuario=request.user)

        if not carrito.items.exists():
            messages.error(request, "Tu carrito está vacío.")
            return redirect('ver_carrito')

        total_carrito = sum(
            (item.producto.fisico.precio if item.formato == "Fisico" else item.producto.digital.precio) * item.cantidad
            for item in carrito.items.all()
        )

        form = CheckoutForm(user=request.user, initial={'total_compra': total_carrito})  # Pasa el usuario autenticado
        context = {
            'items': carrito.items.all(),
            'total_carrito': total_carrito,
            'form': form,
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        carrito = get_object_or_404(Carrito, usuario=request.user)

        if not carrito.items.exists():
            messages.error(request, "Tu carrito está vacío.")
            return redirect('ver_carrito')

        total_carrito = sum(
            (item.producto.fisico.precio if item.formato == "Fisico" else item.producto.digital.precio) * item.cantidad
            for item in carrito.items.all()
        )

        form = CheckoutForm(request.POST, user=request.user, initial={'total_compra': total_carrito})
        if form.is_valid():
            compra = form.realizar_compra(request.user, carrito, total_carrito)
            messages.success(request, "¡Compra realizada con éxito!")
            return redirect('confirmacion_compra', pk=compra.pk)

        # En caso de error, renderizar nuevamente con el formulario inválido
        context = {
            'items': carrito.items.all(),
            'total_carrito': total_carrito,
            'form': form,
        }
        return render(request, self.template_name, context)


# Clase para la confirmación de compra
class ConfirmacionCompraView(DetailView):
    model = Compra
    template_name = 'main/compra/payment-success.html'
    context_object_name = 'compra'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        compra = self.get_object()

        # Obtener los detalles de la compra
        context['items'] = compra.detalles.all()
        return context

# Vista para ver compras realizadas
class ComprasRealizadasView(ListView):
    model = DetalleCompra
    template_name = 'main/compra/compras-realizadas.html'
    context_object_name = 'detalles'

    def get_queryset(self):
        return DetalleCompra.objects.filter(compra__usuario=self.request.user).select_related('compra', 'producto')

    

# Vista para los detalles de una compra
class DetalleCompraView(LoginRequiredMixin, DetailView):
    model = Compra
    template_name = 'main/compra/detalle-compra.html'
    context_object_name = 'compra'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        compra = self.get_object()
        context['detalles'] = DetalleCompra.objects.filter(compra=compra)
        return context
