function showActions(limit) {
    var list = document.querySelectorAll('.actions-list')[0];
    list.innerHTML = null;

    var template = document.getElementById('item-template').innerHTML,
        compiledTemplate = doT.template(template);

    qwest.get('../api-admin/actions/?limit=' + limit)
        .then(function (xhr, data) {
            data.results.forEach(function (action) {
                var listItem = document.createElement('li');
                action.formatted_timestamp = moment(action.timestamp).fromNow();
                listItem.innerHTML = compiledTemplate(action);
                list.appendChild(listItem);
            });
        });
}

function onReady() {
    showActions(5);

    var setLimitLinks = document.querySelectorAll('.set-limit');
    for (var i = 0; i < setLimitLinks.length; i++) {
        setLimitLinks[i].addEventListener('click', function (e) {
            showActions(e.target.getAttribute('data-limit'))
            e.preventDefault();
        });
    }
}

if (document.readyState !== 'loading') {
    onReady();
}
else {
    document.addEventListener('DOMContentLoaded', onReady);
}
