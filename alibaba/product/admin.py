from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'desc', 'price', 'create_time')
    list_display_links = ('title',)
    # 修改时需要验证的字段例如'title'，不要放在list_editable中，这样会绕过ModelForm的验证机制
    list_editable = ('price',)

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)
