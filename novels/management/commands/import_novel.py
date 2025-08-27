from django.core.management.base import BaseCommand
from novels.models import Novel, Chapter
from django.contrib.auth import get_user_model
import re #regular expressions
import requests

class Command(BaseCommand):
    help = "Import novel chapters from a text file or URL"

    def add_arguments(self, parser):
        parser.add_argument("source", type=str, help="File path or URL of the text")
        parser.add_argument("title", type=str, help="Novel title")
        parser.add_argument("author_id", type=int, help="Author user ID")
        parser.add_argument("--is-url", action="store_true", help="Indicate if the source is a URL")

    def handle(self, *args, **options):
        source = options["source"]
        title = options["title"]
        author_id = options["author_id"]
        is_url = options["is_url"]

        # Validate author
        User = get_user_model()
        try:
            author = User.objects.get(id=author_id)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Author with ID {author_id} does not exist"))
            return

        # Fetch text
        if is_url:
            self.stdout.write(f"Fetching text from URL: {source}")
            response = requests.get(source)
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f"Failed to fetch content from URL: {source}"))
                return
            text = response.text
        else:
            self.stdout.write(f"Reading text from file: {source}")
            with open(source, "r", encoding="utf-8") as f:
                text = f.read()

        # Clean Project Gutenberg header/footer (optional)
        text = re.sub(r"\*\*\* START OF.*?\*\*\*", "", text, flags=re.DOTALL)
        text = re.sub(r"\*\*\* END OF.*?\*\*\*", "", text, flags=re.DOTALL)

        # Split by chapters (handle variations like "Chapter 1", "CHAPTER I", etc.)
        chapters = re.split(r"(?:^|\n)(Chapter\s+\w+)", text, flags=re.IGNORECASE)
        print(chapters)

        if len(chapters) < 3:
            self.stdout.write(self.style.WARNING("No chapters found with pattern 'Chapter X'. Check the text format."))
            return

        # Create Novel
        novel = Novel.objects.create(title=title, author=author)

        # Add chapters
        order = 1
        for i in range(1, len(chapters), 2):
            ch_title = chapters[i].strip()
            ch_content = chapters[i+1].strip()
            Chapter.objects.create(
                novel=novel,
                number=order,
                title=ch_title,
                content=ch_content
            )
            order += 1

        self.stdout.write(self.style.SUCCESS(f"Imported {order-1} chapters for '{title}'"))
