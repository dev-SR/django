from typing import Any
from django.shortcuts import render

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView

from htmx.models import Category, ProductVariant


def change_theme(request: HttpRequest):
    if "is_dark_mode" in request.session:
        request.session["is_dark_mode"] = not request.session["is_dark_mode"]
    else:
        request.session["is_dark_mode"] = False

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class HomeList(ListView):
    model = ProductVariant
    template_name = "product/productlist/index.html"
    product_template_partial = "product/productlist/product_item_partial.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if "is_dark_mode" not in request.session:
            request.session["is_dark_mode"] = False
        isHtmx = request.headers.get('HX-Request')
        print(isHtmx, request.GET)

        # if request is not htmx then return the default response
        if not isHtmx:
            return super().get(request, **kwargs)
        # print(self.get_context_data())

        category_id = request.GET.get('category')
        if category_id:
            qs = ProductVariant.objects.filter(product__category__id=category_id)
        else:
            qs = ProductVariant.objects.all()

        return render(request, self.product_template_partial, context={
            'object_list': qs,
            'categories': Category.objects.all()
        })


HomeListView = HomeList.as_view()
