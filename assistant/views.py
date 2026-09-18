import os
import re
from django.shortcuts import render, get_object_or_404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import json

from .models import Document, ChatHistory
from .serializers import DocumentSerializer, ChatHistorySerializer
from .services.doc_parser import extract_text_from_file, fetch_and_parse_url
from .services.chunker import chunk_text
from .services.vector_store import store_document_chunks, delete_document_chunks
from .services.rag_engine import (
    generate_rag_response,
    generate_paper_summary,
    explain_concept,
    generate_presentation_slides,
    generate_viva_questions,
    generate_citation_formats,
    generate_cross_paper_matrix,
    generate_scholarcast_podcast,
    generate_critical_roast,
    generate_formula_to_code
)
from .services.external_resolver import resolve_external_paper

def get_active_user(request):
    """
    Returns authenticated user, or retrieves/creates the default demo researcher so features are 100% accessible to anyone.
    """
    if request.user and request.user.is_authenticated:
        return request.user
    user, _ = User.objects.get_or_create(username='MCA_Evaluator', defaults={'email': 'evaluator@scholarpulse.ai'})
    return user

class FrontendAppView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return render(request, 'research_sphere.html')

class DocumentListCreateView(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        documents = Document.objects.all().order_by('-id')

        if query:
            documents = documents.filter(Q(title__icontains=query) | Q(extracted_text__icontains=query))
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = get_active_user(request)
        file_obj = request.FILES.get('file')
        url_input = (request.data.get('url') or request.data.get('url_input') or '').strip()
        title = (request.data.get('title') or '').strip()

        if not file_obj and not url_input:
            return Response({'error': 'Please provide a file or a valid web/PDF URL'}, status=status.HTTP_400_BAD_REQUEST)

        doc = None
        if url_input:
            try:
                parsed_res = fetch_and_parse_url(url_input, custom_title=title)
                final_title = title or parsed_res['title']
                filename = parsed_res['filename']
                content_file = ContentFile(parsed_res['file_bytes'], name=filename)

                doc = Document.objects.create(
                    user=user,
                    title=final_title,
                    file=content_file,
                    extracted_text=parsed_res['extracted_text']
                )
                chunks = chunk_text(parsed_res['extracted_text'])
                store_document_chunks(doc.id, chunks)

            except Exception as e:
                return Response({'error': f'URL Ingestion Error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        elif file_obj:
            if not title:
                title = file_obj.name

            doc = Document.objects.create(
                user=user,
                title=title,
                file=file_obj
            )

            try:
                ext = os.path.splitext(file_obj.name)[1].lower()
                text = extract_text_from_file(doc.file.path, ext)
                doc.extracted_text = text
                doc.save()

                chunks = chunk_text(text)
                store_document_chunks(doc.id, chunks)
            except Exception as e:
                print(f"Error processing uploaded file {doc.id}: {e}")

        serializer = DocumentSerializer(doc)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DocumentDetailDeleteView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        doc = get_object_or_404(Document, pk=pk)
        serializer = DocumentSerializer(doc)
        return Response(serializer.data)

    def delete(self, request, pk):
        doc = get_object_or_404(Document, pk=pk)
        delete_document_chunks(doc.id)
        doc.delete()
        return Response({'message': 'Document deleted successfully'}, status=status.HTTP_200_OK)

class RAGChatView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        doc = get_object_or_404(Document, pk=pk)
        user = get_active_user(request)
        question = request.data.get('question', '').strip()

        if not question:
            return Response({'error': 'Question cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

        answer = generate_rag_response(doc, question)

        # Save to chat history
        chat = ChatHistory.objects.create(
            document=doc,
            user=user,
            question=question,
            answer=answer
        )

        return Response({
            'id': chat.id,
            'question': question,
            'answer': answer,
            'created_at': chat.created_at
        })

    def get(self, request, pk):
        doc = get_object_or_404(Document, pk=pk)
        chats = ChatHistory.objects.filter(document=doc)
        serializer = ChatHistorySerializer(chats, many=True)
        return Response(serializer.data)

class SummarizeDocumentView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        doc = get_object_or_404(Document, pk=pk)
        mode = request.data.get('mode', 'detailed')
        summary = generate_paper_summary(doc, mode=mode)
        if mode == 'short':
            doc.summary_short = summary
        else:
            doc.summary = summary
        doc.save()
        return Response({
            'summary': doc.summary,
            'summary_short': doc.summary_short
        })

class ExplainModeView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        doc = get_object_or_404(Document, pk=pk)
        concept = request.data.get('concept', '').strip()
        academic_level = request.data.get('academic_level', 'MCA Student')

        if not concept:
            concept = doc.title

        explanation = explain_concept(doc, concept, academic_level)
        return Response({
            'concept': concept,
            'academic_level': academic_level,
            'explanation': explanation
        })

class PresentationAssistantView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        doc = get_object_or_404(Document, pk=pk)
        presentation_data = generate_presentation_slides(doc)
        return Response(presentation_data)

class VivaGeneratorView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        doc = get_object_or_404(Document, pk=pk)
        viva_data = generate_viva_questions(doc)
        return Response(viva_data)

# Module 9: Citation & Reference Intelligence (Mendeley / Zotero Killer)
class CitationGeneratorView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        doc = get_object_or_404(Document, pk=pk)
        citation_data = generate_citation_formats(doc)
        return Response(citation_data)

# Module 10: Cross-Paper Comparative Synthesis Matrix (Elicit / SciSpace Killer)
class CrossPaperMatrixView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        doc_ids = request.data.get('doc_ids', [])
        if not doc_ids or not isinstance(doc_ids, list):
            return Response({'error': 'Please select at least 2 documents for cross-synthesis.'}, status=status.HTTP_400_BAD_REQUEST)
        
        docs = Document.objects.filter(id__in=doc_ids)
        if len(docs) < 2:
            return Response({'error': 'Cross-paper matrix requires at least 2 valid documents from your workspace.'}, status=status.HTTP_400_BAD_REQUEST)
        
        matrix_data = generate_cross_paper_matrix(list(docs))
        return Response(matrix_data)

# Module 11: "ScholarCast" Dual-Host Audio Deep Dive (NotebookLM Killer)
class ScholarCastView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        doc = get_object_or_404(Document, pk=pk)
        podcast_data = generate_scholarcast_podcast(doc)
        return Response(podcast_data)

# Module 12: Reviewer #2 Critical Roast & Rigor Auditor
class CriticalRoastView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        doc = get_object_or_404(Document, pk=pk)
        roast_data = generate_critical_roast(doc)
        return Response(roast_data)

# Module 13: Multimodal Math Formula & Algorithm to Code Synthesizer
class FormulaCodeView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        doc = get_object_or_404(Document, pk=pk)
        formula_query = request.data.get('query', '').strip()
        result = generate_formula_to_code(doc, formula_query)
        return Response(result)

# Module 14: DOI & ArXiv 1-Click Paper Ingestion
class ExternalPaperResolverView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = get_active_user(request)
        identifier = request.data.get('identifier', '').strip()
        save_to_workspace = request.data.get('save_to_workspace', True)
        
        if not identifier:
            return Response({'error': 'DOI or ArXiv ID cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            paper_info = resolve_external_paper(identifier)
        except Exception as e:
            return Response({'error': f'Failed to resolve paper: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        if save_to_workspace:
            # Create a Document in user's library with the extracted abstract & info
            title = paper_info.get('title', 'Resolved Research Paper')
            abstract_text = paper_info.get('abstract', '')
            full_text = f"Title: {title}\n\nAuthors: {', '.join(paper_info.get('authors', []))}\nPublished: {paper_info.get('published_date', '')}\nIdentifier: {paper_info.get('identifier', '')}\n\nAbstract:\n{abstract_text}"

            # Create file
            content_file = ContentFile(full_text.encode('utf-8'), name=f"{re.sub(r'[^a-zA-Z0-9]', '_', title)[:30]}.txt")
            doc = Document.objects.create(
                user=user,
                title=title,
                file=content_file,
                extracted_text=full_text,
                summary_short=abstract_text[:400]
            )

            # Store vectors for RAG
            try:
                chunks = chunk_text(full_text)
                store_document_chunks(doc.id, chunks)
            except Exception as e:
                print(f"Vector store error for external paper: {e}")

            doc_serializer = DocumentSerializer(doc)
            return Response({
                'metadata': paper_info,
                'document': doc_serializer.data,
                'message': f"Paper '{title}' successfully resolved and imported into your workspace!"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({'metadata': paper_info})
