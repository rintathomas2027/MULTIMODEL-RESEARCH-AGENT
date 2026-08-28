from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
import json

from assistant.models import Document, Quiz, Flashcard, ChatHistory

class AIStudyAssistantTests(TestCase):
    def setUp(self):
        # Create user and client
        self.username = "teststudent"
        self.password = "password123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        
        # Create a sample document
        self.doc = Document.objects.create(
            user=self.user,
            title="Intro to Algorithms",
            extracted_text="Algorithms are step-by-step procedures for solving problems. Big O notation describes time complexity.",
            summary="This document explains basic algorithms and Big O time complexity."
        )

    def test_dashboard_redirects_for_anonymous_user(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

    def test_dashboard_renders_for_logged_in_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assistant/dashboard.html')
        self.assertContains(response, "Intro to Algorithms")

    @patch('assistant.views.generate_summary')
    def test_document_upload_notes(self, mock_generate_summary):
        mock_generate_summary.return_value = "Mocked Study Notes Summary."
        self.client.login(username=self.username, password=self.password)
        
        post_data = {
            'title': 'Operating Systems',
            'notes_text': 'An Operating System acts as an intermediary between a user and computer hardware.'
        }
        response = self.client.post(reverse('upload_document'), post_data)
        
        # Verify redirect to document detail
        new_doc = Document.objects.filter(title="Operating Systems").first()
        self.assertIsNotNone(new_doc)
        self.assertRedirects(response, reverse('document_detail', args=[new_doc.id]))
        self.assertEqual(new_doc.summary, "Mocked Study Notes Summary.")

    def test_document_detail_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('document_detail', args=[self.doc.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assistant/document_detail.html')
        self.assertContains(response, "Intro to Algorithms")

    @patch('assistant.views.answer_document_question')
    def test_chatbot_view(self, mock_answer):
        mock_answer.return_value = "Mocked answer: Big O describes the upper bound of run-time."
        self.client.login(username=self.username, password=self.password)
        
        post_data = {'question': 'What is Big O?'}
        response = self.client.post(
            reverse('document_chat', args=[self.doc.id]),
            data=json.dumps(post_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        resp_json = response.json()
        self.assertEqual(resp_json['question'], 'What is Big O?')
        self.assertEqual(resp_json['answer'], "Mocked answer: Big O describes the upper bound of run-time.")
        
        # Verify saved in DB
        chat_entry = ChatHistory.objects.filter(document=self.doc, question='What is Big O?').first()
        self.assertIsNotNone(chat_entry)

    @patch('assistant.views.generate_quizzes')
    def test_quiz_generation_and_grading(self, mock_gen_quizzes):
        mock_questions = [
            {
                "question": "What does Big O notation describe?",
                "options": ["Color", "Time complexity", "Weight", "Volume"],
                "answer": "Time complexity"
            }
        ]
        mock_gen_quizzes.return_value = mock_questions
        self.client.login(username=self.username, password=self.password)
        
        # First request generates the quiz
        response = self.client.get(reverse('document_quiz', args=[self.doc.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assistant/quiz.html')
        
        # Verify quiz created in DB
        quiz = Quiz.objects.filter(document=self.doc).first()
        self.assertIsNotNone(quiz)
        
        # Submit correct answer
        submit_data = {'question_0': 'Time complexity'}
        response = self.client.post(reverse('document_quiz', args=[self.doc.id]), submit_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your Quiz Results")
        self.assertContains(response, "1 / 1")
        self.assertContains(response, "Masterclass!")

    @patch('assistant.views.generate_flashcards')
    def test_flashcards_generation(self, mock_gen_flashcards):
        mock_cards = [
            {"question": "Big O", "answer": "Upper bound complexity description."}
        ]
        mock_gen_flashcards.return_value = mock_cards
        self.client.login(username=self.username, password=self.password)
        
        response = self.client.get(reverse('document_flashcards', args=[self.doc.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assistant/flashcards.html')
        
        # Verify card created in DB
        card = Flashcard.objects.filter(document=self.doc).first()
        self.assertIsNotNone(card)
        self.assertEqual(card.question, "Big O")

    @patch('assistant.views.roast_tech_stack')
    def test_roast_my_stack_view(self, mock_roast):
        mock_roast.return_value = {
            "roast": "Brutal mock roast: using Django for a static page? Classic.",
            "overengineering_score": 85,
            "wallet_bleeding_score": 90,
            "rdd_level": "High",
            "tech_badge": "CRUD Overcomplicator",
            "tips": ["Use SQLite", "Stop buying microservices", "Delete Kubernetes"]
        }
        
        # Get request renders form
        response = self.client.get(reverse('roast_my_stack'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assistant/roast.html')
        
        # Post request returns json
        post_data = {
            'frontend': 'React',
            'backend': 'Django',
            'database': 'PostgreSQL',
            'hosting': 'AWS',
            'bill': '150',
            'team_size': '2'
        }
        response = self.client.post(
            reverse('roast_my_stack'),
            data=json.dumps(post_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        resp_json = response.json()
        self.assertEqual(resp_json['tech_badge'], "CRUD Overcomplicator")
        self.assertEqual(resp_json['overengineering_score'], 85)
