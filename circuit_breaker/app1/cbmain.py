from datetime import datetime
import logging 


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

class RemoteCallFailedException(Exception):
    pass

class StateChoice:
    OPEN = "open"
    CLOSED = "close"
    HALF_OPEN = "half_open"

class CircuitBreaker:

    def __init__(self, function_name, exceptions, threshold, delay):
        
        self.function_name = function_name
        self.exceptions = exceptions
        self.threshold = threshold 
        self.delay = delay
        self.state = StateChoice.CLOSED
        self.last_attempt_time = None 
        self.failed_counts = 0

    def handle_closed_state(self, *args, **kwargs):
        logging.info(f"I'm in {self.state} state")
        allowed_exception = self.exceptions
        try:
            response = self.function_name(*args, **kwargs)
            logging.info(response)
            self.update_last_attempt_time()
            logging.info("Success: Remote call")
            return response
        except allowed_exception as e:
            logging.info("Failure: Remote call")
            self.failed_counts += 1
            self.update_last_attempt_time()
            if self.failed_counts >= self.threshold:
                self.set_state(StateChoice.OPEN) 
            raise RemoteCallFailedException from e 
        

    def handle_open_state(self, *args, **kwargs):
        logging.info(f"I'm in {self.state} state")
        current_time = datetime.utcnow().timestamp()

        if self.last_attempt_time + self.delay >= current_time:
            raise RemoteCallFailedException(f'Retry after {self.last_attempt_time+self.delay-current_time} secs')
    
        self.set_state(StateChoice.HALF_OPEN)
        allowed_exception = self.exceptions
        try:
            response = self.function_name(*args, **kwargs)
            logging.info("Success: Remote call")
            self.set_state(StateChoice.CLOSED)
            self.failed_counts = 0
            self.update_last_attempt_time()
            return response
        except allowed_exception as e:
            self.failed_counts += 1
            self.update_last_attempt_time()
            self.set_state(StateChoice.OPEN)
            raise RemoteCallFailedException from e

    def remote_call(self, *args, **kwargs):
        if self.state == StateChoice.CLOSED:
            return self.handle_closed_state(*args, **kwargs)
        if self.state == StateChoice.OPEN:
            return self.handle_open_state(*args, **kwargs)
        
    def set_state(self, state):
        previous_state, self.state = self.state, state
        logging.info(f"Changed state from {previous_state} to {self.state}")

    
    def update_last_attempt_time(self):
        self.last_attempt_time = datetime.utcnow().timestamp()