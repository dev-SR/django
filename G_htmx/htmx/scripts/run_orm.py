from htmx.models import Option, VariantOption


def run():

    # Get all options
    options_list = Option.objects.get_options_with_values()
    print(options_list)
