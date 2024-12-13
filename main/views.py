from datetime import timedelta
from django.contrib import messages
from django.db.models import Q
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import AccessMixin
from django.db.models import Avg, Count
from .forms import *
from .models import *
from django.db.models import Sum
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, Http404

# Vista mixin que redirige al login
class LoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

# Vista para la mainpage
class IndexPage(TemplateView):
    template_name = 'main/mainPage/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Agregar los 8 libros más leídos (más comprados)
        context['libros_mas_leidos'] = (
            Libro.objects.annotate(total_compras=Sum('detallecompra__cantidad'))
            .filter(total_compras__isnull=False)
            .order_by('-total_compras')[:8]
        )

        # Agregar los 8 libros más nuevos
        context['libros_mas_nuevos'] = (
            Libro.objects.filter(disponibilidad=True)
            .order_by('-fecha_publicacion')[:8]
        )

        # Agregar hasta 8 libros disponibles para reserva
        context['libros_reserva'] = (
            Libro.objects.filter(disponibilidad=True)[:8]
        )

        # Top 5 clientes que más han comprado
        context['top_clientes'] = (
            User.objects.annotate(total_compras=Count('compras'))
            .filter(total_compras__gt=0)
            .order_by('-total_compras')[:5]
        )

        # Media de reservas por libros (libros más prestados)
        context['libros_mas_prestados'] = (
            Libro.objects.annotate(total_reservas=Count('fisico__reservas'))
            .filter(total_reservas__isnull=False)
            .order_by('-total_reservas')[:5]
        )

        # Clientes con más gasto acumulado
        context['clientes_mas_gasto'] = (
            User.objects.annotate(gasto_total=Sum('compras__total_compra'))
            .filter(gasto_total__gt=0)
            .order_by('-gasto_total')[:5]
        )

        # Géneros más vendidos
        context['generos_mas_vendidos'] = (
            Genero.objects.annotate(
                total_vendidos=Sum('libros__detallecompra__cantidad')
            )
            .filter(total_vendidos__gt=0)
            .order_by('-total_vendidos')[:5]
        )

        # Libros con mejores valoraciones promedio
        context['libros_mejores_valorados'] = (
            Libro.objects.annotate(valoracion_promedio=Avg('reseñas__valoracion'))
            .filter(valoracion_promedio__isnull=False)
            .order_by('-valoracion_promedio')[:5]
        )


        return context


# Vista para iniciar sesión de usuario
class LoginPage(LoginView):
    template_name = 'main/mainPage/login.html'
    form_class = LoginForm
    
    def get_success_url(self):
        return reverse_lazy('index')
    

# Vista para registrar un nuevo usuario
class SigninPage(CreateView):
    form_class = RegistroForm
    template_name = 'main/mainPage/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

    
    
# Vista para cerrar sesión de usuario
class LogoutPage(LogoutView):
    next_page = 'index'


# Vista para listar libros con filtros
class LibroSearchView(ListView):
    model = Libro
    template_name = 'main/mainPage/buscar_libros.html'
    context_object_name = 'libros'

    def get_queryset(self):
        queryset = Libro.objects.all()
        query = self.request.GET.get('q', '').strip()
        genero = self.request.GET.get('genero', '').strip()  

        if query:
            # Busca en título, autor (nombre), géneros (nombre) y ISBN
            queryset = queryset.filter(
                Q(titulo__icontains=query) |
                Q(autor__nombre__icontains=query) |
                Q(generos__nombre__icontains=query) |
                Q(isbn__icontains=query)
            ).distinct()

        if genero:
            queryset = queryset.filter(generos__nombre__iexact=genero)

        return queryset

    

# Vista ver detalles del libro
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

        # Verificar si el usuario ha comprado el libro en formato digital
        usuario_compro_digital = False
        if self.request.user.is_authenticated:  # Solo verificamos si el usuario está autenticado
            usuario_compro_digital = DetalleCompra.objects.filter(
                Q(compra__usuario=self.request.user) &
                Q(producto=libro) &
                Q(formato='Digital')
            ).exists()

        context['usuario_compro_digital'] = usuario_compro_digital

        # Formato y precio seleccionado
        formato = self.request.GET.get('formato', 'Fisico')
        context['formato_seleccionado'] = formato
        context['precio'] = self.get_precio_by_formato(libro, formato)

        return context

    def get_precio_by_formato(self, libro, formato):
        if formato == 'Digital':
            return libro.digital.precio if libro.digital else 0
        return libro.fisico.precio if libro.fisico else 0


