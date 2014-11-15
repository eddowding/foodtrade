$(document).ready(function() { //TODO: move templating logic to seperate file using a templating engine
  var markerDict = {};
  var markerSetupFn = function(map, objs) {
    for (var key in markerDict) {
      map.removeLayer(markerDict[key]);
    }
    markerDict = {};
    objs.forEach(function(value, index) {
      var icon = L.icon({
        iconUrl: value.profile_img[0],
        iconSize: [32, 32]
      });
      var latlng = value.latlng[0].split(',');
      latlng = new L.LatLng(parseFloat(latlng[0]), parseFloat(latlng[1]));
      map.panTo(latlng);
      var card_str = '<div class="card-box"><div class="content text-center"><div class=""><a href="/profile/' + value.username[0] + '"><img src="' + value.profile_img[0] + '" alt="' + value.name[0] + '" class="img-circle img-thumbnail img-responsive" style="width:73px;" /></a>';
      card_str += '</div><div class="text"><h3><a href="/profile/' + value.username[0] + '">' + value.name[0] + '</a></h3>';
      card_str += '<p>' + $.trim(value.description[0]).substring(0, 50) + '...</p></div>';
      card_str += '<a href="/profile/' + value.username[0] + '" class="btn btn-primary btn-sm">View profile &raquo;</a></div> </div>';
      var marker = L.marker(latlng, {
        icon: icon,
        clickable: true,
        draggable: false,
        riseOnHover: true
      }).bindPopup(card_str).addTo(map);
      markerDict[value.id] = marker;
    });
  };

  var searchFn = function() {
    var query = $('#search_query').val();
    $.ajax({
      url: '/search/result',
      method: 'get',
      dataType: 'json',
      data: {
        query: query
      },
      success: function(data) {
        $('#profile_results').html(data.html);
        markerSetupFn(map, data.objs);
        $('#profile-type-label').text('Profile Types (' + data.facets.sign_up_as.total + ')');
        var options = '';
        data.facets.sign_up_as.terms.forEach(function(value, index) {
          options += '<option value="' + value.term + '">' + value.term + ' (' + value.count + ')</option>';
        });
        $('#profile-type-select').html(options);
        if (data.objs.length) {
          $('#profile-type-label').show();
          $('#profile-type-select').show();
        } else {
          $('#profile-type-label').hide();
          $('#profile-type-select').hide();
        }
      }
    });
  };

  var map = L.map('map').setView([51.505, -0.09], 6);
  L.tileLayer('https://{s}.tiles.mapbox.com/v3/foodtrade.i26pc0n5/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18
  }).addTo(map);

  $('#search_query').keyup(function(ev) {
    var query = $(this).val();
    if ((query.length % 3) === 0) {
      searchFn();
    }
  });

  $('#profile_results').delegate('.tile-hover', 'mouseover', function() {
    var id = $(this).attr('data-id');
    var marker = markerDict[id];
    marker.openPopup();
  });

  $('#profile_results').delegate('.tile-hover', 'mouseout', function() {
    var id = $(this).attr('data-id');
    var marker = markerDict[id];
    marker.closePopup();
  });
});
