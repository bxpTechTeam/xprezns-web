document.addEventListener('DOMContentLoaded', () => {

      // Adding shadow property to the event card divs
      document.querySelectorAll('.event-card').forEach(div => {
            div.onmouseover = () => {
                  div.className += ' shadows p-3 mb-5 bg-white rounded';
            }
      })
      document.querySelectorAll('.event-card').forEach(div => {
            div.onmouseout = () => {
                  div.classList.remove('shadows', 'p-3', 'mb-5', 'bg-white', 'rounded');
            }
      })



      // Connect to the Web Socket
      var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

      // Configuring the apply buttons to register for the event when connected
      socket.on('connect', () => {
            // Each button should emit a 'register' event
            document.querySelectorAll('button').forEach(button => {
                  button.onclick = () => {
                        const event = button.dataset.event;
                        socket.emit('register', {'event': event});
                        button.disabled = true;
                  }
            })

      })

})
