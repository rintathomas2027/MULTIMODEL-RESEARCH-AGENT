import os
import json
import re
import PyPDF2
import google.generativeai as genai
from django.conf import settings

# Configure Gemini API
def get_gemini_model():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-flash')

# Configure OpenAI API
def get_openai_client():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=api_key)
    except ImportError:
        return None

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file using PyPDF2.
    """
    text = ""
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            num_pages = len(reader.pages)
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        text = f"Error extracting text: {str(e)}"
    return text.strip()

def clean_json_response(text):
    """
    Cleans markdown code block wraps (like ```json ... ```) from a text response.
    """
    # Remove markdown code blocks if present
    match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text.strip()

def generate_summary(text_content):
    """
    Generates a professional study summary of the text content using OpenAI or Gemini.
    """
    prompt = (
        "You are an expert academic tutor. Please generate a comprehensive, structured, and beautifully "
        "formatted study summary of the following text content. Use clean Markdown formatting, "
        "including headers, bullet points, and key definitions. Focus on making it highly readable "
        "and clear for study purposes.\n\n"
        f"Text Content:\n{text_content[:20000]}" # Truncate to stay within reasonable token limit
    )
    
    client = get_openai_client()
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert academic tutor. Produce markdown summaries."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI summary error: {e}")
            # fallback to Gemini

    model = get_gemini_model()
    if not model:
        return "Neither OpenAI nor Gemini API keys are configured. Please check your .env file."
        
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Failed to generate summary: {str(e)}"

def answer_document_question(text_content, chat_history, question):
    """
    Answers a specific question about the document context and past chat history using OpenAI or Gemini.
    """
    # Format recent history
    history_str = ""
    for chat in chat_history[-5:]: # Include last 5 conversations for short-term memory
        history_str += f"Student: {chat.question}\nAI Tutor: {chat.answer}\n\n"

    prompt = (
        "You are a friendly, highly intelligent AI Study Assistant. Answer the student's question based strictly "
        "on the document context provided below. If the answer cannot be found in the context, use your general knowledge "
        "but clearly state that the information was not in the original document.\n\n"
        f"Document Context:\n{text_content[:20000]}\n\n"
        f"Recent Conversation History:\n{history_str}"
        f"New Student Question: {question}\n\n"
        "AI Answer:"
    )

    client = get_openai_client()
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a friendly, highly intelligent AI Study Assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI chat error: {e}")
            # fallback to Gemini

    model = get_gemini_model()
    if not model:
        return "Neither OpenAI nor Gemini API keys are configured. Please check your .env file."

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Failed to get response from Gemini: {str(e)}"

def generate_quizzes(text_content, count=5):
    """
    Generates structured MCQs (Quizzes) from the document using OpenAI or Gemini.
    Returns a Python list of question dicts.
    """
    prompt = (
        f"Generate {count} multiple choice questions (MCQs) for students to test their understanding of the text content below.\n"
        "You MUST return the output as a valid JSON array of objects. Do not include any text outside of the JSON block.\n"
        "Each object in the array must have exactly the following keys:\n"
        "1. 'question': The question text.\n"
        "2. 'options': An array of exactly 4 strings representing choices.\n"
        "3. 'answer': The exact string from the options array that represents the correct answer.\n\n"
        f"Text Content:\n{text_content[:15000]}"
    )

    client = get_openai_client()
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": "You are a quiz generator. You MUST return a JSON object with a 'quizzes' key containing the array of MCQs."},
                    {"role": "user", "content": prompt + "\n\nFormat the JSON response with key 'quizzes' containing the list of objects."}
                ]
            )
            data = json.loads(response.choices[0].message.content)
            if isinstance(data, list):
                return data
            if isinstance(data, dict):
                if 'quizzes' in data:
                    return data['quizzes']
                if isinstance(list(data.values())[0], list):
                    return list(data.values())[0]
            return []
        except Exception as e:
            print(f"Error generating quiz with OpenAI: {e}")
            # fallback to Gemini

    model = get_gemini_model()
    if not model:
        return []

    try:
        response = model.generate_content(prompt)
        cleaned = clean_json_response(response.text)
        data = json.loads(cleaned)
        if isinstance(data, list):
            return data
        return []
    except Exception as e:
        print(f"Error generating quiz: {e}")
        return []

def generate_flashcards(text_content, count=8):
    """
    Generates Q&A flashcards from the document using OpenAI or Gemini.
    Returns a Python list of flashcard dicts containing 'question' and 'answer'.
    """
    prompt = (
        f"Generate {count} Q&A flashcards from the text content below. Flashcards should be concise, focusing on core concepts, "
        "key definitions, and critical facts.\n"
        "You MUST return the output as a valid JSON array of objects. Do not include any text outside of the JSON block.\n"
        "Each object in the array must have exactly the following keys:\n"
        "1. 'question': A short, clear question or concept to define.\n"
        "2. 'answer': A concise, informative explanation or answer.\n\n"
        f"Text Content:\n{text_content[:15000]}"
    )

    client = get_openai_client()
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": "You are a flashcard generator. You MUST return a JSON object with a 'flashcards' key containing the array of flashcards."},
                    {"role": "user", "content": prompt + "\n\nFormat the JSON response with key 'flashcards' containing the list of objects."}
                ]
            )
            data = json.loads(response.choices[0].message.content)
            if isinstance(data, list):
                return data
            if isinstance(data, dict):
                if 'flashcards' in data:
                    return data['flashcards']
                if isinstance(list(data.values())[0], list):
                    return list(data.values())[0]
            return []
        except Exception as e:
            print(f"Error generating flashcards with OpenAI: {e}")
            # fallback to Gemini

    model = get_gemini_model()
    if not model:
        return []

    try:
        response = model.generate_content(prompt)
        cleaned = clean_json_response(response.text)
        data = json.loads(cleaned)
        if isinstance(data, list):
            return data
        return []
    except Exception as e:
        print(f"Error generating flashcards: {e}")
        return []

def roast_tech_stack(stack_details):
    """
    Queries OpenAI or Gemini to generate a highly sarcastic tech stack roast and optimization tips.
    Returns a Python dictionary with 'roast', 'overengineering_score', 'wallet_bleeding_score', 'rdd_level', 'tech_badge', and 'tips'.
    """
    prompt = (
        "You are an elite, highly opinionated, sarcastic, and witty senior software architect who has seen too many over-engineered startup failures.\n"
        "Analyze the following tech stack and cloud bill details, then generate a brutal, hilarious, yet deeply accurate roasting, along with some actually useful cost-optimization/simplification tips.\n\n"
        "Tech Stack Details:\n"
        f"- Frontend: {stack_details.get('frontend', 'Not specified')}\n"
        f"- Backend: {stack_details.get('backend', 'Not specified')}\n"
        f"- Database: {stack_details.get('database', 'Not specified')}\n"
        f"- Hosting/Infrastructure: {stack_details.get('hosting', 'Not specified')}\n"
        f"- Monthly Cloud Bill: ${stack_details.get('bill', '0')}\n"
        f"- Team Size: {stack_details.get('team_size', '1')} developers\n\n"
        "You MUST return the output as a valid JSON object. Do not include any text outside of the JSON block.\n"
        "The JSON object must have exactly the following keys:\n"
        "1. 'roast': A long, detailed, and highly sarcastic markdown text roasting their choices. Call out their resume-driven development, choice of complex databases for simple CRUD, or paying Vercel/AWS massive premiums.\n"
        "2. 'overengineering_score': An integer between 0 and 100 representing how needlessly complex the architecture is.\n"
        "3. 'wallet_bleeding_score': An integer between 0 and 100 representing how much money they are throwing away.\n"
        "4. 'rdd_level': A string representing their Resume-Driven Development level ('Low', 'Medium', 'High', 'Critical').\n"
        "5. 'tech_badge': A short, funny, 2-3 word moniker/archetype title (e.g. 'Vercel Paypig', 'Kubernetes Cultist', 'CRUD Overcomplicator', 'Premature Optimizer').\n"
        "6. 'tips': An array of exactly 3 bullet points containing realistic, direct, and actionable architectural or cost-saving suggestions.\n"
    )

    client = get_openai_client()
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": "You are an elite, highly opinionated, sarcastic, and witty senior software architect. You MUST return JSON matching the schema."},
                    {"role": "user", "content": prompt}
                ]
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error roasting stack with OpenAI: {e}")
            # fallback to Gemini

    model = get_gemini_model()
    if not model:
        return {
            "roast": "Your API Key is missing. I can't roast you if you're too broke to buy a Gemini or OpenAI API Key. Go fix your .env file.",
            "overengineering_score": 100,
            "wallet_bleeding_score": 100,
            "rdd_level": "Critical",
            "tech_badge": "API Broke-boy",
            "tips": ["Get an actual API key", "Stop using placeholder keys", "Clean up your local environment"]
        }

    try:
        response = model.generate_content(prompt)
        cleaned = clean_json_response(response.text)
        data = json.loads(cleaned)
        return data
    except Exception as e:
        print(f"Error in roast_tech_stack: {e}")
        return {
            "roast": f"The roast machine overheated while analyzing your terrible architecture. Error: {str(e)}",
            "overengineering_score": 50,
            "wallet_bleeding_score": 50,
            "rdd_level": "Medium",
            "tech_badge": "System Meltdown",
            "tips": ["Try resubmitting", "Check your Gemini API connection", "Maybe simplify your stack so it doesn't crash the AI"]
        }

def transcribe_audio_file(file_path):
    """
    Transcribes an audio file using OpenAI Whisper or Gemini 1.5 Flash.
    """
    client = get_openai_client()
    if client:
        try:
            with open(file_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                if transcript and transcript.text:
                    return transcript.text.strip()
        except Exception as e:
            print(f"Failed to transcribe with OpenAI Whisper: {e}")
            # fallback to Gemini

    model = get_gemini_model()
    if model:
        try:
            # Upload the file using the Gemini Files API
            audio_file = genai.upload_file(path=file_path)
            
            prompt = "You are a professional transcriber. Transcribe this audio file verbatim into clean text. Do not add any explanations, introductory text, or commentary."
            response = model.generate_content([prompt, audio_file])
            
            # Clean up the file from Gemini servers
            try:
                genai.delete_file(audio_file.name)
            except Exception:
                pass
                
            return response.text.strip()
        except Exception as e:
            return f"Failed to transcribe with Gemini: {str(e)}"

    return "Neither OpenAI nor Gemini API keys are configured. Please check your .env file."
