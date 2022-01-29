var client_id = Date.now()

$("#ws-id").textContent = client_id;
var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
ws.onmessage = function(event) {
    var tbody = $('#user_list')
    var collection = eval(event.data)

    for (var i in eval(event.data)) {
        var item = collection[i]
        
        $("<tr>", {
            id: 'page_' + item.id
        }).prependTo("#user_list")

        $("<td>", {
            text: item.name
        }).appendTo("#page_" + item.id)

        $("<td>", {
            text: item.chapters_total
        }).appendTo("#page_" + item.id)

    }
};
function sendMessage(event) {
    ws.send('OK')
    event.preventDefault()
}


window.addEventListener('blur', sendMessage);
window.addEventListener('focus', sendMessage);