from subprocess import call, PIPE, Popen
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_silent(command):
    return True if call(command,
                        stdout=PIPE,
                        stderr=PIPE) == 0 else False


class CommandExecError(Exception):
     def __init__(self, command, return_code, stderr):
         self.command = command
         self.return_code = return_code
         self.stderr = stderr

     def __str__(self):
         return repr("Error Trying to execute: %s; - "
                     "Error Code: #%s; - "
                     "ErrOutput: %s" % (self.command,
                                        self.return_code,
                                        self.stderr))


class ExecManager():

    def __init__(self):
        self.verbose = False

    def append_log(self, text, stdout=False):
        try:
            self.log += '\n%s' % text

            if self.verbose or stdout:
                print text

        except AttributeError:
            self.log = text

    def output_log(self):
        return self.log

    def _exec(self, command, echo_stdout=False):
        proc = Popen(args=command,
                     bufsize=-1,
                     stdout=PIPE,
                     stderr=PIPE)

        proc_return = proc.communicate()

        if proc.returncode == 0:
            self.append_log(proc_return[0])

            if self.verbose or echo_stdout:
                print proc_return[0]

        else:
            self.append_log(proc_return[1])

            raise CommandExecError(command=command,
                                   return_code=proc.returncode,
                                   stderr=proc_return[1])

class ConfigTemplate():

    def _parse(self, config_data):
        pass

    def __init__(self, config_name):
        self.name = config_name
        self.file = 'template/%s' % self.name

        with open(os.path.join(BASE_DIR, self.file), 'r') as file_handler:
            self.content = file_handler.read()

    def render(self, site_object):
        self.content = self.content % site_object

    def __str__(self):
        return self.content


