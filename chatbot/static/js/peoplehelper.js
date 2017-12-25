function startConversation(userid){
	$.ajax({
			url: "http://localhost:8000/startconversation/",
			type: "get",
			data: {
				'csrfmiddlewaretoken': '{{ csrf_token }}',
				'targetuserid': userid,
			},
			dataType: 'json',
			success: function(output) {
				console.log(output);
				$('#conversationid').val(output["conversationid"]);
				renderMessages(output["messages"]);
			}
	});
}

function renderPeopleList(peopleData){
	var list = document.getElementById('peoplenavigationlist');
	list.innerHTML = "";
	for(var i=0; i<peopleData.length; i++){
		var user = peopleData[i];
		var li = document.createElement('li');
		var butt = document.createElement('button');
		butt.value = user["userid"];
		butt.name = user["userid"];
		butt.appendChild(document.createTextNode(user["userid"]));
		butt.onclick = function() {
			startConversation(user["userid"]);
		};
		li.appendChild(butt);
		list.appendChild(li);
	}
}

setInterval(function(){
   	refreshPeopleList();
}, 3000);

function refreshPeopleList(){
	$.ajax({
			url: "http://localhost:8000/refreshpeople/",
			type: "get",
			data: {
				'csrfmiddlewaretoken': '{{ csrf_token }}',
			},
			dataType: 'json',
			success: function(output) {
				renderPeopleList(output["peoplelist"]);
			}
	});
}