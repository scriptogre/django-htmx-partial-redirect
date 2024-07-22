# Django Partial View Redirect Middleware

This Django middleware redirects direct accesses to partial views (e.g., HTMX modal content) to a full page, passing the original URL as a `partial_url` parameter.

## Installation

1. Install the package:
   ```
   pip install django-htmx-partial-redirect
   ```

2. Add the middleware to your `MIDDLEWARE` in `settings.py`:
   ```python
   MIDDLEWARE = [
       # ...
       'django_htmx_partial_redirect.middleware.HTMXPartialViewRedirectMiddleware',
       # ...
   ]
   ```

3. Configure the settings in your `settings.py`:
   ```python
   HTMX_PARTIAL_VIEWS = ['login', 'signup', 'todos:add']  # List of view names to be treated as partial
   HTMX_PARTIAL_VIEWS_REDIRECT_URL = '/home/'  # URL to redirect to when accessing partial views directly
   ```

## Usage

In your view or template, you can check for the `partial_url` parameter and load the partial content using lazy loading (via `hx-trigger="load"`):

```html
{% if request.GET.partial_url %}
    <div hx-get="{{ request.GET.partial_url }}"
         hx-target="body"
         hx-swap="beforeend"
         hx-trigger="load">
    </div>
{% endif %}
```

## How it works

The middleware intercepts requests to the specified partial views when they're accessed directly (not via HTMX). It then redirects to the specified full page URL, adding the original partial view URL as a `partial_url` parameter.

## Configuration

- `HTMX_PARTIAL_VIEWS`: A list of view names to be treated as partial views.
- `HTMX_PARTIAL_VIEWS_REDIRECT_URL`: The URL to redirect to when a partial view is accessed directly.

## License

This project is licensed under the MIT License.