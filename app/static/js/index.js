var map;

function getCovidsafeScore(place_id) {
    $.ajax({
        url: '/covidsafeScore?place_id=' + place_id,
        success: function (result) {
            console.log('covidsafeScore', result);
        }
    });
}

function getListOfPlaces(place_name) {
    var request = {
        query: place_name,
        fields: ["formatted_address","business_status","geometry","icon","name","place_id"]
    };
    
    service = new google.maps.places.PlacesService(map);
    
    service.findPlaceFromQuery(request, function(results, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            getCovidsafeScore(results[0].place_id);
        }
    });
}

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: -34.397, lng: 150.644 },
        zoom: 8
    });
}

$(document).ready(function () {
    console.log('wazzup');
});