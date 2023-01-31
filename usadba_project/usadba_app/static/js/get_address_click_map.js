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