# Vista para listar autores
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

# Vista para añadir autor
class AutorCreateView(CreateView):
    form_class = AutorForm
    template_name = 'main/autor/add_autor.html'
    success_url = reverse_lazy('listar_autores')  

    def form_valid(self, form):
        form.instance.imagen = self.request.FILES.get('imagen')
        return super().form_valid(form)


# Vista para editar autor
class AutorUpdateView(UpdateView):
    model = Autor
    form_class = AutorForm
    template_name = 'main/autor/edit_autor.html'
    success_url = reverse_lazy('listar_autores')  


# Vista para eliminar autor
class AutorDeleteView(DeleteView):
    model = Autor
    template_name = 'main/autor/delete_autor.html'
    success_url = reverse_lazy('listar_autores') 


# Vista para listar géneros
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


# Vista para crear género
class GeneroCreateView(CreateView):
    model = Genero
    fields = ['nombre'] 
    template_name = 'main/genero/add_genero.html'
    success_url = reverse_lazy('listar_generos')

    def form_valid(self, form):
        return super().form_valid(form)


# Vista para editar género
class GeneroUpdateView(UpdateView):
    model = Genero
    fields = ['nombre']  
    template_name = 'main/genero/edit_genero.html'
    success_url = reverse_lazy('listar_generos')


# Vista para eliminar género
class GeneroDeleteView(DeleteView):
    model = Genero
    template_name = 'main/genero/delete_genero.html'
    success_url = reverse_lazy('listar_generos')


# Vista para listar libros
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


# Vista para añadir libro
class LibroCreateView(CreateView):
    form_class = LibroCreateForm
    template_name = 'main/libro/add_libro.html'
    success_url = reverse_lazy('listar_libros')  

    def form_valid(self, form):
        #form.instance.imagen = self.request.FILES.get('imagen')
        return super().form_valid(form)
  

# Vista para editar libro
class LibroUpdateView(UpdateView):
    model = Libro
    form_class = LibroCreateForm
    template_name = 'main/libro/edit_libro.html'
    success_url = reverse_lazy('listar_libros')


# Vista para eliminar libro
class LibroDeleteView(DeleteView):
    model = Libro
    template_name = 'main/libro/delete_libro.html'
    success_url = reverse_lazy('listar_libros')


# Vista para aumentar stock
class AumentarStockView(View):
    def post(self, request, libro_id):
        libro_fisico = get_object_or_404(LibroFisico, libro_id=libro_id)
        libro_fisico.stock += 1  
        libro_fisico.save()
        return redirect('listar_libros')  


# Vista para disminuir stock
class DisminuirStockView(View):
    def post(self, request, libro_id):
        libro_fisico = get_object_or_404(LibroFisico, libro_id=libro_id)
        if libro_fisico.stock > 0:
            libro_fisico.stock -= 1  
            libro_fisico.save()
        return redirect('listar_libros')
    

# Vista para carrito
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

    
# Vista  para añadir producto al carrito
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


# Vista para aumentar cantidad del producto en el carrito
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

# Vista para restar producto en el carrito
class RestarProductoCarrito(View):
    def post(self, request, pk):
        item = get_object_or_404(ItemCarrito, pk=pk)
        
        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()
        else:
            item.delete()

        return redirect('carrito')

# Vista para eliminar un producto ya añadido a la compra
class EliminarProductoCarrito(View):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        item = get_object_or_404(ItemCarrito, pk=item_id, carrito__usuario=request.user)
        item.delete()

        return redirect('carrito')
    
# Vista para vaciar el carrito entero
class LimpiarCarrito(View):
    def post(self, request, *args, **kwargs):
        carrito = Carrito.objects.get(usuario=request.user)
        carrito.items.all().delete()

        return redirect('carrito')


# Vista para ver todas las reseñas
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
    
# Vista s para editar el perfil de usuario
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
        
# Vista para editar perfil
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
    
# Vista para ver tarjetas
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

# Vista para editar una tarjeta
class TarjetaUpdateView(LoginRequiredMixin, UpdateView):
    model = Tarjeta
    form_class = TarjetaForm
    template_name = 'main/perfil/tarjeta/editar-tarjeta.html'
    success_url = reverse_lazy('ver_tarjetas')

# Vista para eliminar un tarjeta
class TarjetaDeleteView(LoginRequiredMixin, DeleteView):
    model = Tarjeta
    template_name = 'main/perfil/tarjeta/eliminar-tarjeta.html'
    success_url = reverse_lazy('ver_tarjetas')


