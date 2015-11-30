(function () {
    var endpoint = '../api-admin/actions/geojson/',
        apiDateFormat = 'YYYY-MM-DD',
        inputDateFormat = 'YYYY-MM-DD',
        map,
        actionLayer;

    function createMap(data) {
        map = L.map('actions-map-map', {
            center: [20, 0],
            zoom: 1
        });

        L.tileLayer('https://{s}.tiles.mapbox.com/v3/{mapboxId}/{z}/{x}/{y}.png', {
            attribution: 'Data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a>, Imagery &copy; <a href="http://mapbox.com">Mapbox</a>',
            maxZoom: 18,
            mapboxId: 'farmingconcrete.i29og38a'
        }).addTo(map);

        actionLayer = L.markerClusterGroup();
        map.addLayer(actionLayer);
    }

    function updateMap() {
        var minTimestamp = document.querySelector('.actions-map-filters-min-timestamp').value,
            maxTimestamp = document.querySelector('.actions-map-filters-max-timestamp').value;

        var verbOptions = document.querySelectorAll('.actions-map-filters-verb option');
        var verbs = _.chain(verbOptions)
            .filter(function (option) {
                return option.selected;
            })
            .map(function (option) {
                return 'verb=' + option.value;
            });

        qwest.get(endpoint + '?' + verbs.join('&'), {
            'max_timestamp': maxTimestamp,
            'min_timestamp': minTimestamp
        })
            .then(function (xhr, data) {
                actionLayer.clearLayers();
                actionLayer.addLayer(L.geoJson(data));
                map.fitBounds(actionLayer.getBounds());
            });
    }

    function actionsMapOnReady() {
        var select = document.querySelectorAll('.actions-map-filters-verb')[0];
        actionVerbsMappable.forEach(function (verb) {
            var option = document.createElement('option');
            option.setAttribute('value', verb);
            option.textContent = verb;
            select.appendChild(option);
        });

        select.addEventListener('change', function () {
            updateMap();
        });

        // Initialize min/max timestamp fields
        var minTimestamp = document.querySelector('.actions-map-filters-min-timestamp'),
            maxTimestamp = document.querySelector('.actions-map-filters-max-timestamp'),
            now = moment(new Date()),
            lastYear = now.clone().subtract(1, 'years');
        minTimestamp.setAttribute('value', lastYear.format(inputDateFormat));
        maxTimestamp.setAttribute('value', now.format(inputDateFormat));

        // When timestamp fields change, update
        minTimestamp.addEventListener('change', function () {
            updateMap();
        });
        maxTimestamp.addEventListener('change', function () {
            updateMap();
        });

        setTimeout(function () {
            createMap();
            updateMap();
        }, 1000);
    }

    if (document.readyState !== 'loading') {
        actionsMapOnReady();
    }
    else {
        document.addEventListener('DOMContentLoaded', actionsMapOnReady);
    }
})();
