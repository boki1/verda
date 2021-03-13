const socket = io.connect('http://' + document.domain + ':' + location.port);


$(document).ready(function() {
    let flag = true;
    $('#btnVerda').click(function() {
        if (flag) {
            flag = false;
            $('div.row').hide();
            $('.header').animate({ position: 'relative', height: '100%', width: '100%' }, 'slow');
            $('body').height($(window).height());
        } else {
            flag = true;
            $('div.row').show();
            $('.header').animate({ padding: '150px' }, 'slow');
        }
        $('#chat_and_message').slideToggle();
        $('.slideshow-container').slideToggle();
        $('#logoPic').slideToggle();
    });
});

socket.on('connect', function() {
    const input = $('input.message');
    $('form').on('submit', function(e) {
        e.preventDefault()
        let message = input.val().trim();
        if (message !== '') {
            socket.emit('send_usr_message', message)
            input.val('').focus()
        }
    });
})

socket.on('print_bot_message', function(message) {
    const chat = $('div#chat');
    chat.append('<br><br><br>' + '<div class="botMessage"><p>' + message + '</p></div>')
})

socket.on('print_usr_message', function(message) {
    const chat = $('div#chat');
    chat.append('<br><br><br>' + '<div class="usrMessage"><p>' + message + '</p></div>')
})