'use strict';
const searchSocket = new WebSocket(
    'ws://' 
    + window.location.host
    + '/ws/search/'
);

searchSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const container = document.getElementById('container')
    const anchor = document.getElementsByClassName('link')
    let lst = []
    for (const elem of data.info) {
        lst.push(container.getElementsByClassName(`link ${elem}`)[0])
    }
    for (let i=0, len=anchor.length; i<len; i++) {
        anchor[i].style.display = 'None';
    }
    for (let i=0, len=lst.length; i < len; i++) {
        if (lst[i] !== void 0){ 
            lst[i].style.display = 'inline';
        };
    }
    
    let info = data.info;
    

};

searchSocket.onclose = function(e) {
        console.error('Search socket closed unexpectedly');
    };

document.querySelector('#chat-message-input').oninput = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const search = messageInputDom.value;
    searchSocket.send(JSON.stringify({
        'search': search
    }));
};