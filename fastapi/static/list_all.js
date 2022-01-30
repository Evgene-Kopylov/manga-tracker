var ws = new WebSocket(`ws://localhost:8000/ws/list_all`);
ws.onmessage = function(event) {
    var collection = eval(event.data)

    for (var i in eval(event.data)) {
        var item = collection[i]
        
        if ($('#page_' + item.id).length) {
            console.log('item already present')
        } else {
            $("<tr>", {
                id: 'page_' + item.id
            }).prependTo("#user_list")

            $("<td>", {
                text: item.name
            }).appendTo("#page_" + item.id)

            $("<td>", {
                id: "edit_name_page_" + item.id,
            }).appendTo("#page_" + item.id)

                $("<button>", {
                    id: '#edit_page',
                    class: 'edit_name',
                    value: item.id,
                    text: '/'
                }).appendTo("#edit_name_page_" + item.id)

            $("<td>", {
                text: item.chapters_total
            }).appendTo("#page_" + item.id)

            $("<td>", {
                text: item.new || '(+new)'
            }).appendTo("#page_" + item.id)
            
            $("<td>", {
                id: "td_remove_page_" + item.id,
            }).appendTo("#page_" + item.id)

                $("<button>", {
                    id: "remove_page_" + item.id,
                    class: 'remove_page',
                    value: item.id,
                    text: 'X'
                }).appendTo("td#td_remove_page_" + item.id)
        }
    }
};
function sendMessage(event) {
    ws.send(JSON.stringify({msg: event}))
    event.preventDefault()
};

window.addEventListener('focus', sendMessage);

$(document).on("click",".edit_name", function () {
    var clickedBtnID = this.id
    console.log('you clicked on button #' + clickedBtnID)
    ws.send(JSON.stringify({id: this.id, value: this.value}));
});

$(document).on("click",".remove_page", function () {
    var clickedBtnID = this.id
    console.log('you clicked on button #' + clickedBtnID)
    ws.send(JSON.stringify({id: this.id, value: this.value}));
});


const refresh_interval = 30000
setInterval(function() {
    console.log('Interval reached every ' + 
                refresh_interval + ' msec')
    if (!document.hidden) {
        console.log("not hidden")
    } else {
        console.log("hidden")
    }
}, refresh_interval);

ws.onopen = () => ws.send(JSON.stringify({msg: 'ws.onopen'}));
