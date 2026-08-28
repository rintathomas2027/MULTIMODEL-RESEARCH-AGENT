from rest_framework import serializers
from .models import Document, ChatHistory

class DocumentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    file_size_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            'id', 'user', 'username', 'title', 'file', 'uploaded_at', 
            'extracted_text', 'summary', 'summary_short', 'file_size_formatted'
        ]
        read_only_fields = ['user', 'uploaded_at', 'extracted_text', 'summary', 'summary_short']

    def get_file_size_formatted(self, obj):
        if not obj.file:
            return "0 KB"
        try:
            size = obj.file.size
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"
            else:
                return f"{size / (1024 * 1024):.1f} MB"
        except Exception:
            return "Unknown"

class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ['id', 'document', 'user', 'question', 'answer', 'created_at']
        read_only_fields = ['user', 'created_at']
