
from django.core.management.base import BaseCommand
from transformers import AutoModelForSequenceClassification, AutoTokenizer

class Command(BaseCommand):
    help = 'Download and save Hugging Face model locally'

    def handle(self, *args, **kwargs):
        model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        
        # 모델과 토크나이저 다운로드 및 로컬 저장
        self.stdout.write("Downloading and saving model...")
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        model.save_pretrained("./models/distilbert")
        tokenizer.save_pretrained("./models/distilbert")
        self.stdout.write(self.style.SUCCESS(f'Model and tokenizer saved locally in ./models/distilbert'))
