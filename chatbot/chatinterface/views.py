from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
import json

# Create your views here.

class Conversation:
	def __init__(self):
		self.chatmessages = []

class ChatMessage:
	def __init__(self, id, userid, text):
		self.id = id
		self.userid = userid
		self.text = text
		self.active = True

conversation = Conversation()

def getMessages(n):
	conv = Conversation()
	conv.chatmessages = [msg for msg in conversation.chatmessages if msg["active"]][-1*n:]
	return conv.__dict__
'''conversation.chatmessages.append(ChatMessage(1, "ajay", "Hello").__dict__)
conversation.chatmessages.append(ChatMessage(1, "vinku", "Hi").__dict__)
conversation.chatmessages.append(ChatMessage(1, "ajay", "How are you?").__dict__)'''
 
class ChatPageView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'index.html', getMessages(10))

class ClearChatPageView(TemplateView):
	def get(self, request, **kwargs):
		for i in range(len(conversation.chatmessages)):
			conversation.chatmessages[i]["active"] = False
		return HttpResponse(json.dumps(getMessages(10)), content_type="application/json")

class SendMessage(TemplateView):
	def get(self, request, **kwargs):
		userid = request.get["userid"]
		text = request.get["text"]
		conversation.chatmessages.append(ChatMessage(1, userid, text).__dict__)
		return HttpResponse(json.dumps(getMessages(10)), content_type="application/json")
	def post(self, request, **kwargs):
		userid = request.POST["userid"]
		text = request.POST["text"]
		conversation.chatmessages.append(ChatMessage(1, userid, text).__dict__)
		return HttpResponse(json.dumps(getMessages(10)), content_type="application/json")