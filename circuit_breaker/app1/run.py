from snippets import *
from cbmain import *

obj = CircuitBreaker(make_request, exceptions=(Exception,), threshold=2, delay=10)
obj.remote_call(success_endpoint)
obj.remote_call(faulty_endpoint)
obj.remote_call(faulty_endpoint)
obj.remote_call(faulty_endpoint)

