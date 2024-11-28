const sendMsgBut = document.getElementById('sendMsgBut')
function addMessage(username, msg) {
					const li = document.createElement('li');
					const spanUsername = document.createElement("span")
					const spanMessage = document.createElement("span")
					const chatmsgs = document.getElementById('chatmsgs')

					spanUsername.classList += "username"
					spanUsername.textContent = `${username}: `

					spanMessage.classList += "message"
					spanMessage.textContent = msg

					li.appendChild(spanUsername)
					li.appendChild(spanMessage)
					
					chatmsgs.appendChild(li);
					chatmsgs.scrollTop = chatmsgs.scrollHeight;
}
// socketIO logic
var socket = io();
socket.on('message', (data) => {
					console.log(data.message);
					addMessage(data.username, data.message)
});
socket.on('connect', function() {
					socket.emit('message', {data: 'I\'m connected!'});
});
sendMsgBut.onclick = async () => {
					const username = document.getElementById('usernamefield').value
					const message = document.getElementById('message').value
					socket.emit('message', {username: username, message});
}
