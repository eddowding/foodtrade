

// Location autosuggestions

var placeCord;
function initialize() {

  // Create the search box and link it to the UI element.
  var input = /** @type {HTMLInputElement} */(
      document.getElementById('pac_input_market'));
  var input_profile = (document.getElementById('pac_input_profile'));

  var searchBox = new google.maps.places.SearchBox(
    /** @type {HTMLInputElement} */(input));

  var profile_address = new google.maps.places.SearchBox((input_profile));



  google.maps.event.addListener(input_profile, 'places_changed', function() {
    loading_latlng = true;
  var places = searchBox.getPlaces();
    placeCord = places[0].geometry.location;
    $("#lon").val(placeCord.lng());
    $("#lat").val(placeCord.lat());

     get_address("profile");




  });

  // [START region_getplaces]
  // Listen for the event fired when the user selects an item from the
  // pick list. Retrieve the matching places for that item.
  google.maps.event.addListener(searchBox, 'places_changed', function() {
    loading_latlng = true;
  var places = searchBox.getPlaces();
    placeCord = places[0].geometry.location;
    $("#lon").val(placeCord.lng());
    $("#lat").val(placeCord.lat());
    get_address("market");
  });


}
google.maps.event.addDomListener(window, 'load', initialize);


function get_time_text(time)
              {

                var time_elapsed = Date.now()/1000 - parseInt(time); 
                var time_text = "";
                if (time_elapsed<60)
                    time_text = parseInt(time_elapsed) + ' seconds';

                else if(time_elapsed < 3600)
                {

                    var minutes = time_elapsed/60;
                    time_text = parseInt(minutes) + ' minutes';
                  }
                else if(time_elapsed < 3600*24)
                {
                    var hours = time_elapsed/3600;
                    time_text = parseInt(hours) + ' hours';
                  }
                else if(time_elapsed < 3600*24*365)
                {
                    var days = time_elapsed/3600/24;
                    time_text = parseInt(days) + ' days';
                  }
                else
                {
                    var years = time_elapsed/3600/24/365;
                    time_text = parseInt(years) + ' years';
                  }
                return time_text;
              }


 var latest_timestamp = 0;
              function update_latest_updates(data)
                {
                    var updates_result = jQuery.parseJSON(data);

                    var feeds = updates_result.result;
                    var updates  = "";
                    if(feeds.length>0)
                    {
                      latest_timestamp = updates_result.time;
                    }
                    for(var i = 0;i<feeds.length;i++)
                    {
                      var item = feeds[i];
                      updates +='<div class="update" data-toggle="popover" data-title="help" data-tweet-id="'+item.updates.tweet_id+'" data-trigger="manual" data-container="body" data-placement="left" data-original-title="" title="" data-html="true"  >';
                      updates += '<img src="'+item.profile_img+'" class="pull-left" style="width:25px; margin-right: 10px;" /><p class="margin-image-left-small">'+item.updates.status+'<br /><small class="text-muted">'+get_time_text(item.updates.time_stamp)+'</small> </p></div>';


                    }
                    $("#updates").prepend(updates).fadeIn('slow');
                }


function poll_latest_updates()
{

setTimeout(function() {   
   ajax_request("get_latest_updates", 'update_latest_updates',{time:latest_timestamp});
   poll_latest_updates();
    }, 60000); 

}



              $(document).ready(function(){
                
                poll_latest_updates();
                ajax_request("get_latest_updates", 'update_latest_updates',{time:latest_timestamp});
                 $("#updates").on("click",".update",function(e){ 
                  if($(this).attr('data-trigger')!="manual")
                    return;
                  var tweet_id = $(this).attr('data-tweet-id');
                  var that = this;

                  $.post( "/ajax-handler/get_single_tweet", { tweet_id:tweet_id }, function( data ) {
                    var content = "<div class='text-center'><p class=''>This is over 50 miles away. If you'd like to see it, please go ahead and ...</p><a href='/subscribe' class='btn btn-primary'>Upgrade</a></div>";
                      var title = "Aww shucks!!";
                    if(data.status == "ok")
                    {
                      var result = data.result;
                      var content = "<div class=''><div class='timeline-top-info'>";
                      content += "<div class='pull-right' style='margin-left: 5px;'>";
                      content += "<a type='button' class='btn btn-primary btn-xs' href='/"+result.username+"/post/"+result.updates.tweet_id+"'>";
                      content += "<i class='fa fa-arrow-right fa-lg' style='color:#fff;'></i> ";
                      content += "</a>";
                      content += "</div>   ";
                      content += "</div>";
                      content += "<div class='media margin-none'>   ";
                      content += "<div class=' '>";
                      content += result.updates.status;
                      content += "</div>"; 
                      content += "</div> ";
                      content += "<div class='timeline-bottom  border-top clearfix innerTB half'>";
                      content += "<a href='http://maps.google.com/maps?saddr=51.4529956141,-2.62451568043&amp;daddr=51.4619294,-2.5891196' target='_blank' data-placement='top' data-toggle='tooltip' class='pull-right' rel='tooltip' title='' data-original-title='Get directions'> ";
                      content += "<i class='fa fa-location-arrow fa-fw'></i> "+result.distance+" miles  ";
                      content += "</a>";
                      if(result.type_user.length>0)
                      {
                          content += "<i class='fa fa-home fa-fw'></i>";
                      }
                      
                      for(var index in result.type_user)
                      {
                        var biz_type = result.type_user[index];
                        content += '<a href="/activity/?b='+encodeURIComponent(biz_type)+'" class="innerR half">'+biz_type+'</a> ';
                      }
                      content += "</div> ";
                      content += "<div class='border-top innerT'> ";
                      if(result.replies_count>0)
                      {
                        content += "<p class='small text-center'>";
                        content += "<i class='fa fa-comments fa-fw'></i>";
                        content += "<a href='#'>See all "+result.replies_count+" replies</a>";
                        content += "</p>";
                      }
                      content += "<input class='form-control input-sm enterhandler reply_input' data-tweet-id='"+result.updates.tweet_id+"' data-main='main' type='text' placeholder='Reply to @"+result.username+"'  data-toggle='market-reply'  data-mentions='@"+result.username+"'> ";
                      content += "</div>";
                      content += "</div>";
                      var title = result.name;
                    }
                   
                   $(that).popover({
                              trigger : "click",
                              placement : 'left',
                              html : true,
                              title:title,
                              content: content
                          }).popover("show");
                       $(that).attr('data-trigger',"click");
 
}, "json");
                      
                });
                 });
