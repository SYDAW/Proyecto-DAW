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

        def form_valid(self, form):
            if form.is_valid():
                form.save()  # Guarda el objeto si es válido
                return super().form_valid(form)
            else:
                print(form.errors)  # Esto te permitirá ver los errores en la consola
                return self.form_invalid(form)

# Formulario Libro
class LibroCreateForm(forms.ModelForm):
    precio_digital = forms.DecimalField(
        required=True,
        label="Precio Digital",
        max_digits=12,
        decimal_places=2,
    )

    precio_fisico = forms.DecimalField(
        required=True,
        label="Precio Físico",
        max_digits=12,
        decimal_places=2,
    )

    archivo_digital = forms.FileField(
        required=True,
        label="Archivo Digital",
    )

    class Meta:
        model = Libro
        fields = [
            'titulo', 
            'isbn', 
            'fecha_publicacion', 
            'autor', 
            'generos', 
            'descripcion', 
            'disponibilidad', 
            'imagen', 
        ]
        labels = {
            'titulo': 'Título',
            'isbn': 'ISBN',
            'fecha_publicacion': 'Fecha de Publicación',
            'autor': 'Autor',
            'generos': 'Géneros',
            'descripcion': 'Descripción',
            'disponibilidad': 'Disponibilidad',
            'imagen': 'Imagen',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción del libro'}),
            'fecha_publicacion': forms.DateInput(attrs={'type': 'date'}),
            'imagen': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        archivo_digital = cleaned_data.get('archivo_digital')
        precio_digital = cleaned_data.get('precio_digital')
        precio_fisico = cleaned_data.get('precio_fisico')

        if not archivo_digital:
            self.add_error('archivo_digital', 'El archivo digital es obligatorio.')
        if not precio_digital:
            self.add_error('precio_digital', 'El precio para el formato digital es obligatorio.')
        if not precio_fisico:
            self.add_error('precio_fisico', 'El precio para el formato físico es obligatorio.')

        return cleaned_data

    def save(self, commit=True):
        libro = super().save(commit=commit)
        archivo_digital = self.cleaned_data.get('archivo_digital')
        precio_digital = self.cleaned_data.get('precio_digital')
        precio_fisico = self.cleaned_data.get('precio_fisico')

        # Crear instancias de LibroDigital y LibroFisico
        LibroDigital.objects.create(libro=libro, archivo=archivo_digital, precio=precio_digital)
        LibroFisico.objects.create(libro=libro, stock=10, precio=precio_fisico)

        return libro


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