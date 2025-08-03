# chatmessages/management/commands/train_flag_model.py

from django.core.management.base import BaseCommand
from chatmessages.flag_classifier import FlagClassifier


class Command(BaseCommand):
    help = "Train a model to classify flagged messages."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("📚 Training model..."))

        classifier = FlagClassifier()
        classifier.train()

        self.stdout.write(self.style.SUCCESS("✅ Model trained and saved!"))
