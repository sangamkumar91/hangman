class Gallow:

    def __init__(self, status, token, rem, state):
        self.status = status
        self.token = token
        self.rem = rem
        self.state = state

    def __str__(self):
        return "Gallow:\n\tStatus: {}" \
               "\n\tToken: {}" \
               "\n\tRemaining Tries: {}" \
               "\n\tState: {}\n".format(self.status, self.token, self.rem, self.state)
