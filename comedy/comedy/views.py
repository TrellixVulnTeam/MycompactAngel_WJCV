from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
chatbot = ChatBot("My Aangel")
chatbot.set_trainer(ListTrainer)
#chatbot.train("chatterbot.corpus.spanish")
chatbot.train([
    "Hola",
    "Hola ¿Cómo estás?",
    "Estoy bien y tu ¿Cómo estás?",
    "Me encuentro muy bien gracias a Dios cuentame ¿Cómo estas hoy?",
    "Estoy triste o un poco mal",
    "Lamento mucho eso ¿Qué te ocurre?",
    "Suicidio o maltrato",
    "Si deseas hablar puedes llamarme al 106 para que se comuniquen contigo",
    "Gracias",
    "Muchas gracias a ti por hablar conmigo, no dudes en probar nuestros servicios de chat",
    "Me siento con ansiedad",
    "Entiendo, te recomiendo que escuches esta meditación guiada sobre la ansiedad https://www.youtube.com/watch?v=GNiZuPKWHHI",
])
# Train based on the english corpus

#Already trained and it's supposed to be persistent
#chatbot.train("chatterbot.corpus.english")

@csrf_exempt
def get_response(request):
	response = {'status': None}

	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))
		message = data['message']

		chat_response = chatbot.get_response(message).text
		response['message'] = {'text': chat_response, 'user': False, 'chat_bot': True}
		response['status'] = 'ok'

	else:
		response['error'] = 'no post data found'

	return HttpResponse(
		json.dumps(response),
			content_type="application/json"
		)




def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('home')
	else:
		form = UserCreationForm()
	return render(request, 'signup.html', {'form': form})


def check_my_meditations(request, template_name="meditation_iist.html"):
	context = {'title': 'Your video list'}
	return render_to_response(template_name, context)

def select_help(request, template_name="select_plan.html"):
	context = {'title': 'Select your plan'}
	return render_to_response(template_name, context)

def home(request, template_name="home.html"):
	context = {'title': 'Chatbot Version 1.0'}
	return render_to_response(template_name, context)
