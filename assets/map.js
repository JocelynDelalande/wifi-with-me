$( document ).ready(function() {

    // Defaults
    defaults = {
        lat: 47.218371,
        lng: -1.553621,
        zoom: 13,
    }

    // Create map
    var map = L.map('map', {scrollWheelZoom: false}).setView([defaults.lat,defaults.lng], defaults.zoom);
    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18
    }).addTo(map);

    // Get JSON
    var GeoJsonPath = $('#map').data('json')
    $.getJSON(GeoJsonPath, function(data){

        function buildPopupContent(feature, layer) {
            feature.properties.popupContent = '';

            if (feature.properties.name) {
                feature.properties.popupContent += '<h2>#'+feature.id+': '+feature.properties.name+'</h2>';
            }
            else {
                feature.properties.popupContent += '<h2>#'+feature.id+'</h2>';
            }

            if (feature.properties.place) {
                feature.properties.popupContent += '<ul>';
                if (feature.properties.place.hasOwnProperty('floor')) feature.properties.popupContent += '<li>Étage: '+feature.properties.place.floor+'</li>';
                if (feature.properties.place.orientations[0]) feature.properties.popupContent += '<li>Orientation: '+feature.properties.place.orientations.join(', ')+'</li>';
                if (feature.properties.place.roof) feature.properties.popupContent += '<li>Accès au toit'+'</li>';
                feature.properties.popupContent += '</ul>'
            }

            if (feature.properties.comment) {
                feature.properties.popupContent += '<p>'+feature.properties.comment+'</p>';
            }

            layer.bindPopup(feature.properties.popupContent);
        }

        // Add to map
        var featureLayer = L.geoJson(data, {
            onEachFeature: buildPopupContent
        }).addTo(map);

        // Auto Zoom
        // Strange leaflet bug, we need to set a null timeout
        setTimeout(function () {
            map.fitBounds(featureLayer.getBounds())
        }, 2);

    });

});
