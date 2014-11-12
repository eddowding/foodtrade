$(document).ready(function() {
  var map = L.map('map').setView([51.505, -0.09], 13);
  L.tileLayer('https://{s}.tiles.mapbox.com/v3/foodtrade.i26pc0n5/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18
  }).addTo(map);

  $('#search_query').keyup(function (ev) {
    var query = $(this).val();
    if ((query.length % 3)===0) {
      $.ajax({
        url: '/search/result',
        method: 'get',
        dataType: 'json',
        data: {query: query},
        success: function (data) {
          $('#profile_results').html(data.html);
        }
      });
    }
  });
});
