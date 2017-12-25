from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
import json
import uuid

chatsize = 10
sessions = {}
conversations = {}
users = {}
# Create your views here.
class UserProfile:
	def __init__(self, userid):
		self.userid = userid
		self.conversationids = []

class Conversation:
	def __init__(self):
		self.chatmessages = []
		self.conversationid = str(uuid.uuid4())
		self.conversationname = "MyNewChat"
		self.convusers = []

class ChatMessage:
	def __init__(self, id, userid, text):
		self.id = id
		self.userid = userid
		self.text = text
		self.active = True

def getUserList(userid):
	result = []
	for key, value in users.items():
		if key != userid:
			result.append({"userid": key})
	return result

def addUserToList(userid):
	try:
		user = users[userid]
	except KeyError:
		users[userid] = UserProfile(userid)

def createNewConversation(userid, targetuserid):
	conv = Conversation()
	convid = conv.conversationid
	conv.convusers.append(userid)
	conv.convusers.append(targetuserid)
	users[userid].conversationids.append(convid)
	users[targetuserid].conversationids.append(convid)
	conversations[convid] = conv
	return convid

def getConversation(userid, targetuserid):
	exists = False
	try:
		userconvs = users[userid].conversationids
		for convid in userconvs:
			try:
				uids = conversations[convid].convusers
				if (userid in uids) and (targetuserid in uids):
					exists = True
					return convid
			except KeyError:
				a = 1
		if exists == False:
			convid = createNewConversation(userid, targetuserid)
			return convid
	except KeyError:
		convid = createNewConversation(userid, targetuserid)
		return convid

def getUserConversations(userid):
	result = []
	try:
		user = users[userid]
		try:
			for convid in user.conversationids:
				result.append({ "convid": convid,  "convname": conversations[convid].conversationname})
		except KeyError:
			a = 1
	except KeyError:
		a = 1
	return result

def addMessageToConversation(conversationid, msg):
	try:
		conversations[conversationid].chatmessages.append(msg)
	except KeyError:
		return

def getMessages(conversationid, n):
	conv = Conversation()
	conv.chatmessages = [msg for msg in conversations[conversationid].chatmessages if msg["active"]][-1*n:]
	return conv.__dict__
 
class ChatPageView(TemplateView):
	def get(self, request, **kwargs):
		userid = str(request.user)
		addUserToList(userid)
		if userid:
			return render(request, 'index.html', {"userid": userid, "userconversations": getUserConversations(userid), "peoplelist": getUserList(userid)})
		else:
			return render(request, 'registration/login.html', context=None)

class StartConversationPageView(TemplateView):
	def get(self, request, **kwargs):
		targetuser = request.GET["targetuserid"]
		userid = str(request.user)
		conversationid = getConversation(userid, targetuser)
		return HttpResponse(json.dumps({"conversationid": conversationid, "messages": getMessages(conversationid, chatsize)}), content_type="application/json")

class RefreshPeopleListView(TemplateView):
	def get(self, request, **kwargs):
		userid = str(request.user)
		if userid:
			return HttpResponse(json.dumps({"peoplelist": getUserList(userid)}), content_type="application/json")
		else:
			return HttpResponse('Login session expired, please log in', content_type="text/html")

class RefreshChatPageView(TemplateView):
	def get(self, request, **kwargs):
		userid = str(request.user)
		conversationid = request.GET['conversationid']
		if userid and conversationid:
			return HttpResponse(json.dumps(getMessages(conversationid, chatsize)), content_type="application/json")
		else:
			return HttpResponse('Login session expired, please log in', content_type="text/html")			

class SendMessage(TemplateView):
	def get(self, request, **kwargs):
		userid = request.GET["userid"]
		text = request.GET["text"]
		conversationid = request.GET['conversationid']
		addMessageToConversation(conversationid, ChatMessage(1, userid, text).__dict__)
		return HttpResponse(json.dumps(getMessages(conversationid, chatsize)), content_type="application/json")
	def post(self, request, **kwargs):
		userid = request.POST["userid"]
		text = request.POST["text"]
		conversationid = request.POST['conversationid']
		print("Conversationid", conversationid)
		addMessageToConversation(conversationid, ChatMessage(1, userid, text).__dict__)
		return HttpResponse(json.dumps(getMessages(conversationid, chatsize)), content_type="application/json")