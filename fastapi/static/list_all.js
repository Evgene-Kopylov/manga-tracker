var client_id = Date.now()
document.querySelector("#ws-id").textContent = client_id;
var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
ws.onmessage = function(event) {
    var tbody = document.getElementById('user_list')
    var collection = eval(event.data)

    for (var i in eval(event.data)) {
        var item = collection[i]
        var item_line = document.createElement('tr')
        item_line.setAttribute('id', 'page_' + item.id)

        var column_0 = document.createElement('td')
        column_0.innerText = item.name
        item_line.appendChild(column_0)

        var column_1 = document.createElement('td')
        column_1.innerText = item.chapters_total
        item_line.appendChild(column_1)

        tbody.prepend(item_line)
    }
};
function sendMessage(event) {
    ws.send('OK')
    event.preventDefault()
}


window.addEventListener('blur', sendMessage);
window.addEventListener('focus', sendMessage);