# Vista para ver y crear direcciones
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


# Vista para editar direccion
class DireccionUpdateView(LoginRequiredMixin, UpdateView):
    model = Direccion
    form_class = DireccionForm
    template_name = 'main/perfil/direccion/editar-direccion.html'
    success_url = reverse_lazy('perfil')

# Vista para eliminar direccion
class DireccionDeleteView(LoginRequiredMixin, DeleteView):
    model = Direccion
    template_name = 'main/perfil/direccion/eliminar-direccion.html'
    success_url = reverse_lazy('perfil')


# Vista para hacer el porceso Checkout
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
        else:
            print(form.errors)

        # En caso de error, renderizar nuevamente con el formulario inválido
        context = {
            'items': carrito.items.all(),
            'total_carrito': total_carrito,
            'form': form,
        }
        return render(request, self.template_name, context)


# Vista para la confirmación de compra
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


# Vista  para ver compras realizadas
class ComprasRealizadasView(ListView):
    model = Compra
    template_name = 'main/compra/compras-realizadas.html'
    context_object_name = 'compras'

    def get_queryset(self):
        return Compra.objects.filter(usuario=self.request.user).prefetch_related('detalles__producto')


# Vista  para ver los detalles de compra
class DetallePedidoView(LoginRequiredMixin, DetailView):
    model = Compra
    template_name = 'main/compra/detalles-pedido.html'
    context_object_name = 'compra'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        compra = self.get_object()
        
        # Calcular el precio total de los libros en el pedido
        total_libros = sum(detalle.precio_unitario * detalle.cantidad for detalle in compra.detalles.all())
        context['total_libros'] = total_libros
        
        return context

# Vista  para crear la reseña
class CrearEditarReseñaView(LoginRequiredMixin, FormView):
    model = Reseña
    form_class = ReseñaForm
    template_name = 'main/perfil/reseña/crear_editar_reseña.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        libro = get_object_or_404(Libro, pk=self.kwargs['pk'])
        compra = get_object_or_404(Compra, pk=self.request.GET.get('compra_id'))  # Obtener compra del parámetro GET
        detalle = get_object_or_404(DetalleCompra, producto=libro, compra=compra)  # Buscar el detalle de la compra
        context['libro'] = libro
        context['compra'] = compra
        context['detalle'] = detalle
        return context

    def get_form(self):
        libro = get_object_or_404(Libro, pk=self.kwargs['pk'])
        compra_id = self.request.GET.get('compra_id')  # Obtener el ID de la compra desde el GET
        compra = get_object_or_404(Compra, pk=compra_id)

        try:
            # Buscar la reseña existente vinculada al usuario y al libro
            reseña = Reseña.objects.get(libro=libro, usuario=self.request.user)
            return ReseñaForm(instance=reseña, **self.get_form_kwargs())
        except Reseña.DoesNotExist:
            return ReseñaForm(**self.get_form_kwargs())

    def form_valid(self, form):
        libro = get_object_or_404(Libro, pk=self.kwargs['pk'])
        compra = get_object_or_404(Compra, pk=self.request.GET.get('compra_id'))
        detalle = get_object_or_404(DetalleCompra, producto=libro, compra=compra)

        # Crear o actualizar reseña
        reseña, created = Reseña.objects.get_or_create(
            libro=libro,
            usuario=self.request.user,
            defaults={
                'comentario': form.cleaned_data['comentario'],
                'valoracion': form.cleaned_data['valoracion']
            }
        )
        if not created:
            reseña.comentario = form.cleaned_data['comentario']
            reseña.valoracion = form.cleaned_data['valoracion']
            reseña.save()

        # Redirigir al detalle de la compra
        return redirect('compras_realizadas') 

    def form_invalid(self, form):
        return super().form_invalid(form)

# Vista para ver todas las reseñas
class MisReseñasView(LoginRequiredMixin, ListView):
    model = Reseña
    template_name = 'main/perfil/reseña/mis-reseñas.html'
    context_object_name = 'reseñas'

    def get_queryset(self):
        return Reseña.objects.filter(usuario=self.request.user).select_related('libro').order_by('-fecha')
    
