from django.contrib import admin
from .models import Document, Quiz, Flashcard, ChatHistory

admin.site.register(Document)
admin.site.register(Quiz)
admin.site.register(Flashcard)
admin.site.register(ChatHistory)
