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
from django.core.paginator import Paginator


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
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        # context['options'] = Option.objects.get_options_with_values()

        return context

    def get(self, request, *args, **kwargs):
        if "is_dark_mode" not in request.session:
            request.session["is_dark_mode"] = False
        is_htmx = request.headers.get('HX-Request')

        if not is_htmx:
            return super().get(request, **kwargs)

        category_id = request.GET.get('category')
        search_query = request.GET.get('search')
        selected_filters = {}

        # Collect selected filter values for each option
        for key, values in request.GET.lists():
            if values and key not in ["category", "search", "page"]:
                selected_filters[key] = values

        product_variants_queryset = ProductVariant.objects.all()

        # Apply category filter
        if category_id:
            product_variants_queryset = product_variants_queryset.filter(product__category__id=category_id)
            # Apply selected filters to the queryset
            for option_name, option_values in selected_filters.items():
                q_objects = Q()
                for value in option_values:
                    q_objects |= Q(variant_options__option__name=option_name, variant_options__value=value)
                product_variants_queryset = product_variants_queryset.filter(q_objects)

        # Apply search filter
        if search_query:
            product_variants_queryset = product_variants_queryset.filter(
                Q(product__name__icontains=search_query) | Q(sku__icontains=search_query)
            )

        # When a category is selected, add unselected values to the options
        if not category_id:
            options_list = []
        else:
            options_dict = {}
            options = Option.objects.prefetch_related('variant_options').filter(category__id=category_id)
            for option in options:
                unique_values = set(vo.value for vo in option.variant_options.all())
                options_dict[option.name] = [
                    {'name': value, 'checked': value in selected_filters.get(option.name, [])} for value in unique_values
                ]
            # Iterate over each variant to collect option values
            for variant in product_variants_queryset:
                for option_value in variant.variant_options.all():
                    option_name = option_value.option.name
                    value_name = option_value.value
                    if option_name not in options_dict:
                        options_dict[option_name] = []
                    if value_name not in [item['name'] for item in options_dict[option_name]]:
                        options_dict[option_name].append(
                            {'name': value_name, 'checked': value_name in selected_filters.get(option_name, [])}
                        )

            # Iterate over each option value to mark it as unavailable if not found in the queryset
            for option_name, values_list in options_dict.items():
                for value in values_list:
                    value['available'] = any(
                        value['name'] == option_value.value
                        for variant in product_variants_queryset
                        for option_value in variant.variant_options.filter(option__name=option_name)
                    )

            # Construct options_list in the desired pattern
            options_list = [{'option': option_name, 'values': values_list}
                            for option_name, values_list in options_dict.items()]

        paginator = Paginator(product_variants_queryset, per_page=self.paginate_by)
        page = request.GET.get('page', 1)
        page_obj = paginator.get_page(page)

        return render(request, self.product_template_partial, context={
            "options": options_list,
            'page_obj': page_obj,
        })


HomeListView = HomeList.as_view()
