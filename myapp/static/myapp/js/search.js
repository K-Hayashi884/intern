'use strict';
const searchSocket = new WebSocket(
    'ws://' 
    + window.location.host
    + '/ws/search/'
);

// 検索結果を画面に表示
searchSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const container = document. getElementById('container')
    const anchor = document.getElementsByClassName('link')
    let lst = []
    for (const elem of data.info) {
        lst.push(container.getElementsByClassName(`link ${elem}`)[0])
    };
    for (let i=0, len=anchor.length; i<len; i++) {
        anchor[i].style.display = 'None';
    };
    for (let i=0, len=lst.length; i < len; i++) {
        if (lst[i] !== void 0){ 
            lst[i].style.display = 'inline';
        };
    };
    
};

// エラー文をコンソールに表示
searchSocket.onclose = function(e) {
        console.error('Search socket closed unexpectedly');
    };

// 検索文をソケットに送信
document.querySelector('#chat-message-input').oninput = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const search = messageInputDom.value;
    searchSocket.send(JSON.stringify({
        'search': search
    }));
};