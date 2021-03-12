const socket = io.connect('http://' + document.domain + ':' + location.port);

$(document).ready(function(){
    $('#btnVerda').click( function() {
        $('#chat_and_message').slideToggle();
        $('#quote').slideToggle();
    });
});

socket.on('connect', function() {
    const input = $('input.message');
    $('form').on('submit', function (e) {
        e.preventDefault()
        let message = input.val().trim();
        if (message !== '') {
            socket.emit('send', message)
            input.val('').focus()
        }
    });
})
socket.on('print_message', function(message) {
    $('div#chat').append('<div><b>'+'You:'+'</b>'+message+'</div>')
})