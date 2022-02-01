var ws = new WebSocket(`ws://localhost:8000/ws/list_all`);
ws.onmessage = function (event) {
  var collection = eval(event.data)

  for (var i in eval(event.data)) {
    var item = collection[i]

    if ($('#page_' + item.id).length) {  // item already present
      var new_0 = $("#new_" + item.id).text()
      var new_1 = ''
      if (item.new) {
        new_1 = `(+${item.new})`
      } 
      if (new_0 == new_1) {
        console.log('==')
      } else {
        $("#new_" + item.id).text(new_1)
      }
    } else {  // new item
      $("<tr>", {
        id: 'page_' + item.id
      }).prependTo("#user_list");

      let item_new = ''
      if (item.new) {
        item_new = `(+${item.new})`
      }

      $('#page_' + item.id).html(`
      <td class="page_name">
          <a value="${item.id}" id="link_page_${item.id}" class="page_url" onclick="return false;" href="${item.url}">${item.name}</a>
      </td>
      <td>
          <button id="edit_page_${item.id}" class="edit_name" value="${item.id}">
            &#128394;
          </button>
      </td>
      <td>
          <span>${item.chapters_total}</span>
      </td>
      <td>
          <span id="new_${item.id}">${item_new}</span>
      </td>
      <td>
          <button id="remove_page_${item.id}" class="remove_page" value="${item.id}">&#10005;</button>
      </td>
      `);

    }
  }
};

window.addEventListener('focus', function() {
  ws.send(JSON.stringify({ event: 'focus' }))
});

$(document).on("click", ".edit_name", function () {
  let page_id = this.value

  var link = $('#link_page_' + this.value)
  let old_name = link.prop("innerText")

  var input = $("<input>", {
    id: 'name_field_' + this.value,
    class: 'name_field',
    size: 50,
    value: old_name,
  })

  link.replaceWith(input);
  input.focus()

  function editName() {
    var new_name = input.prop("value")
    if (old_name !== new_name) {
      ws.send(JSON.stringify({
        event: 'edit_name',
        page_id: page_id,
        value: new_name,
    }));
    link.text(new_name);
  }};

  input.keypress(function (event) {
    if (event.keyCode === 13) {
      editName()
      input.replaceWith(link);
    }
  });

  input.blur(function () {
    editName()
    input.replaceWith(link);
  });

  input.blur(input.replaceWith.link)
});

$(document).on("click", ".remove_page", function () {
  var clickedBtnID = this.id
  console.log('you clicked on button #' + clickedBtnID)
  ws.send(JSON.stringify({
    event: 'remove_page',
    page_id: this.value
  }));
  $("#page_" + this.value).remove();
});

$(document).on("click", ".page_url", function () {
  console.log('you clicked on button #' + this.id)
  console.log('href= ' + $(this).attr('href'))
  ws.send(JSON.stringify({
    event: 'page_url_click',
    page_id: $(this).attr('value')
  }));
  window.location.replace($(this).attr('href'));

});

const refresh_interval = 30000
setInterval(function () {
  console.log('Interval reached every ' +
    refresh_interval + ' msec')
  if (!document.hidden) {
    console.log("not hidden")
  } else {
    console.log("hidden")
  }
}, refresh_interval);

ws.onopen = () => ws.send(JSON.stringify({ event: 'ws.onopen' }));
