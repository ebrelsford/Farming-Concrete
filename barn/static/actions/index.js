var limit = 5,
    offset = 0;

function showActions(limit, offset) {
    var list = document.querySelectorAll('.actions-list')[0];
    list.innerHTML = null;

    var template = document.getElementById('item-template').innerHTML,
        compiledTemplate = doT.template(template);

    qwest.get('../api-admin/actions/?limit=' + limit + '&offset=' + offset)
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
    showActions(limit);

    // Initialize limit links
    var setLimitLinks = document.querySelectorAll('.set-limit');
    for (var i = 0; i < setLimitLinks.length; i++) {
        setLimitLinks[i].addEventListener('click', function (e) {
            showActions(e.target.getAttribute('data-limit'), offset)
            e.preventDefault();
        });
    }

    // Initialize next and previous links
    document.querySelectorAll('.actions-previous')[0].addEventListener('click', function (e) {
        offset -= limit;
        showActions(limit, offset);
        e.preventDefault();
    });
    document.querySelectorAll('.actions-next')[0].addEventListener('click', function (e) {
        offset += limit;
        showActions(limit, offset);
        e.preventDefault();
    });
}

if (document.readyState !== 'loading') {
    onReady();
}
else {
    document.addEventListener('DOMContentLoaded', onReady);
}
