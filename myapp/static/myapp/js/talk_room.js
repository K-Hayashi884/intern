'use strict';
const room_path = JSON.parse(document.getElementById('room_path').textContent);
const partner_id = JSON.parse(document.getElementById('partner').textContent);
const user_id = JSON.parse(document.getElementById('user').textContent)
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + room_path
    + '/'
);

chatSocket.onmessage = function(e) {
    const div_container = document.getElementById('container')
        
    const data = JSON.parse(e.data);

    let div_talkContainer = document.createElement('div');
    let div_time = document.createElement('div');
    let div_message = document.createElement('div');        
    div_time.classList.add('group');
    div_message.classList.add('message');
    div_message.classList.add('group');
    div_time.innerHTML = data.time_talkRoom;
    div_message.innerHTML = data.message;


    if (Number.parseInt(data.user_id) === Number.parseInt(user_id)) {
        div_talkContainer.classList.add('my-talk-container');
        div_message.classList.add('mine');

        div_talkContainer.appendChild(div_time);
        div_talkContainer.appendChild(div_message);
        div_container.appendChild(div_talkContainer);
    } else {
        let div_talkFrom = document.createElement('div');
        let talk_from = document.createTextNode(data.username);
        div_talkFrom.classList.add('talk-from')
        div_talkFrom.appendChild(talk_from);

        div_talkContainer.classList.add('your-talk-container');
        div_message.classList.add('yours');

        div_talkContainer.appendChild(div_message);
        div_talkContainer.appendChild(div_time);
        div_container.appendChild(div_talkFrom);
        div_container.appendChild(div_talkContainer);
    };

    let content = document.getElementById('content');
    content.scrollTo(0, content.scrollHeight);
};

chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('.submit-button').click();
    }
};

document.querySelector('.submit-button').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'user_id': user_id,
        'partner_id': partner_id,
        'message': message
    }));
    messageInputDom.value = '';
};

document.addEventListener('DOMContentLoaded', function() {
    let content = document.getElementById('content');
    content.scrollTo(0, content.scrollHeight);
})


