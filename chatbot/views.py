from django.shortcuts import render,redirect
from django.http import JsonResponse
import google.generativeai as genai
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
from dotenv import main
import os

main.load_dotenv()

# Create your views here.

def home(request):
    chats = Chat.objects.filter(user=request.user)
    if request.method == 'POST':
        message = request.POST.get('message')
        convo.send_message(message)
        # response = ask_openai(message)
        response = convo.last.text

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message':message, 'response':response})
    return render(request, 'chatbot.html', {'chats':chats})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {
                'error_message':error_message
            })
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('home')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message':error_message})
        else:
            error_message = 'Password Does Not Match'
            return render(request, 'register.html', {'error_message':error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')


genai.configure(api_key=os.getenv('api-key1'))

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", generation_config=generation_config, safety_settings=safety_settings)

convo = model.start_chat(history=[])




# print(convo.last.text)

# def ask_openai(message):
#     reponse = openai.completions.create(
#         model = "gpt-3.5-turbo-instruct",
#         prompt = message,
#         max_tokens=150,
#         n=1,
#         stop=None,
#         temperature=0.7,
#     )

    # answer = reponse.choices[0].text.strip()
    # return answer

    # test
    # test123




