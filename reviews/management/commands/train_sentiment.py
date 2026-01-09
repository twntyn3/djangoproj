
from django.core.management.base import BaseCommand
from reviews.ml import train_tiny_model

class Command(BaseCommand):
    help = "Train and save a tiny sentiment SVM (demo)."

    def handle(self, *args, **options):
        train_tiny_model()
        self.stdout.write(self.style.SUCCESS("Tiny sentiment model trained and saved."))
