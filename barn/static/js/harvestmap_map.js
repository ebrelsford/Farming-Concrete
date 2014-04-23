var GardenMap = {

    epsg4326: new OpenLayers.Projection("EPSG:4326"),
    epsg900913: new OpenLayers.Projection("EPSG:900913"),

    allGardensLayer: null,
    selectControl: null,

    defaultStyle: { pointRadius: '3', fillColor: '#85137B', fillOpacity: '0.9', strokeWidth: '0', },
    selectedStyle: { pointRadius: '5', fillColor: '#85137B', fillOpacity: '0.9', strokeColor: '#FB62FF', strokeWidth: '3' },
    clickedStyle: { pointRadius: '15' },

    init: function(options, elem){
        this.elem = elem;
        this.$elem = $(elem);

        this.olMap = new OpenLayers.Map(this.$elem.attr('id'), {
            controls: [
                new OpenLayers.Control.Navigation(),
                new OpenLayers.Control.Attribution(),
                new OpenLayers.Control.LoadingPanel(),
                new OpenLayers.Control.ZoomPanel()
            ],
            restrictedExtent: this.createBBox(-75.066, 41.526, -72.746, 39.953), 
        });

        var mapbox = new OpenLayers.Layer.XYZ('mapbox', [
            'https://a.tiles.mapbox.com/v3/farmingconcrete.i29og38a/${z}/${x}/${y}.png',
            'https://b.tiles.mapbox.com/v3/farmingconcrete.i29og38a/${z}/${x}/${y}.png',
            'https://c.tiles.mapbox.com/v3/farmingconcrete.i29og38a/${z}/${x}/${y}.png',
            'https://d.tiles.mapbox.com/v3/farmingconcrete.i29og38a/${z}/${x}/${y}.png'
        ], {
            attribution: "Tiles &copy; <a href='http://mapbox.com/'>MapBox</a>",
            sphericalMercator: true,
            wrapDateLine: true
        });
        this.olMap.addLayer(mapbox);
        this.olMap.setBaseLayer(mapbox);

        this.changeGardensLayer('2011'); // TODO replace with selected on map

        var t = this;
        this.olMap.zoomToMaxExtent = function() {
            t.olMap.setCenter(new OpenLayers.LonLat(-8230729.8555054, 4970948.0494563), 10);
        };

        return this;
    },

    changeGardensLayer: function(year) {
        if (this.allGardensLayer) {
            this.allGardensLayer.removeAllFeatures();
        }
        url = '/harvestmap/gardens/kml?year=' + year;
        this.allGardensLayer = this.getAllGardensLayer(url);
        return this.allGardensLayer;
    },

    getAllGardensLayer: function(kml_url) {
        var layer = new OpenLayers.Layer.Vector(name, {
            projection: this.epsg4326,
            strategies: [new OpenLayers.Strategy.Fixed()],
            styleMap: this.getStyles(),
            protocol: new OpenLayers.Protocol.HTTP({
                url: kml_url,
                format: new OpenLayers.Format.KML()
            })
        });
        this.addStyles(layer);
        this.olMap.addLayer(layer);

        this.selectControl = this.getControlSelectFeature(layer);

        return layer;
    },

    getControlSelectFeature: function(layer) {
        var selectControl = new OpenLayers.Control.SelectFeature(layer);

        var t = this;
        layer.events.on({
            "featureselected": function(event) {
                t.createAndOpenPopup(event.feature);
            },
            "featureunselected": function(event) {
                var feature = event.feature;
                if(feature.popup) {
                    t.olMap.removePopup(feature.popup);
                    feature.popup.destroy();
                    delete feature.popup;
                }
            },
        });
        this.olMap.addControl(selectControl);
        selectControl.activate();   
        return selectControl;
    },

    createAndOpenPopup: function(feature) {
        var content = "<div style=\"padding-top: 7px; padding-left: 5px;\">" + feature.attributes.name + "</div>";

        var t = this;
        var popup = new OpenLayers.Popup.Anchored("chicken", 
                                    feature.geometry.getBounds().getCenterLonLat(),
                                    null,
                                    content,
                                    null, 
                                    true, 
                                    function(event) { t.selectControl.unselectAll(); });
        popup.autoSize = true;
        popup.panMapIfOutOfView = true;
        feature.popup = popup;
        this.olMap.addPopup(popup);

        // don't let the close box add whitespace to the popup
        var new_width = $('.olPopupContent').width() + $('.olPopupCloseBox').width();
        $('.olPopupContent').width(new_width);
        return $('#chicken_contentDiv');
    },

    createBBox: function(lon1, lat1, lon2, lat2) {
        var b = new OpenLayers.Bounds();
        b.extend(this.getTransformedLonLat(lon1, lat1));
        b.extend(this.getTransformedLonLat(lon2, lat2));
        return b;
    },

    getTransformedLonLat: function(longitude, latitude) {
        return new OpenLayers.LonLat(longitude, latitude).transform(this.epsg4326, this.epsg900913);
    },

    addStyles: function(layer) {
        var filter1 = new OpenLayers.Filter.Comparison({
            type: OpenLayers.Filter.Comparison.EQUAL_TO,
            property: "picked0",
            value: true
        });

        layer.styleMap.styles['default'].addRules([
            new OpenLayers.Rule({ 
                filter: new OpenLayers.Filter.FeatureId({
                    fids: []
                }),
                symbolizer: this.selectedStyle
            }),
            new OpenLayers.Rule({
                elseFilter: true
            })
        ]);
    },

    highlightGardens: function(ids) {
        this.allGardensLayer.styleMap.styles['default'].rules[0].filter = new OpenLayers.Filter.FeatureId({
            fids: ids
        });
        this.allGardensLayer.redraw();
    },

    clearHighlightedGardens: function(layer) {
        this.highlightGardens([]);
    },

    getStyles: function() {
        return new OpenLayers.StyleMap({
            'default': this.defaultStyle,
            'select': this.clickedStyle,
        });
    },

    zoom_to_visible_gardens: function(garden_layer) {
        this.olMap.zoomToExtent(this.get_bounds(this.get_points(garden_layer)));   
    },

    get_points: function(layer) {
        return $.map(layer.features, function(feature, i) {
            return feature.geometry;
        });
    },

    get_bounds: function(points) {  
        return new OpenLayers.Geometry.MultiPoint(points).getBounds();
    },


    hideLayer: function(name) {
        var layers = this.olMap.getLayersByName(name);
        if (layers.length == 0) return;
        layers[0].setVisibility(false);
    },

    showLayer: function(name) {
        var layers = this.olMap.getLayersByName(name);
        if (layers.length == 0) {
            this.loadLayer(name);
        }
        else {
            layers[0].setVisibility(true);
        }
    },

    layerUrls: {
        'City Councils': "/static/geojson/nycc.geojson",
        'City Council Labels': "/static/geojson/nycc_centroids.geojson",
        'Community Districts': "/static/geojson/nycd.geojson",
        'Community District Labels': "/static/geojson/nycd_centroids.geojson",
        'Boroughs': "/static/geojson/boroughs.geojson",
        'Borough Labels': "/static/geojson/borough_centroids.geojson",
    },

    loadLayer: function(name) {
        var layer = new OpenLayers.Layer.Vector(name, {
            projection: this.epsg4326,
            strategies: [new OpenLayers.Strategy.Fixed()],
            protocol: new OpenLayers.Protocol.HTTP({
                url: this.layerUrls[name],
                format: new OpenLayers.Format.GeoJSON(),
            }),
            styleMap: new OpenLayers.StyleMap({
                'default': {
                    'strokeWidth': 1,
                    'strokeColor': '#000',
                    'fillOpacity': 0,
                },
            }),
        });
        this.olMap.addLayer(layer);
    },

    hideLabelLayer: function(name) {
        var layers = this.olMap.getLayersByName(name);
        if (layers.length == 0) return;
        layers[0].setVisibility(false);
    },

    showLabelLayer: function(name) {
        var layers = this.olMap.getLayersByName(name);
        if (layers.length == 0) {
            this.loadLabelLayer(name);
        }
        else {
            layers[0].setVisibility(true);
        }
    },

    loadLabelLayer: function(name) {
        var layer = new OpenLayers.Layer.Vector(name, {
            projection: this.olMap.displayProjection,
            strategies: [new OpenLayers.Strategy.Fixed()],
            protocol: new OpenLayers.Protocol.HTTP({
                url: this.layerUrls[name],
                format: new OpenLayers.Format.GeoJSON(),
            }),
            styleMap: new OpenLayers.StyleMap({
                'default': {
                    'label': '${label}',
                },
            }),
        });
        this.olMap.addLayer(layer);
    },
};

$.plugin('gardenmap', GardenMap);
