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
            $('.header').animate({ position: 'auto', height: 'auto' }, 'slow');
        }
        $('#chat_and_message').slideToggle();
        $('.slideshow-container').slideToggle();
        $('#logoPic').slideToggle();
    });
});

$(function() {
  // this initializes the dialog (and uses some common options that I do)
  $("#dialog").dialog({autoOpen : false, modal : true, show : "blind", hide : "blind"});

  // next add the onclick handler
  $("#contactUs").click(function() {
    $("#dialog").dialog("open");
    return false;
  });
});


socket.on('connect', function() {
    const input = $('input.message');
    const checkbox = $('#text-to-speech-checkbox');

    $("#activate-speech-recognition").click(function() {
        if (checkbox.is(":checked")) {
            socket.emit('bot_speech_to_text_api', $('html')[0].lang)
            alert("speak now")
            console.log("Entered bot_speech_to_text_api mode");
        } else {
            socket.emit('usr_speech', $('html')[0].lang)
            alert("speak now")
            console.log("Entered usr_speech mode");
        }
    })

    $('form').on('submit', function(e) {
        e.preventDefault()
        let message = input.val().trim();
        if (message !== '') {
            socket.emit('send_usr_message', message)
            console.log("Entered send_usr_message mode");
            if (checkbox.is(":checked")) {
                socket.emit('bot_speech_api', message, $('html')[0].lang)
                console.log("Entered bot_speech_api mode");
            } else {
                socket.emit('send_bot_message', message, $('html')[0].lang)
                console.log("Entered send_bot_message mode");
                console.log($('html')[0].lang);
            }
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