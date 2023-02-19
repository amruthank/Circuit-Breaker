from django.http import HttpResponse
import json


def success_endpoint(request):
    response = {'messgae': 'Call to this endpoint was a smashing success.'}
    return HttpResponse(json.dumps(response), status = 200, content_type = 'application/json')


def faulty_endpoint(request):
    print("This request will fail!")
    response = {'messgae': 'This request is going to fail!'}
    return HttpResponse(json.dumps(response), status = 500, content_type = 'application/json')