var ws = new WebSocket(`ws://localhost:8000/ws/list_all`);

const table = {
  row: function(item) {
    if ($('#page_' + item.id).length) {
      table.updateTotal(item);
      table.updateNew(item);
    } else {
      table.spawnRow(item);
      table.setName(item);
      table.setTotal(item);
      table.setNew(item);      
    }
  },

  updateTotal: function(item) {
    if ($(`#total_${item.id} > span`).text() !== item.total) {
      table.setTotal(item)
    }
  },

  updateNew: function(item) {
    if ($(`#new_${item.id} > span`).text() !== `(+${item.new})`) {
      table.setNew(item)
    };
    if (item.pending) {
      $(`#new_${item.id}`).addClass('pending')
    } else {
      $(`#new_${item.id}`).removeClass('pending')
    };

  },

  spawnRow: function(item) {
    $("<tr>", {
      id: 'page_' + item.id,
      html: `
      <td id="name_${item.id}" class="page_name"><a href="${item.url}"></a></td>
      <td id="edit_${item.id}" class="edit_name" value="${item.id}">&#128394;</td>
      <td id="total_${item.id}" class="total"><span></span></td>
      <td id="new_${item.id}" class="new" value="${item.id}"><span></span></td>
      <td id="remove_${item.id}" class="remove_page" value="${item.id}">&#10005;</td>`
    }).prependTo("#watchlist");
  },

  setName: function(item) {
    $(`#name_${item.id} > a`).text(item.name)
  },

  setTotal: function(item) {
    if ($(`#total_${item.id} > span`).text() !== item.total.toString()) {
      $(`#total_${item.id} > span`).text(item.total)
    }    
  },

  setNew: function(item) {
    if (item.new && (item.new !== item.total)) {
      $(`#new_${item.id} > span`).text(`(+${item.new})`)
    } else {
      $(`#new_${item.id} > span`).empty()
    }
  },
};

ws.onmessage = function (event) {
  var collection = eval(event.data);
  for (var i in collection) {
    var item = collection[i];
    table.row(item);
  } 
};

window.addEventListener('focus', function() {
  ws.send(JSON.stringify({ event: 'focus' }))
});

$("#watchlist").on("click", ".edit_name", function () {
  let id = $(this).attr('value')
  var link = $('#name_' + id + ' > a')
  let old_name = $(`#name_${id} > a`).text()
  var input = $("<input>", {
    id: 'name_field_' + id,
    class: 'name_field',
    size: 50,
    value: old_name,
  })

  link.replaceWith(input);
  input.trigger('focus')

  function editName() {
    var new_name = input.prop("value")
    if (old_name !== new_name) {
      ws.send(JSON.stringify({
        event: 'edit_name',
        page_id: id,
        value: new_name,
    }));
    link.text(new_name);
  }};

  input.on("keydown", function (event) {
    if (event.key === 'Enter') {
      editName()
      input.replaceWith(link);
    }
  });

  input.on("blur", function () {
    editName()
    input.replaceWith(link);
  });
});

$("#watchlist").on("click", ".remove_page", function () {
  console.log('#' + this.id)
  var id = $(this).attr('value')
  ws.send(JSON.stringify({
    event: 'remove_page',
    page_id: id
  }));
  $("#page_" + id).remove();
});

$("#watchlist").on("click", ".page_url", function () {
  console.log('#' + this.id)
  console.log('href= ' + $(this).attr('href'))
  ws.send(JSON.stringify({
    event: 'page_url_click',
    page_id: $(this).attr('value')
  }));
  window.location.replace($(this).attr('href'));
});

$("#watchlist").on("click", ".new", function () {
  console.log('new for page ' + $(this).attr('value'))
  ws.send(JSON.stringify({
    event: 'click_new',
    page_id: $(this).attr('value')
  }));
});

const refresh_interval = 2000
setInterval(function () {
  if (!document.hidden && ws.readyState) {
    ws.send(JSON.stringify({ event: 'window.active' }))
  } else {
    console.log("document.hidden")
  }
}, refresh_interval);

ws.onopen = () => ws.send(JSON.stringify({ event: 'ws.onopen' }));
