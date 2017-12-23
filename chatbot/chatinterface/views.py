from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

conversation = {"chatmessages": [{"id": 1, "text": "Hello", "userid": "ajay"}, {"id": 1, "text": "Hi", "userid": "vinku"}, {"id": 1, "text": "How are you?", "userid": "ajay"}]}

class ChatPageView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'index.html', conversation)

class SendMessage(TemplateView):
	def get(self, request, **kwargs):
		userid = request.get["userid"]
		text = request.get["text"]
		conversation["chatmessages"].append({"id": 1, "text": text, "userid": userid})
		return render(request, 'index.html', conversation)
	def post(self, request, **kwargs):
		userid = request.POST["userid"]
		text = request.POST["text"]
		conversation["chatmessages"].append({"id": 1, "text": text, "userid": userid})
		return render(request, 'index.html', conversation)