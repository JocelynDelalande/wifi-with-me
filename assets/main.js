$( document ).ready(function() {

	var map = L.map('map').setView([47.218371,-1.553621], 13);
	var latitude = document.getElementById('latitude');
	var longitude = document.getElementById('longitude');

	L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
	    maxZoom: 18
	}).addTo(map);


	var marker = L.marker([47.218371,-1.553621], {
	    draggable: true
	}).addTo(map);

	// every time the marker is dragged, update the coordinates container
	marker.on('dragend', ondragend);

	// Set the initial marker coordinate on load.
	ondragend();

	function ondragend() {
	    var m = marker.getLatLng();
	    latitude.value = m.lat;
	    longitude.value = m.lng;
	}

	$('#search-btn').click(function(e){
		e.preventDefault();

		var searchString = $('#search').val();
		$.getJSON('http://nominatim.openstreetmap.org/search?limit=5&format=json&q='+searchString, function(data){
			var items = [];
			$.each(data, function(key, val) {
			  items.push(
			    "<li class='list-group-item'><a href='#' data-lat='"+val.lat+"' data-lng='"+val.lon+"'>" + val.display_name + '</a></li>'
			  );
			});

			$('#search-results').empty();
	        if (items.length != 0) {
	            // $('<p>Resultats</p>').appendTo('#search-results');
	            $('<ul/>').addClass("list-group").html(items.join('')).appendTo('#search-results');
	        } else {
	            $('<p>', { html: "No results found" }).appendTo('#search-results');
	        }

			$('#search-results a').on('click', function(e){
				e.preventDefault();

				marker.setLatLng({lat:$(this).data('lat'), lng:$(this).data('lng')}).update();
				map.panTo({lat:$(this).data('lat'), lng:$(this).data('lng')});
				ondragend();
			});
		});
	});



});