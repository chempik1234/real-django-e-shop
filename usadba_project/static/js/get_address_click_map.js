var locationInfo = document.getElementById('location');

DG.then(function () {
    var map,
        marker;

    map = DG.map('map', {
        center: [54.488781, 53.468230],
        zoom: 15
    });

    marker = DG.marker([54.488781, 53.468230], {
        draggable: true
    }).addTo(map);

    marker.on('drag', function(e) {
        var lat = e.target._latlng.lat.toFixed(3),
            lng = e.target._latlng.lng.toFixed(3);

        locationInfo.value = lat + ',' + lng;
    });
});

$('input[type="radio"]').click(function () {
    if ($(this).attr("name") == "deliever_or_pickup" && $(this).attr("value") == "False") {
        $(".deliver_pickup_hide").hide('slow');
    }
    if ($(this).attr("name") == "deliever_or_pickup" && $(this).attr("value") == "True") {
        $(".deliver_pickup_hide").show('slow');
    }
});

$('input[type="radio"]').trigger('click');  // trigger the event