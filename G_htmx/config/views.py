from htmx.models import ProductVariant, Category, Option
from django.views.generic import ListView
from typing import Any
from django.shortcuts import render
from pprint import pprint
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.db.models import Q


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['options'] = Option.objects.get_options_with_values()

        return context

    def get(self, request, *args, **kwargs):
        if "is_dark_mode" not in request.session:
            request.session["is_dark_mode"] = False
        isHtmx = request.headers.get('HX-Request')

        if not isHtmx:
            return super().get(request, **kwargs)

        category_id = request.GET.get('category')
        search_query = request.GET.get('search')
        selected_filters = {}

        # Collect selected filter values for each option
        for key, values in request.GET.lists():
            if values and key != 'category' and key != 'search':
                selected_filters[key] = values

        qs = ProductVariant.objects.all()

        if category_id:
            qs = qs.filter(product__category__id=category_id)

        if search_query:
            qs = qs.filter(Q(product__name__icontains=search_query) | Q(sku__icontains=search_query))

        # Apply selected filters to the queryset
        for option_name, option_values in selected_filters.items():
            q_objects = Q()
            for value in option_values:
                q_objects |= Q(variant_options__option__name=option_name, variant_options__value=value)
            qs = qs.filter(q_objects)

        # dynamic options/ narrowed down:
        options = Option.objects.prefetch_related('variant_options').all()
        if category_id:
            options = options.filter(category__id=category_id)
        options_dict = {}
        for option in options:
            unique_values = set(vo.value for vo in option.variant_options.all())
            options_dict[option.name] = [
                {'name': value, 'checked': value in selected_filters.get(option.name, [])} for value in unique_values]
        options_list = [{'option': key, 'values': value} for key, value in options_dict.items()]
        # pprint(options_list)

        # pprint(set(vo.value for vo in variants))
        return render(request, self.product_template_partial, context={
            'object_list': qs,
            "options": options_list
        })


HomeListView = HomeList.as_view()