# Vista para editar reseña
class EditarReseñaView(LoginRequiredMixin, UpdateView):
    model = Reseña
    form_class = ReseñaForm
    template_name = 'main/perfil/reseña/editar_reseña.html'

    def get_queryset(self):
        return Reseña.objects.filter(usuario=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['libro'] = self.object.libro
        return context

    def form_valid(self, form):
        self.object = form.save()
        return redirect('mis_reseñas')  

# Vista para eliminar reseña
class EliminarReseñaView(LoginRequiredMixin, DeleteView):
    model = Reseña
    template_name = 'main/perfil/reseña/eliminar_reseña.html'

    def get_queryset(self):
        return Reseña.objects.filter(usuario=self.request.user)

    def get_success_url(self):
        return reverse_lazy('mis_reseñas')
    
# Vista para elegir el formato del libro al hacer la reserva
class ElegirFormatoView(LoginRequiredMixin, FormView):
    template_name = "main/reserva_libro/elegir_formato.html"
    form_class = ElegirFormatoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        libro = get_object_or_404(Libro, id=self.kwargs['libro_id'])
        context['libro'] = libro
        context['libro_fisico'] = LibroFisico.objects.filter(libro=libro).first()
        context['libro_digital'] = LibroDigital.objects.filter(libro=libro).first()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        kwargs['libro'] = get_object_or_404(Libro, id=self.kwargs['libro_id'])
        return kwargs

    def form_valid(self, form):
        formato = form.cleaned_data.get('formato')
        tarjeta_id = form.cleaned_data.get('tarjeta')
        libro_id = self.kwargs['libro_id']
        usuario = self.request.user

        if formato == 'Físico':
            libro_fisico = get_object_or_404(LibroFisico, libro_id=libro_id)
            tarjeta = get_object_or_404(Tarjeta, id=tarjeta_id, usuario=usuario)

            if libro_fisico.stock <= 0:
                messages.error(self.request, "No hay stock disponible para el libro físico.")
                return self.form_invalid(form)

            fianza = libro_fisico.precio + 5
            reserva = ReservaLibroFisico.objects.create(
                usuario=usuario,
                libro=libro_fisico,
                tarjeta_reserva=tarjeta,
                fecha_devolucion=date.today() + timedelta(days=30),
                fianza=fianza,
                estado_reserva='Activa'
            )
            libro_fisico.stock -= 1
            libro_fisico.save()
            return redirect(reverse('reserva_confirmada', kwargs={'reserva_id': reserva.id}))

        elif formato == 'Digital':
            libro_digital = get_object_or_404(LibroDigital, libro_id=libro_id)
            reserva = ReservaLibroDigital.objects.create(
                usuario=usuario,
                libro=libro_digital,
                fecha_expiracion=date.today() + timedelta(days=25),
                estado_reserva='Activa'
            )
            return redirect(reverse('reserva_confirmada', kwargs={'reserva_id': reserva.id}))

# Vista para confirmación de reserva     
class ReservaConfirmadaView(LoginRequiredMixin, TemplateView):
    template_name = "main/reserva_libro/reserva_confirmada.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reserva_id = self.kwargs['reserva_id']
        
        # Busca la reserva en ambas tablas
        reserva = (
            ReservaLibroFisico.objects.filter(id=reserva_id).first() or 
            ReservaLibroDigital.objects.filter(id=reserva_id).first()
        )

        if reserva:
            context['reserva'] = reserva
            # Extrae el formato directamente del tipo de reserva
            context['formato'] = 'Físico' if isinstance(reserva, ReservaLibroFisico) else 'Digital'
        else:
            context['reserva'] = None
            context['formato'] = None

        return context


# Vista para ver todas la reservas
class MisReservasView(LoginRequiredMixin, ListView):
    template_name = "main/reserva_libro/reservas_usuario.html"
    context_object_name = "reservas"

    def get_queryset(self):
        usuario = self.request.user
        query = self.request.GET.get("q", "")

        # Obtener reservas físicas y digitales
        reservas_fisicas = ReservaLibroFisico.objects.filter(usuario=usuario)
        reservas_digitales = ReservaLibroDigital.objects.filter(usuario=usuario)

        # Filtrar por búsqueda
        if query:
            reservas_fisicas = reservas_fisicas.filter(
                Q(libro__libro__titulo__icontains=query) | Q(libro__libro__autor__nombre__icontains=query)
            )
            reservas_digitales = reservas_digitales.filter(
                Q(libro__libro__titulo__icontains=query) | Q(libro__libro__autor__nombre__icontains=query)
            )

        # Añadir el formato como atributo a cada reserva
        for reserva in reservas_fisicas:
            reserva.formato = "Físico"
        for reserva in reservas_digitales:
            reserva.formato = "Digital"

        # Combinar las reservas
        return list(reservas_fisicas) + list(reservas_digitales)

# Vista para ver detalles de reserva
class DetalleReservaView(TemplateView):
    template_name = "main/reserva_libro/detalle_reserva.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')

        # Buscar primero en las reservas físicas
        reserva = ReservaLibroFisico.objects.filter(pk=pk).first()
        if reserva:
            context['reserva'] = reserva
            context['formato'] = "Físico"
            return context

        # Si no es una reserva física, buscar en las digitales
        reserva = get_object_or_404(ReservaLibroDigital, pk=pk)
        context['reserva'] = reserva
        context['formato'] = "Digital"
        return context

# Vista para ver los libros epubs del usuario
class MisLibrosEPUBView(LoginRequiredMixin, TemplateView):
    template_name = 'main/perfil/mis_libros/perfil_libros_epub.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener el término de búsqueda
        query = self.request.GET.get('q', '')

        # Inicializar variables con valores predeterminados
        libros_comprados = DetalleCompra.objects.filter(
            compra__usuario=self.request.user,
            formato='Digital'
        )

        libros_reservados = ReservaLibroDigital.objects.filter(
            usuario=self.request.user,
            estado_reserva='Activa'
        )

        # Filtrar resultados si hay consulta
        if query:
            libros_comprados = libros_comprados.filter(
                Q(producto__titulo__icontains=query) |
                Q(producto__autor__nombre__icontains=query)
            )
            libros_reservados = libros_reservados.filter(
                Q(libro__libro__titulo__icontains=query) |
                Q(libro__libro__autor__nombre__icontains=query)
            )

        # Asignar los valores al contexto
        context['libros_epub'] = libros_comprados
        context['libros_reservados'] = libros_reservados
        context['query'] = query  
        return context


# Vista para descargar libro comprado
class DescargarLibroDigitalView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        # Obtener el detalle de la compra para verificar que pertenece al usuario
        detalle_compra = get_object_or_404(DetalleCompra, pk=pk, compra__usuario=request.user, formato='Digital')
        
        # Obtener el libro digital relacionado
        libro_digital = get_object_or_404(LibroDigital, libro=detalle_compra.producto)

        # Verificar si el archivo existe
        if not libro_digital.archivo:
            raise Http404("El archivo del libro no está disponible.")

        # Configurar la respuesta para la descarga del archivo
        response = HttpResponse(libro_digital.archivo.open('rb'), content_type='application/epub+zip')
        response['Content-Disposition'] = f'attachment; filename="{libro_digital.libro.titulo}.epub"'
        return response


# Vista para gestionar todas las reservas con buscador
class GestionReservasListView(UserPassesTestMixin, ListView):
    template_name = 'main/reserva_libro/gestion_reservas.html'
    context_object_name = 'reservas'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        reservas_fisicas = ReservaLibroFisico.objects.filter(
            Q(libro__libro__titulo__icontains=query) | Q(estado_reserva__icontains=query)
        )
        reservas_digitales = ReservaLibroDigital.objects.filter(
            Q(libro__libro__titulo__icontains=query) | Q(estado_reserva__icontains=query)
        )
        return {
            'reservas_fisicas': reservas_fisicas,
            'reservas_digitales': reservas_digitales
        }

# Vista  para el historial de compras
class HistorialComprasListView(UserPassesTestMixin, ListView):
    model = Compra
    template_name = 'main/compra/historial_compras.html'
    context_object_name = 'compras'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return Compra.objects.filter(
            Q(id__icontains=query) |
            Q(usuario__username__icontains=query) |
            Q(detalles__producto__titulo__icontains=query) |
            Q(fecha__icontains=query)
        ).distinct().order_by('id')

# Vista  para para listar libros para reseña
class ListarLibroReseñaView(ListView):
    model = Libro
    template_name = 'main/reseñas/libros_reseña.html'
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
    

# Vista  para editar una reseña
class AdminEditarReseñaView(UserPassesTestMixin, UpdateView):
    model = Reseña
    form_class = ReseñaForm
    template_name = 'main/reseñas/admin_editar_reseña.html'
    success_url = reverse_lazy('listar_libros')  

    def test_func(self):
        return self.request.user.is_staff

# Vista  para borrar una reseña
class AdminEliminarReseñaView(UserPassesTestMixin, DeleteView):
    model = Reseña
    template_name = 'main/reseñas/admin_eliminar_reseña.html'
    success_url = reverse_lazy('listar_libros') 

    def test_func(self):
        return self.request.user.is_staff
    