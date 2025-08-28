from django.core.management.base import BaseCommand
import re
class Command(BaseCommand):

    ## help -> String shown when using --help
    help = 'Description of what this command does'

    ## handle is the main logic of the command
    def handle(self, *args, **kwargs):
        #Print output to console.
        self.stdout.write("Hello from custom command")
        text = "Chapter I: Introduction\nChapter II: Getting Started\nChapter III: Advanced Topics"
        pattern = r"Chapter\s+\w+"
        matches = re.findall(pattern,text)
        print(matches)