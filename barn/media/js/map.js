var GardenMap = {

    epsg4326: new OpenLayers.Projection("EPSG:4326"),
    epsg900913: new OpenLayers.Projection("EPSG:900913"),

    init: function(options, elem) {
        //this.t = this;
        var t = this;
        this.options = $.extend({}, this.options, options);

        this.elem = elem;
        this.$elem = $(elem);

        this.olMap = new OpenLayers.Map(this.$elem.attr('id'), {
            controls: [
                new OpenLayers.Control.Navigation(),
                new OpenLayers.Control.Attribution(),
                new OpenLayers.Control.LoadingPanel(),
                /*new OpenLayers.Control.ZoomPanel()*/
            ],
            restrictedExtent: this.createBBox(-75.066, 41.526, -72.746, 39.953), 
            zoomToMaxExtent: function() {
                this.setCenter(t.options.center, t.options.initialZoom);
            }
        });

        var cloudmade = new OpenLayers.Layer.CloudMade("CloudMade", {
            key: '781b27aa166a49e1a398cd9b38a81cdf',
            styleId: '17595',
            transitionEffect: 'resize'
        });
        this.olMap.addLayer(cloudmade);

        this.olMap.zoomToMaxExtent();

        /* add the base gardens layer */
        this.getLayer('counted', '/cropcount/gardens/complete/geojson/', this.defaultStyle);
        /*
        this.surveyedGardensLayer = this.addSurveyedGardens();
        this.unsurveyedGardensLayer = this.addUnsurveyedGardens();

        this.addControls([this.surveyedGardensLayer, this.unsurveyedGardensLayer]);
        */

        return this;
    },

    options: {
        center: new OpenLayers.LonLat(-8230729.8555054, 4970948.0494563),
        initialZoom: 10,
        addContentToPopup: function(popup, feature) { ; },
    },

    createBBox: function(lon1, lat1, lon2, lat2) {
        var b = new OpenLayers.Bounds();
        b.extend(this.getTransformedLonLat(lon1, lat1));
        b.extend(this.getTransformedLonLat(lon2, lat2));
        return b;
    },

    defaultStyle: {
        pointRadius: '5',
        fillColor: '#3f9438',
        fillOpacity: '0.4',
        strokeOpacity: '0.8',
        strokeWidth: 0,
    },

    styles: [
        { pointRadius: '6', fillColor: '#f9ff51', fillOpacity: '0.6' },
        { pointRadius: '6', fillColor: '#f90000', fillOpacity: '0.4' },
        { pointRadius: '8', fillColor: '#E8C051', fillOpacity: '0.8' },
    ],

    unsurveyedStyle: { pointRadius: '2', fillColor: '#0000FF', fillOpacity: '0.5', strokeWidth: 0 },

    getStyles: function(style) {
        return new OpenLayers.StyleMap({'default': style, 'select': {pointRadius: 15}, 'temporary': {pointRadius: 10}});
    },

    getLayer: function(name, url, style) {
        var layer = new OpenLayers.Layer.Vector(name, {
            projection: this.olMap.displayProjection,
            strategies: [new OpenLayers.Strategy.Fixed()],
            styleMap: this.getStyles(style),
            protocol: new OpenLayers.Protocol.HTTP({
                url: url,
                format: new OpenLayers.Format.GeoJSON()
            })
        });
        this.olMap.addLayer(layer);
        return layer;
    },

    addStyles: function(layer) {
        var filter1 = new OpenLayers.Filter.Comparison({
            type: OpenLayers.Filter.Comparison.EQUAL_TO,
            property: "picked0",
            value: true
        });
        var filter2 = new OpenLayers.Filter.Comparison({
            type: OpenLayers.Filter.Comparison.EQUAL_TO,
            property: "picked1",
            value: true
        });

        var rulePicked = [];
        rulePicked[0] = new OpenLayers.Rule({
            filter: filter1,
            symbolizer: this.styles[0]
        });
        rulePicked[1] = new OpenLayers.Rule({
            filter: filter2,
            symbolizer: this.styles[1]
        });
        rulePicked[2] = new OpenLayers.Rule({
            filter: new OpenLayers.Filter.Logical({
                type: OpenLayers.Filter.Logical.AND,
                filters: [ filter1, filter2 ]
            }),
            symbolizer: this.styles[2]
        });
        rulePicked[3] = new OpenLayers.Rule({
            elseFilter: true
        });
        layer.styleMap.styles['default'].addRules(rulePicked);
    },

    addControls: function(layers) {
        this.getControlHoverFeature(layers);
        this.selectControl = this.getControlSelectFeature(layers);
    },

    getControlSelectFeature: function(layers) {
        var selectControl = new OpenLayers.Control.SelectFeature(layers);
        var t = this;

        $.each(layers, function(i, layer) {
            layer.events.on({
                "featureselected": function(event) {
                    var feature = event.feature;
                    var popup = t.createAndOpenPopup(feature);
                    t.options.addContentToPopup(popup, feature);
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
        });

        this.olMap.addControl(selectControl);
        selectControl.activate();   
        return selectControl;
    },

    createAndOpenPopup: function(feature) {
        var content = "<div style=\"min-width: 500px; min-height: 250px;\"></div>";
        var t = this;

        var popup = new OpenLayers.Popup.Anchored("chicken", 
                                    feature.geometry.getBounds().getCenterLonLat(),
                                    new OpenLayers.Size(500, 300),
                                    content,
                                    null, 
                                    true, 
                                    function(event) { t.selectControl.unselectAll(); });
        popup.panMapIfOutOfView = true;
        feature.popup = popup;
        this.olMap.addPopup(popup);

        // don't let the close box add whitespace to the popup
        var new_width = $('.olPopupContent').width() + $('.olPopupCloseBox').width();
        $('.olPopupContent').width(new_width);
        return $('#chicken_contentDiv');
    },

    getControlHoverFeature: function(layers) {
        var selectControl = new OpenLayers.Control.SelectFeature(layers, {
            hover: true,
            highlightOnly: true,
            renderIntent: 'temporary'
        });
        this.olMap.addControl(selectControl);
        selectControl.activate();   
        return selectControl;
    },


    clearPicked: function(index) {
        var attr = "picked" + index;
        $.each(this.surveyedGardensLayer.features, function(i, feature) {
            feature.attributes[attr] = false;
        });
        this.surveyedGardensLayer.redraw();
    },

    addGardenIdsToPicked: function(gardenIds, index) {
        this.clearPicked(index);

        var attr = "picked" + index;
        $.each(this.surveyedGardensLayer.features, function(i, feature) {
            if ($.inArray(parseInt(feature.fid), gardenIds) >= 0) {
                feature.attributes[attr] = true;
            }
        });
        this.surveyedGardensLayer.redraw();
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
        'City Councils': "resources/geojson/nycc.geojson",
        'City Council Labels': "resources/geojson/nycc_centroids.geojson",
        'Community Districts': "resources/geojson/nycd.geojson",
        'Community District Labels': "resources/geojson/nycd_centroids.geojson",
        'Boroughs': "resources/geojson/boroughs.geojson",
        'Borough Labels': "resources/geojson/borough_centroids.geojson",
    },

    loadLayer: function(name) {
        var layer = new OpenLayers.Layer.Vector(name, {
            projection: this.olMap.displayProjection,
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

    selectAndCenterOnGarden: function(fid) {
        var feature = this.surveyedGardensLayer.getFeatureByFid(fid);
        if (!feature) feature = this.unsurveyedGardensLayer.getFeatureByFid(fid);
        if (!feature) return;

        var l = new OpenLayers.LonLat(feature.geometry.x, feature.geometry.y);
        this.olMap.setCenter(l, 15);
        this.selectControl.unselectAll();
        this.selectControl.select(feature);
    },

    getTransformedLonLat: function(longitude, latitude) {
        return new OpenLayers.LonLat(longitude, latitude).transform(this.epsg4326, this.epsg900913);
    },

};

$.plugin('gardenmap', GardenMap);
