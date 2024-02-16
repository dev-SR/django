# HTMX in Django Web Application

- [HTMX in Django Web Application](#htmx-in-django-web-application)
	- [Search, Filter, Paginate with HTMX](#search-filter-paginate-with-htmx)

This project is a Django web application for managing products, allowing users to filter products by category and search for specific items. The project utilizes the HTMX library for dynamic updates and interactions without full-page reloads.
My apologies for the misunderstanding. Let me explain the specific HTMX code used for form filtering and pagination in the project:

## Search, Filter, Paginate with HTMX

The application uses HTMX to submit form data and dynamically update the product list based on user selections. Here's how it works:

1. **User Interaction:** The user interacts with the filter form in `index.html`. This includes selecting categories, entering search queries, or changing filter options.

	```html
	<div >
		<!-- Filter Form -->
		<form id="filter-form"
				hx-get="{% url 'index' %}"
				hx-target="#product_list"
				hx-trigger="input change delay:300ms"
				hx-push-url="false"
				class="w-full dark:text-white">
		<!-- Form fields for search and category filtering -->
		<!-- Dynamic filter options -->
			<div id="dynamic_filter">
				{% for option_dict in options %}
					<!-- Filter option fieldsets -->
				{% endfor %}
			</div>
		</form>
		<!-- Product Cards -->
		<div id="product_list" >
			{% for product in page_obj %}
				<div >
					<h2>{{ product }}</h2>
					<p>{{ product.description }}</p>
					<p>{{ product.price }}</p>
					<p>Stock: {{ product.stock }}</p>
				</div>
			{% endfor %}
			{% include 'pagination/ssr_pagination.html' %}
		</div>
	</div>
	```

	`config\views.py`
	```python
	class HomeList(ListView):
		model = ProductVariant
		template_name = "product/productlist/index.html"

		def get_context_data(self, **kwargs):
			context = super().get_context_data(**kwargs)
			context['categories'] = Category.objects.all()
			context['options'] = []
			return context
	```

1. **HTMX Request:** When triggered by events like `input` or `change`, HTMX sends an asynchronous GET request to the server. The form data is included in the request. Key HTMX Attributes used in the form:
   - `hx-get`: Specifies the URL for the GET request.
   - `hx-target`: Identifies the element to update with the response (`#product_list`).
   - `hx-trigger`: Defines the events that trigger the request (e.g., `input change`).
   - `hx-push-url`: Optionally, whether to update the browser history (usually `false`).


2. **Server-Side Processing (views.py):**
   - `HomeList.get()` checks for the presence of the `HX-Request` header to identify an HTMX request.
   - It processes the form data, including:
     - Category selection (if any)
     - Search query (if any)
     - Selected filter options (using `request.GET.lists()`)
   - It filters the `ProductVariant` queryset based on the collected data.
   - It prepares the **html** response, which includes:
     - Updated product list HTML and Updated filter options (using `product_template_partial.html`)

	```html
	{% for product in page_obj %}
		<div >
			<h2>{{ product }}</h2>
			<p>{{ product.description }}</p>
			<p>{{ product.price }}</p>
			<p>Stock: {{ product.stock }}</p>
		</div>
	{% endfor %}
	<!-- Paginate -->
	{% include 'pagination/htmx_pagination.html' %}
	<div id="dynamic_filter" hx-swap-oob="true">
		{% for option_dict in options %}
			<fieldset>
				<legend class="font-bold">{{ option_dict.option }}</legend>
				{% for value in option_dict.values %}
					<div>
						<input type="checkbox"
							id="{{ value.name }}"
							name="{{ option_dict.option }}"
							value="{{ value.name }}"
							{% if value.checked %}checked{% endif %}>
						<label for="{{ value.name }}"
							{% if not value.available %}class="text-gray-300 dark:text-gray-600"{% endif %}>
							{{ value.name }}
						</label>
					</div>
				{% endfor %}
			</fieldset>
		{% endfor %}
	</div>
	```

3. **HTMX Response:** The server sends the response back to the client.
4. **Client-Side Updates (index.html):**
   - HTMX updates the `#product_list` div in `index.html` with all the content from `product_template_partial.html` **except** the  `#dynamic_filter` element with `hx-swap-oob="true"` which is swapped out as out-of-band content in the place of `#dynamic_filter` element in `index.html` filter form.

> Killing two birds with one stone.

> Notice the pagination is different from initial server side pagination logic. If dynamic filter is applied, the pagination also need to apply the filter. This is done by including the filter form data in the pagination request using `hx-include="#filter-form"`. So, the pagination uses `hx-get` to send a GET request to the server, **including the current URL with the desired page number appended and the filter form data using** `hx-include`. The server processes the request and filters the queryset based on the URL parameters and form data. It prepares the response, including updated product list HTML for the new page and updated filter options (if the selected page changes the available options). HTMX then updates the `#product_list` element with the new product list HTML and swaps out the `#dynamic_filter` element with the updated filter options (if necessary). See below for the pagination implementation.


`templates\pagination\htmx_pagination.html`

```html
<a hx-get="{{ request.path }}?page={{ page_obj.previous_page_number }}"
   hx-target="#product_list"
   hx-indicator="#loading-indicator"
   hx-include="#filter-form"
   class="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 dark:ring-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 focus:z-20 focus:outline-offset-0 cursor-pointer">
    <!-- Pagination link content -->
</a>
```

HTMX Logic Explanation:

- `hx-get`: The `hx-get` attribute specifies the URL for the GET request, which includes the current page's URL with the desired page number appended using the `page_obj.previous_page_number` or `page_obj.next_page_number` template variables.
- `hx-target`: The `hx-target` attribute identifies the HTML element (`#product_list`) that will be updated with the response from the server. This ensures that only the product list section is refreshed.
- `hx-indicator`: The `hx-indicator` attribute specifies the loading indicator element (`#loading-indicator`) that will be displayed while the request is being processed, providing visual feedback to the user.
- `hx-include`: The `hx-include` attribute includes the filter form (`#filter-form`) in the request, ensuring that any selected filters persist across pagination.

