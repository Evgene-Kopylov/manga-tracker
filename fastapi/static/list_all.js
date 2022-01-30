var ws = new WebSocket(`ws://localhost:8000/ws/list_all`);
ws.onmessage = function(event) {
    var tbody = $('#user_list')
    var collection = eval(event.data)

    for (var i in eval(event.data)) {
        var item = collection[i]
        
        if ($('#page_' + item.id).length) {
            console.log('ok')
        } else {
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
    }
};
function sendMessage(event) {
    ws.send('OK')
    event.preventDefault()
}


window.addEventListener('blur', sendMessage);
window.addEventListener('focus', sendMessage);