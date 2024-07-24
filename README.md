# Django HTMX Partial Redirect Middleware

This Django middleware redirects direct accesses to HTMX partial views (e.g., modal content) to a full page, passing the original URL as a 'partial_url' parameter.

## Problem:

When a user directly accesses a URL (via address bar) that's meant to render a partial HTML view (with HTMX):
1. They see only the partial content (e.g., a login form).
2. The page lacks full context (CSS, JS, surrounding layout).

Example: Accessing `/login/` shows only a `<form>` without styling or proper page structure.

## Solution:

This middleware:
1. Intercepts direct access to partial view URLs.
2. Redirects to a full page URL of your choice.
3. Passes the original partial URL as a parameter.

## Result:

1. User sees a complete, properly styled page.
2. The partial content (e.g., login form) can be lazy-loaded via HTMX by adding a check for the `partial_url` parameter in the template.
3. Partial content appears as intended (e.g., in a modal).

## How it works:

1. User accesses `/login/` directly.
2. Middleware redirects to `/?partial_url=/login/`.
3. Full page loads with HTMX trigger: `hx-trigger="load"`.
4. HTMX loads `/login/` content into the page (e.g., as a modal).
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
   HTMX_PARTIAL_VIEWS = ['login', 'signup', 'logout']  # List of view names to be treated as partial
   HTMX_PARTIAL_VIEWS_REDIRECT_URL = '/'  # URL to redirect to when accessing partial views directly
   ```

## Usage

In your base template, add this snippet at the end of the `<body>` tag:

```html
{% if request.GET.partial_url %}
   <div hx-trigger="load"
        hx-get="{{ request.GET.partial_url }}"
        hx-swap="outerHTML">
   </div>
{% endif %}
```

Create a base modal template (e.g., `modal_base.html`):

```html
<dialog hx-on::load="this.showModal()"
        hx-on:close="this.remove()">

   <!-- Backdrop (click to close) -->
   <form method="dialog" class="fixed inset-0 cursor-pointer -z-10" hx-on:click="this.submit()"></form>

   <!-- Modal content -->
   <div id="modal-content">
      {% block content %}{% endblock %}
   </div>
</dialog>
```

In your partial views (e.g., login, signup), extend the modal base:

```html
{% extends "modal_base.html" %}

{% block content %}
<!-- Your form or content here -->
{% endblock %}
```

## How it works

The middleware intercepts requests to the specified HTMX partial views when they're accessed directly (not via HTMX). It then redirects to the specified full page URL, adding the original partial view URL as a `partial_url` parameter.

## Configuration

- `HTMX_PARTIAL_VIEWS`: A list of view names to be treated as HTMX partial views.
- `HTMX_PARTIAL_VIEWS_REDIRECT_URL`: The URL to redirect to when a partial view is accessed directly.

## Notes

If you don't want users to see the parameter in the URL (e.g. `/?partial_url=/login/`), you can use the `hx-push-url` attribute to update the URL in the address bar:

```html
<div hx-trigger="load"
     hx-get="{{ request.GET.partial_url }}"
     hx-swap="outerHTML"
     hx-push-url="/">
</div>
```

## License

This project is licensed under the MIT License.