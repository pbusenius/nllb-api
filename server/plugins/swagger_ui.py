from pathlib import Path
from os import environ
from typing import Any

from litestar import Request
from litestar.openapi.plugins import SwaggerRenderPlugin


class CustomSwaggerRenderPlugin(SwaggerRenderPlugin):
    """
    Summary
    -------
    Custom Swagger UI render plugin that uses bundled CSS/JS assets
    and matches the whisper-asr-webservice look and feel
    """

    def __init__(self, server_root_path: str = "/api") -> None:
        super().__init__()
        self.server_root_path = server_root_path
        
        # Check if swagger-ui assets exist and override CSS/JS URLs
        # Assets are in $HOME/swagger-ui-assets in Docker container
        home_dir = Path(environ.get("HOME", str(Path.home())))
        swagger_ui_assets_path = home_dir / "swagger-ui-assets"
        if swagger_ui_assets_path.exists():
            css_file = swagger_ui_assets_path / "swagger-ui.css"
            js_file = swagger_ui_assets_path / "swagger-ui-bundle.js"
            if css_file.exists() and js_file.exists():
                # Override the CSS and JS URLs to use local assets
                self.css_url = f"{self.server_root_path}/swagger-ui-assets/swagger-ui.css"
                self.js_url = f"{self.server_root_path}/swagger-ui-assets/swagger-ui-bundle.js"

    def render(self, request: Request, openapi_schema: dict[str, Any]) -> bytes:
        """
        Summary
        -------
        Render Swagger UI HTML with custom configuration to match whisper-asr-webservice

        Parameters
        ----------
        request (Request)
            the request object

        openapi_schema (dict[str, Any])
            the OpenAPI schema

        Returns
        -------
        html (bytes)
            the Swagger UI HTML
        """
        from litestar.config.csrf import CSRFConfig
        from litestar.serialization import encode_json

        def create_request_interceptor(csrf_config: CSRFConfig | None) -> bytes:
            if not csrf_config or csrf_config.cookie_httponly:
                return b""

            def _get_cookie_value_or_undefined(cookie_name: str) -> str:
                return f"document.cookie.split('; ').find(row => row.startsWith('{cookie_name}='))?.split('=')[1]"

            return f"""
                  requestInterceptor: (request) => {{
                    const csrf_token = {_get_cookie_value_or_undefined(csrf_config.cookie_name)};

                    if (csrf_token !== undefined) {{
                      request.headers['{csrf_config.header_name}'] = csrf_token;
                    }}

                    return request;
                  }},""".encode()

        # Remove servers from schema to hide servers dropdown (like whisper-asr-webservice)
        schema_without_servers = openapi_schema.copy()
        schema_without_servers.pop("servers", None)

        # Custom CSS to hide servers dropdown and ensure openapi.json link is visible
        custom_style = """
            <style>
              /* Hide servers dropdown - multiple selectors for different Swagger UI versions */
              .swagger-ui .scheme-container,
              .swagger-ui .servers,
              .swagger-ui .servers-container,
              .swagger-ui select[data-name="servers"],
              .swagger-ui label[for="servers"],
              .swagger-ui .opblock-section label:has(+ select[data-name="servers"]) {
                display: none !important;
              }
              /* Style for openapi.json link */
              .swagger-ui .info .title {
                display: flex;
                align-items: center;
                gap: 1rem;
              }
              .swagger-ui .info .title a {
                display: inline-block;
                font-size: 0.9em;
                color: #3b49df;
                text-decoration: none;
              }
              .swagger-ui .info .title a:hover {
                text-decoration: underline;
              }
            </style>
        """

        # Get the openapi.json URL for the download link
        openapi_json_url = f"{self.server_root_path}/schema/openapi.json"

        head = f"""
          <head>
            <title>{openapi_schema["info"]["title"]}</title>
            {self.favicon}
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="{self.css_url}" rel="stylesheet">
            <script src="{self.js_url}" crossorigin></script>
            <script src="{self.standalone_preset_js_url}" crossorigin></script>
            {custom_style}
            {self.style}
          </head>
        """

        body = b"".join(
            [
                b"""
            <body>
              <div id='swagger-container'/>
                <script type='text/javascript'>
                const ui = SwaggerUIBundle({
                  spec: """,
                self.render_json(request, schema_without_servers),
                b""",
                  dom_id: '#swagger-container',
                  deepLinking: true,
                  showExtensions: true,
                  showCommonExtensions: true,
                  defaultModelsExpandDepth: -1,
                  presets: [
                      SwaggerUIBundle.presets.apis,
                      SwaggerUIBundle.SwaggerUIStandalonePreset
                  ],""",
                create_request_interceptor(request.app.csrf_config) if hasattr(request.app, "csrf_config") and request.app.csrf_config else b"",
                b"""
                })
            ui.initOAuth(""",
                encode_json(self.init_oauth),
                b""")
            </script>
            <script type='text/javascript'>
            // Override the title to include openapi.json link (like FastAPI) and hide servers dropdown
            const openapiJsonUrl = """,
                encode_json(openapi_json_url),
                b""";
            
            function addOpenApiLink() {
              // Try multiple selectors to find the title element
              const selectors = [
                '.swagger-ui .info .title',
                '.swagger-ui .info h2',
                '.swagger-ui .info h2.title',
                '.swagger-ui .info h2.main-title',
              ];
              
              let titleElement = null;
              for (const selector of selectors) {
                titleElement = document.querySelector(selector);
                if (titleElement) break;
              }
              
              if (titleElement) {
                // Check if link already exists
                const existingLink = titleElement.querySelector('a[href="' + openapiJsonUrl + '"]') || 
                                    (titleElement.parentElement && titleElement.parentElement.querySelector('a[href="' + openapiJsonUrl + '"]'));
                
                if (!existingLink) {
                  // Get the text content
                  const titleText = titleElement.textContent || titleElement.innerText || '';
                  // Add the link after the title text
                  const link = document.createElement('a');
                  link.href = openapiJsonUrl;
                  link.textContent = '/openapi.json';
                  link.style.marginLeft = '1rem';
                  link.style.fontSize = '0.9em';
                  link.style.color = '#3b49df';
                  link.style.textDecoration = 'none';
                  link.addEventListener('mouseenter', function() { this.style.textDecoration = 'underline'; });
                  link.addEventListener('mouseleave', function() { this.style.textDecoration = 'none'; });
                  
                  // Try to append as sibling first, then as child
                  if (titleElement.parentElement) {
                    titleElement.parentElement.insertBefore(link, titleElement.nextSibling);
                  } else {
                    titleElement.appendChild(document.createTextNode(' '));
                    titleElement.appendChild(link);
                  }
                }
              }
            }
            
            function hideServers() {
              // Try various selectors
              const selectors = [
                '.swagger-ui .scheme-container',
                '.swagger-ui .servers',
                '.swagger-ui .servers-container',
                '.swagger-ui select[data-name="servers"]',
                '.swagger-ui label:has(+ select)',
                '.swagger-ui label[role="label"]:has(combobox)',
              ];
              selectors.forEach(function(selector) {
                try {
                  const elements = document.querySelectorAll(selector);
                  elements.forEach(function(el) {
                    if (el.textContent && el.textContent.includes('/api')) {
                      el.style.display = 'none';
                    }
                  });
                } catch (e) {
                  // Ignore errors for unsupported selectors
                }
              });
              
              // Also try to find and hide the combobox/label combo
              const labels = document.querySelectorAll('.swagger-ui label[role="label"]');
              labels.forEach(function(label) {
                const combobox = label.querySelector('combobox');
                if (combobox && combobox.getAttribute('name') === '/api') {
                  label.style.display = 'none';
                  if (label.parentElement) {
                    label.parentElement.style.display = 'none';
                  }
                }
              });
            }
            
            // Run immediately and on load
            addOpenApiLink();
            hideServers();
            
            window.addEventListener('load', function() {
              addOpenApiLink();
              hideServers();
              setTimeout(addOpenApiLink, 50);
              setTimeout(hideServers, 50);
              setTimeout(addOpenApiLink, 100);
              setTimeout(hideServers, 100);
              setTimeout(addOpenApiLink, 300);
              setTimeout(hideServers, 300);
              setTimeout(addOpenApiLink, 500);
              setTimeout(hideServers, 500);
              setTimeout(addOpenApiLink, 1000);
              setTimeout(hideServers, 1000);
            });
            
            // Also use MutationObserver to catch dynamic changes
            if (window.MutationObserver) {
              const observer = new MutationObserver(function(mutations) {
                let shouldRun = false;
                for (let i = 0; i < mutations.length; i++) {
                  const mutation = mutations[i];
                  if (mutation.addedNodes.length > 0) {
                    for (let j = 0; j < mutation.addedNodes.length; j++) {
                      const node = mutation.addedNodes[j];
                      if (node.nodeType === 1 && (
                        (node.classList && node.classList.contains('swagger-ui')) ||
                        (node.querySelector && node.querySelector('.swagger-ui .info'))
                      )) {
                        shouldRun = true;
                        break;
                      }
                    }
                  }
                }
                if (shouldRun) {
                  setTimeout(addOpenApiLink, 10);
                  setTimeout(hideServers, 10);
                }
              });
              observer.observe(document.body, {
                childList: true,
                subtree: true
              });
            }
            </script>
          </body>
        """,
            ]
        )

        return b"".join([b"<!DOCTYPE html><html>", head.encode(), body, b"</html>"])

