from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .views import index
from django.contrib import admin
from django.urls import include, path, reverse
from django.conf import settings
from django.conf.urls.static import static

from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProductForm
from app.models import Product
from django.contrib import messages


def form_edit(request, pk=None):
    if pk is not None:
        product = get_object_or_404(Product, pk=pk)
    else:
        product = None
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            updated_product = form.save()
            if product is None:
                messages.success(request, f"Product {updated_product.name} created!")
            else:
                messages.success(request, f"Product {updated_product.name} updated!")
            # redirect on edit page
            return redirect(reverse("form_edit", kwargs={"pk": updated_product.pk}))
    else:
        form = ProductForm(instance=product)

    return render(request, "form/form-example2.html", {"form": form})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name='index'),
    path('form-edit/', form_edit, name='form_create'),
    path('form-edit/<int:pk>/', form_edit, name='form_edit'),
    path("__reload__/", include("django_browser_reload.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT)
