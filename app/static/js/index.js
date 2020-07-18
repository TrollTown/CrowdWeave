var map;

function getCovidsafeScore(place_id) {
    $.ajax({
        url: 'https://covidsafebutbetter.trolltown.codes/covidsafeScore?place_id=' + place_id
    }).then(function(result) {
        console.log(result);
        return result;
    });
}

function getListOfPlaces(place_name) {
    let request = {
        query: place_name,
        fields: ["formatted_address","business_status","geometry","icon","name","place_id"]
    };
    
    service = new google.maps.places.PlacesService(map);
    
    service.textSearch(request, function(results, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            console.log(results)
            addCovidScore(results);
        }
    });
}

function addCovidScore(place_list) {
    let new_list = [];

    for (let i = 0; i < place_list.length; i++) {
        let score = getCovidsafeScore(place_list[i].place_id);
        let obj = {place: place_list[i], covid_score: score};
        new_list.push(obj);
    }

    console.log(new_list);
}

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: -33.828725, lng: 151.092503 },
        zoom: 12,
        mapTypeControl: false,
        fullscreenControl: false,
        streetViewControl: false,
        styles: [
            {elementType: 'geometry', stylers: [{color: '#242f3e'}]},
            {elementType: 'labels.text.stroke', stylers: [{color: '#242f3e'}]},
            {elementType: 'labels.text.fill', stylers: [{color: '#746855'}]},
            {
              featureType: 'administrative.locality',
              elementType: 'labels.text.fill',
              stylers: [{color: '#d59563'}]
            },
            {
              featureType: 'poi',
              elementType: 'labels.text.fill',
              stylers: [{color: '#d59563'}]
            },
            {
              featureType: 'poi.park',
              elementType: 'geometry',
              stylers: [{color: '#263c3f'}]
            },
            {
              featureType: 'poi.park',
              elementType: 'labels.text.fill',
              stylers: [{color: '#6b9a76'}]
            },
            {
              featureType: 'road',
              elementType: 'geometry',
              stylers: [{color: '#38414e'}]
            },
            {
              featureType: 'road',
              elementType: 'geometry.stroke',
              stylers: [{color: '#212a37'}]
            },
            {
              featureType: 'road',
              elementType: 'labels.text.fill',
              stylers: [{color: '#9ca5b3'}]
            },
            {
              featureType: 'road.highway',
              elementType: 'geometry',
              stylers: [{color: '#746855'}]
            },
            {
              featureType: 'road.highway',
              elementType: 'geometry.stroke',
              stylers: [{color: '#1f2835'}]
            },
            {
              featureType: 'road.highway',
              elementType: 'labels.text.fill',
              stylers: [{color: '#f3d19c'}]
            },
            {
              featureType: 'transit',
              elementType: 'geometry',
              stylers: [{color: '#2f3948'}]
            },
            {
              featureType: 'transit.station',
              elementType: 'labels.text.fill',
              stylers: [{color: '#d59563'}]
            },
            {
              featureType: 'water',
              elementType: 'geometry',
              stylers: [{color: '#17263c'}]
            },
            {
              featureType: 'water',
              elementType: 'labels.text.fill',
              stylers: [{color: '#515c6d'}]
            },
            {
              featureType: 'water',
              elementType: 'labels.text.stroke',
              stylers: [{color: '#17263c'}]
            }
          ]
    });
}

function openNav() {
    document.getElementById("mySidenav").style.right = "0px";
}

$(document).ready(function () {
    console.log('wazzup');
    button = document.getElementById("searchBtn");
    button.addEventListener("click", e => {
        var place = document.getElementById("searchTextbox").value
        console.log(place)
        if (place.length == 0){
            return
        }
        openNav();
        getListOfPlaces(place);
    })
});