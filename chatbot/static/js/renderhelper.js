function renderMessages(messageData){
	var list = document.getElementById('conversationlist');
	//list.innerHTML = "";
	for(var i=0; i<messageData["chatmessages"].length; i++){
		var msg = messageData["chatmessages"][i];
		var li = document.createElement('li');
		li.appendChild(document.createTextNode(msg["userid"] + ': ' + msg["text"]));
		list.appendChild(li);
	}
}

function clearChat(){
	$.ajax({
						url: "http://localhost:8000/clearchat/",
						type: "get",
						data: {
							'csrfmiddlewaretoken': '{{ csrf_token }}',
						},
						dataType: 'json',
						success: function(output) {
							console.log(output);
							document.innerHTML = output;
						}
					});
}

function clearTextArea(){
	var textarea = document.getElementById('chatinput');
	textarea.value = "";
}