from django.utils.deprecation import MiddlewareMixin
from django.utils.cache import patch_vary_headers


class CorsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response = {}
        # print(request.META.get('REMOTE_ADDR'))
        # patch_vary_headers(response, ["Origin"])
        if request.method == "OPTIONS":
            response["Access-Control-Allow-Origin"] = "*"
        return response
