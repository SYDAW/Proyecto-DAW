from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from datetime import date

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

    def clean_precio_digital(self):
        precio_digital = self.cleaned_data.get('precio_digital')
        if precio_digital and precio_digital <= 0:
            raise forms.ValidationError("El precio digital debe ser mayor que cero.")
        return precio_digital

    def clean_precio_fisico(self):
        precio_fisico = self.cleaned_data.get('precio_fisico')
        if precio_fisico and precio_fisico <= 0:
            raise forms.ValidationError("El precio físico debe ser mayor que cero.")
        return precio_fisico

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

        if archivo_digital and precio_digital and precio_fisico:
            # Crear instancias de LibroDigital y LibroFisico solo si los datos son válidos
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

# Formulario tarjeta de credito
class TarjetaForm(forms.ModelForm):
    mes_caducidad = forms.ChoiceField(
        choices=[(i, f"{i:02}") for i in range(1, 13)],
        label="Mes de Caducidad",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    año_caducidad = forms.ChoiceField(
        choices=[(year, year) for year in range(date.today().year, date.today().year + 21)],
        label="Año de Caducidad",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Tarjeta
        fields = ['titular','numero', 'tipo', 'saldo', 'mes_caducidad', 'año_caducidad']
        widgets = {
            'titular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titular de la tarjeta'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numeración de la tarjeta'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'saldo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Saldo disponible'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        mes = int(cleaned_data.get("mes_caducidad"))
        año = int(cleaned_data.get("año_caducidad"))
        cleaned_data['caducidad'] = date(año, mes, 1)  
        return cleaned_data
    
# Formulario direcciones
class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['calle', 'ciudad', 'codigo_postal', 'pais']
        widgets = {
            'calle': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formulario usuario
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

#Formulario para editar contraseña
class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label='Contraseña actual', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirmar nueva contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('La contraseña actual es incorrecta.')
        return old_password

    def clean(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError('Las contraseñas nuevas no coinciden.')
        return self.cleaned_data

    def save(self, commit=True):
        new_password = self.cleaned_data['new_password1']
        self.user.set_password(new_password)
        if commit:
            self.user.save()
        return self.user
    
# Formulario para el checkout de compra
class CheckoutForm(forms.Form):
    direccion = forms.ModelChoiceField(
        queryset=Direccion.objects.none(),  
        label="",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Selecciona una dirección"
    )
    tarjeta = forms.ModelChoiceField(
        queryset=Tarjeta.objects.none(),  
        label="",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Selecciona una tarjeta"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Limitar las opciones de dirección y tarjeta al usuario actual
        if user:
            direcciones = Direccion.objects.filter(user=user)
            tarjetas = Tarjeta.objects.filter(usuario=user)

            print("Direcciones:", direcciones)  # Agrega este print
            print("Tarjetas:", tarjetas)       # Agrega este print

            self.fields['direccion'].queryset = direcciones
            self.fields['tarjeta'].queryset = tarjetas

    def clean(self):
        cleaned_data = super().clean()
        tarjeta = cleaned_data.get('tarjeta')
        total_compra = self.initial.get('total_compra')

        # Verificar saldo suficiente en la tarjeta
        if tarjeta and tarjeta.saldo < total_compra:
            raise forms.ValidationError("Saldo insuficiente en la tarjeta seleccionada.")
        return cleaned_data

    def realizar_compra(self, user, carrito, total_compra):
        # Obtener datos del formulario
        direccion = self.cleaned_data['direccion']
        tarjeta = self.cleaned_data['tarjeta']

        # Validar saldo suficiente
        if tarjeta.saldo < total_compra:
            raise forms.ValidationError("Saldo insuficiente en la tarjeta seleccionada.")


        # Actualizar saldo de la tarjeta
        tarjeta.saldo -= total_compra
        tarjeta.save()

        # Crear la compra
        compra = Compra.objects.create(
            usuario=user,
            total_compra=total_compra,
            direccion_envio=direccion,
            tarjeta_compra=tarjeta,
        )

        # Guardar los detalles de la compra
        for item in carrito.items.all():
            DetalleCompra.objects.create(
                compra=compra,
                producto=item.producto,
                formato=item.formato,
                cantidad=item.cantidad,
                precio_unitario=(item.producto.fisico.precio if item.formato == "Fisico" else item.producto.digital.precio)
            )

        # Vaciar el carrito
        carrito.items.all().delete()

        return compra