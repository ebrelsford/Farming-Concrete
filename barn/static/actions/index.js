(function () {
    var limit = 5,
        offset = 0;

    function prepareAction(action) {
        action.formatted_timestamp = moment(action.timestamp).fromNow();
        if (action.action_object && !action.action_object.url) {
            action.action_object.url = [
                action.action_object.app_label,
                action.action_object.model_name,
                action.action_object.id
            ].join('/');
        }
        if (action.target && !action.target.url) {
            action.target.url = [
                action.target.app_label,
                action.target.model_name,
                action.target.id
            ].join('/');
        }
        return action;
    }

    function showActions(limit, offset) {
        var list = document.querySelectorAll('.actions-list')[0];
        list.innerHTML = null;

        var template = document.getElementById('item-template').innerHTML,
            compiledTemplate = doT.template(template);

        qwest.get('../api-admin/actions/?limit=' + limit + '&offset=' + offset)
            .then(function (xhr, data) {
                data.results.forEach(function (action) {
                    var listItem = document.createElement('li');
                    listItem.innerHTML = compiledTemplate(prepareAction(action));
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
                limit = parseInt(e.target.getAttribute('data-limit'));
                showActions(limit, offset)
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
})();
