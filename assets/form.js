$( document ).ready(function() {

    // Defaults
    defaults = {
        lat: ($('#latitude').val()) ? $('#latitude').val() : 45.75884,
        lng: ($('#longitude').val()) ? $('#longitude').val() : 4.82709,
        zoom: 11,
    }

    // Create map
    var map = L.map('map', {scrollWheelZoom: false}).setView([defaults.lat,defaults.lng], defaults.zoom);
    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18
    }).addTo(map);

    // Create marker
    var marker = L.marker([defaults.lat,defaults.lng], {
        draggable: true
    }).addTo(map);

    // every time the marker is dragged, update the coordinates container
    marker.on('dragend', mapUpdateCoords);

    // Set the initial marker coordinate on load.
    mapUpdateCoords();

    function mapUpdateCoords() {
        var m = marker.getLatLng();
        $('#latitude').val(m.lat);
        $('#longitude').val(m.lng);
    }

	// Display tiny circles on existing public points
	var GeoJsonPath = $('#map').data('json');
    $.getJSON(GeoJsonPath, function(data){
	    var featureLayer = L.geoJson(data, {
		    pointToLayer: function (feature, latlng) {
			    return L.circleMarker(latlng, {color: '#00B300'});
		    }
        }).addTo(map);
    });

    // Search sub form
    $('#search-btn').click(function(e){
        e.preventDefault();
        var btn = $(this).button('loading');

        // Geocoding
        var searchString = $('#search').val();
        $.getJSON('http://nominatim.openstreetmap.org/search?limit=5&format=json&q='+searchString, function(data){

            var items = [];
            $.each(data, function(key, val) {
                items.push(
                    "<li class='list-group-item'><a href='#' data-lat='"+val.lat+"' data-lng='"+val.lon+"'>" + val.display_name + '</a></li>'
                );
            });

            $('#modal .modal-body').empty();
            if (items.length != 0) {
                $('<ul/>').addClass("list-group").html(items.join('')).appendTo('#modal .modal-body');
            } else {
                $('<p/>', { html: "Aucun résultat" }).appendTo('#modal .modal-body');
            }
            $('#modal').modal('show');

            // Bind click on results and update coordinates
            $('#modal .modal-body a').on('click', function(e){
                e.preventDefault();

                marker.setLatLng({lat:$(this).data('lat'), lng:$(this).data('lng')}).update();
                map.panTo({lat:$(this).data('lat'), lng:$(this).data('lng')});
                map.setZoom(16);
                mapUpdateCoords();
                $('#modal').modal('hide');
            });

            btn.button('reset');
        }); // getJSON

    }); // Search sub form

    // Enter key on search form does not submit form,
    // Trigger search button instead.
    $('#search').keypress(function(e) {
        if (e.which == '13') {
            e.preventDefault();
            $('#search-btn').trigger('click');
        }
    });


    // Contrib share dynamic form
    if ($('[name="contrib-type"]:checked').val() == 'share') { $('#contrib-type-share').show(); }
    else { $('#contrib-type-share').hide(); }
    // On change
    $('[name="contrib-type"]').change(function(e){
        if ($(this).val() == 'share') { $('#contrib-type-share').slideDown(); }
        else { $('#contrib-type-share').slideUp(); }
    });

    // select/deselect all checkbox
    $('#orientation-all').change(function(e){
        $('input[name="orientation"]').prop('checked', $(e.target).is(':checked') );
    });
    $('.orientation').change(function(e){
        if (! $(e.target).is(':checked')) {
            $('input[name="orientation-all"]').prop('checked', false);
        }
        if ($('.orientation').filter(':not(:checked)').length == 0) {
            $('input[name="orientation-all"]').prop('checked', true);
        }
    });

});
