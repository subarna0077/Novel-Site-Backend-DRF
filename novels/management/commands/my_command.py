from django.core.management.base import BaseCommand

class Command(BaseCommand):

    ## help -> String shown when using --help
    help = 'Description of what this command does'

    ## handle is the main logic of the command
    def handle(self, *args, **kwargs):
        #Print output to console.
        self.stdout.write("Hello from custom command")