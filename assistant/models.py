from django.db import models
from django.contrib.auth.models import User
import json

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    summary_short = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-uploaded_at']

class Quiz(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='quizzes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    created_at = models.DateTimeField(auto_now_add=True)
    # Stores list of dicts: [{"question": "...", "options": ["A", "B", "C", "D"], "answer": "..."}]
    questions_json = models.TextField()

    @property
    def questions(self):
        try:
            return json.loads(self.questions_json)
        except Exception:
            return []

    def __str__(self):
        return f"Quiz for {self.document.title} by {self.user.username}"

    class Meta:
        ordering = ['-created_at']

class Flashcard(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='flashcards')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flashcards')
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Flashcard for {self.document.title} - {self.question[:30]}..."

    class Meta:
        ordering = ['created_at']

class ChatHistory(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chat_histories')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_histories')
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat for {self.document.title} - Q: {self.question[:30]}"

    class Meta:
        ordering = ['created_at']
