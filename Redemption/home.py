

# -*- coding: utf-8 -*-
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import requests


@csrf_exempt
def index(request):
    if request.method == "POST":
        r = requests.Requests(request)
        response = r.postRequest()
        return JsonResponse(response, safe=False)