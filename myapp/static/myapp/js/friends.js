'use strict';
const container = document.getElementById('container')
var room_path_elements = document.getElementsByClassName('room_path')
var chatSocket = []
var room_path = []
for  (var i = 0, len = room_path_elements.length; i < len; i++) {
    room_path.push(JSON.parse(room_path_elements[i].textContent));
    chatSocket.push(new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + room_path[i]
    + '/'));
    chatSocket[i].onmessage = function(e) {
        var data = JSON.parse(e.data);
        var div_message = document.getElementsByClassName(`message ${data.room_path}`)[0];
        var div_time = document.getElementsByClassName(`time ${data.room_path}`)[0];
            
        div_message.textContent = data.display_message;
        div_time.textContent = data.time_friend;
        var anchor = document.getElementsByClassName(`link ${data.room_path}`)[0];
        anchor.lastElementChild.classList.add('blue');

        container.insertBefore(anchor, container.firstChild);
    };
};