function renderMessages(messageData){
	var list = document.getElementById('conversationlist');
	list.innerHTML = "";
	for(var i=0; i<messageData["chatmessages"].length; i++){
		var msg = messageData["chatmessages"][i];
		var li = document.createElement('li');
		li.appendChild(document.createTextNode(msg["userid"] + ': ' + msg["text"]));
		list.appendChild(li);
	}
}

setInterval(function(){
   	refreshChat();
}, 3000);

function refreshChat(){
	$.ajax({
			url: "/refreshchat/",
			type: "get",
			data: {
				'csrfmiddlewaretoken': '{{ csrf_token }}',
				'conversationid': $('#conversationid').val(),
			},
			dataType: 'json',
			success: function(output) {
				console.log(output);
				renderMessages(output);
			}
	});
}

function clearChat(){
	$.ajax({
			url: "/clearchat/",
			type: "get",
			data: {
				'csrfmiddlewaretoken': '{{ csrf_token }}',
			},
			dataType: 'json',
			success: function(output) {
				console.log(output);
				renderMessages(output);
			}
	});
}

function clearTextArea(){
	var textarea = document.getElementById('chatinput');
	textarea.value = "";
}