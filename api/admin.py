from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import *

class UsuarioCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    is_superuser = forms.BooleanField(label='Superuser??', required=False)

    class Meta:
        model = Usuario
        fields = ('email', 'first_name', 'last_name', 'direccion', 'ciudad', 'pais', 'codigo_postal', 'telefono', 'is_superuser')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_superuser = self.cleaned_data.get("is_superuser")
        user.is_staff = self.cleaned_data.get("is_superuser")
        if commit:
            user.save()
        return user

class UsuarioChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ('email', 'first_name', 'last_name', 'direccion', 'ciudad', 'pais', 'codigo_postal', 'telefono', 'password', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')

    def clean_password(self):
        return self.initial["password"]

class UsuarioAdmin(BaseUserAdmin):
    form = UsuarioChangeForm
    add_form = UsuarioCreationForm

    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'direccion', 'ciudad', 'pais', 'codigo_postal', 'telefono')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'direccion', 'ciudad', 'pais', 'codigo_postal', 'telefono', 'password1', 'password2', 'is_superuser')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre_producto', 'categoria', 'marca', 'precio', 'stock']
    search_fields = ['nombre_producto', 'categoria', 'marca']
    list_filter = ['categoria', 'marca']
    inlines = [ImagenProductoInline]

class PedidoAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'fecha_pedido', 'metodo_pago', 'precio_total', 'estado_pedido']
    list_filter = ['estado_pedido', 'metodo_pago']
    search_fields = ['cliente__email']

class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'producto', 'cantidad', 'precio_unidad']
    search_fields = ['pedido__id', 'producto__nombre_producto']

class ReembolsoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'fecha_reembolso', 'precio_reembolso', 'motivo']
    search_fields = ['pedido__id']

class CarritoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'creado_en']
    search_fields = ['usuario__email']

class ProductoCarritoAdmin(admin.ModelAdmin):
    list_display = ['carrito', 'producto', 'cantidad']
    search_fields = ['carrito__usuario__email', 'producto__nombre_producto']

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(DetallePedido, DetallePedidoAdmin)
admin.site.register(Reembolso, ReembolsoAdmin)
admin.site.register(Carrito, CarritoAdmin)
admin.site.register(ProductoCarrito, ProductoCarritoAdmin)
