from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
#template_name="main/registration/password_reset_form.html"

urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('login/', LoginPage.as_view(), name='login'),
    path('register/', SigninPage.as_view(), name='signin'),
    path('logout/', LogoutPage.as_view(), name='logout'),
    path('buscar-libros/', LibroSearchView.as_view(), name='buscar_libro'),
    path('libro/<int:pk>/', LibroDetailView.as_view(), name='detalle_libro'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_send/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('autores/', ListarAutorView.as_view(), name='listar_autores'),
    path('autores/add', AutorCreateView.as_view(), name='add_autor'),
    path('autores/edit/<int:pk>/', AutorUpdateView.as_view(), name='edit_autor'),
    path('autores/delete/<int:pk>/', AutorDeleteView.as_view(), name='delete_autor'),
    path('generos/', ListarGeneroView.as_view(), name='listar_generos'),
    path('generos/add/', GeneroCreateView.as_view(), name='add_genero'),
    path('generos/edit/<int:pk>/', GeneroUpdateView.as_view(), name='edit_genero'),
    path('generos/delete/<int:pk>/', GeneroDeleteView.as_view(), name='delete_genero'),
    path('libros/', ListarLibroView.as_view(), name='listar_libros'),
    path('libros/add', LibroCreateView.as_view(), name='add_libro'),
    path('libros/edit/<int:pk>/', LibroUpdateView.as_view(), name='edit_libro'),
    path('libros/delete/<int:pk>/', LibroDeleteView.as_view(), name='delete_libro'),
    path('libros/<int:libro_id>/aumentar_stock/', AumentarStockView.as_view(), name='aumentar_stock'),
    path('libros/<int:libro_id>/disminuir_stock/', DisminuirStockView.as_view(), name='disminuir_stock'),
]