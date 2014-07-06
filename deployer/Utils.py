from subprocess import call, PIPE


def run_silent(command):
    return True if call(command,
                        stdout=PIPE,
                        stderr=PIPE) == 0 else False


class CommandExecError(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)