class ServiceError(Exception):
    def __init__(self, code, message, status_code=400):
        super(ServiceError, self).__init__(self)
        self.code = code
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return "{0}: {1}".format(self.code, self.message)
