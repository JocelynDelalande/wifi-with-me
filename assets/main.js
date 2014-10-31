$( document ).ready(function() {

    // Create map
    var map = L.map('map').setView([47.218371,-1.553621], 13);
    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18
    }).addTo(map);

    // Create marker
    var marker = L.marker([47.218371,-1.553621], {
        draggable: true
    }).addTo(map);

    // every time the marker is dragged, update the coordinates container
    marker.on('dragend', ondragend);

    // Set the initial marker coordinate on load.
    ondragend();

    function ondragend() {
        var m = marker.getLatLng();
        $('latitude').value = m.lat;
        $('longitude').value = m.lng;
    }

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
                ondragend();
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

});