from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

# Formulario de autenticación de usuario
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget= forms.TextInput(attrs={'class': 'form-control'}),
        label='Username'
    )

    password = forms.CharField(
        widget= forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Password'
    )

# Formulario de registro de usuario
class RegistroForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label='Username'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso. Por favor, elige otro.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

        return user


# Formulario Autor
class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 'biografia', 'imagen']
        widgets = {
            'biografia': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'imagen': forms.FileInput(attrs={'accept': 'image/*'}),
        }

# Formulario Libro
class LibroCreateForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = [
            'titulo', 
            'isbn', 
            'fecha_publicacion', 
            'autor', 
            'precio', 
            'generos', 
            'descripcion', 
            'formato', 
            'disponibilidad', 
            'imagen'
        ]
        labels = {
            'titulo': 'Título',
            'isbn': 'ISBN',
            'fecha_publicacion': 'Fecha de Publicación',
            'autor': 'Autor',
            'precio': 'Precio',
            'generos': 'Géneros',
            'descripcion': 'Descripción',
            'formato': 'Formato',
            'disponibilidad': 'Disponibilidad',
            'imagen': 'Imagen',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción del libro'}),
            'fecha_publicacion': forms.DateInput(attrs={'type': 'date'}),
            'precio': forms.NumberInput(attrs={'step': 0.01}),
            'imagen': forms.FileInput(attrs={'accept': 'image/*'}),
        }


# Formulario para libro fisico
class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = LibroFisico
        fields = ['stock']
        labels = {
            'stock': 'Cantidad en Stock',
        }
        widgets = {
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }