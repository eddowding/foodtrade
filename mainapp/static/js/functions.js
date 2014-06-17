function get_box_profile(user)
{
  var content = "";

	content += '<div class="box-generic">';
	content += '<div class="timeline-top-info border-bottom clearfix">';
	content += '<div class="pull-right" style="margin-left: 5px;">';
	content += '<a type="button" class="dropdown-toggle" data-toggle="dropdown">';
	content += '<i class="fa fa-fw fa-cog text-muted"></i>';
	content += '<span class="sr-only">Toggle Dropdown</span>';
	content += '</a>';
	content += '<a type="button" class="btn btn-primary btn-xs" href="/'+user.username+'">';
	content += '<i class="fa fa-arrow-right fa-lg" style="color:#fff;"></i> ';
	content += '</a>';
	content += '<ul class="dropdown-menu" role="menu">  ';
	content += '<li><a href="http://www.facebook.com/sharer/sharer.php?u=http://foodtrade.com/profile/wallfishbristol" target="_blank"><i class="fa fa-facebook fa-fw facebook"></i> Share on Facebook</a></li>';
	content += '<li><a href="http://twitter.com/home?status=We%20are%20now%20open%20and%20taking%20bookings.%20Owned%20and%20run%20by%20staff%20who%20have%20done%20time%20with%20Hix%2C%20River%20Cottage%2C%20Le%20Caf%C3%A9%20Anglais%20and%20Ducksoup%20http://foodtrade.com/profile/wallfishbristol" target="_blank"><i class="fa fa-twitter fa-fw twitter "></i> Share on Twitter</a></li>';
	content += '<li><a type="button" href="/profile/wallfishbristol/">';
	content += '<i class="fa fa-info-circle fa-lg fa-fw"></i> View profile</a></li> ';
	content += '<li><a href="#" onclick="click_activity(\'follow\',\''+user.username+'\')"><i class="fa fa-star-o fa-fw"></i>  Follow on Twitter</a></li>';
	content += '<li><a href="#" onclick="click_activity(\'spam\',\''+user.username+'\')" class=" "><i class="fa fa-flag-o flag fa-fw"></i> Report</a></li>';
	content += '</ul>  ';
	content += '</div>  ';
	content += '<img src="'+user.profile_img+'" alt="The Wallfish Bistro" class="img-responsive pull-left" style="width:50px; margin-right: 5px;">';

	content += '<h4 class="margin0"><a href="/'+user.username+'" class="text-inverse">';
	content += user.name;
	content += '</a></h4> ';
	for(var index in user.type_user)
	{
		var biz_type = user.type_user[index];
		content += '<a href="/activity/?b='+biz_type+' class="  small">'+biz_type+'</a> ';
	}
	content += '</div>';
	content += '<div class="media margin-none status">  ';
	content += '<div class="content">';
	content += '<div class="text  innerAll half"> ';
	content += '<p class="">'+user.description+'</p>';
	content += '</div>';
	content += '<div class="innerTB half border-top border-bottom"> ';
	content += '<span class="label label-default"><i class="fa fa-sign-in fa-fw"></i>BUYS</span> <b>Carrots</b> &amp; 18 more <br />';
	content += '<span class="label label-default"><i class="fa fa-sign-out fa-fw"></i>SELLS:</span> Fish <-- this is the name of the matching item';
	content += '</div> ';
	content += '<div class="innerTB half clearfix"> ';
	content += '<img src="http://pbs.twimg.com/profile_images/1690823879/Screen_shot_2011-12-13_at_12.21.20_bigger.png" alt="The Wallfish Bistro" class="img-responsive pull-left" style="width:40px; margin-right: 5px;">';
	content += '<img src="http://pbs.twimg.com/profile_images/1690823879/Screen_shot_2011-12-13_at_12.21.20_bigger.png" alt="The Wallfish Bistro" class="img-responsive pull-left" style="width:40px; margin-right: 5px;">';
	content += '<img src="http://pbs.twimg.com/profile_images/1690823879/Screen_shot_2011-12-13_at_12.21.20_bigger.png" alt="The Wallfish Bistro" class="img-responsive pull-left" style="width:40px; margin-right: 5px;">';
	content += '<img src="http://pbs.twimg.com/profile_images/1690823879/Screen_shot_2011-12-13_at_12.21.20_bigger.png" alt="The Wallfish Bistro" class="img-responsive pull-left" style="width:40px; margin-right: 5px;">';
	content += '</div> ';
	content += '</div>   ';
	content += '</div> ';
	content += '<div class="timeline-bottom innerTB half small border-top clearfix">';
	content += '<a href="http://maps.google.com/maps?saddr=51.4529956141,-2.62451568043&amp;daddr=51.454513,-2.58791" target="_blank" data-placement="top" data-toggle="tooltip" class="pull-left" rel="tooltip" title="" data-original-title="Get directions"> ';
	content += '<span class="hidden-sm hidden-xs truncate100 address">';
	content += '<i class="fa fa-map-marker fa-fw"></i>';
	content += 'Bristol, City of Bristol, UK';
	content += '</span>';
	content += '</a> ';
	content += '<a href="http://maps.google.com/maps?saddr=51.4529956141,-2.62451568043&amp;daddr=51.4536248,-2.6241012" target="_blank" data-placement="top" data-toggle="tooltip" class="pull-right" rel="tooltip" title="" data-original-title="Get directions"> ';
	content += '<i class="fa fa-location-arrow fa-fw"></i> 0.0 miles  ';
	content += '</a>';
	content += '</div>  ';
	content += '<div class="innerAll border-top bg-gray  reply" style="display: none;"> ';
	content += '<input class="form-control input-sm enterhandler reply_input" data-main="main" type="text" placeholder="Reply to @wallfishbristol" data-mentions="@wallfishbristol"> ';
	content += '</div>';
	content += '</div>';
	return content;

}



function map_profile_card(user)
{
  var con = user;
      var name = con.name;
      var status =  con.description;
      var profile_img = con.profile_img;
      var username = con.username;
      var banner = con.banner_url;
      var description = con.description;
      var type_user = con.type_user;
      var sign_up_as = con.sign_up_as;
      if(!type_user)
      {
        type_user = [];
      }


      
      // if(sign_up_as != "Business")
      // {
      //  continue;
      // }

      // if(current_lon == def_lon && current_lat == def_lat)
      //     {
      //       continue;
      //     }
      
var card_str = '<div class="card-box"><div class="content text-center"><div class=""><a href="/profile/'+username+'"><img src="'+profile_img+'" alt="'+name+'" class="img-circle img-thumbnail img-responsive" style="width:73px;" /></a>';
    card_str += '</div><div class="text"><h3><a href="/profile/'+username+'">'+name+'</a></h3>';

    if(type_user.length>0)
    {
      card_str += '<div class="  clearfix">';
      for(var j=0;j<type_user.length;j++)
      {  
        
        card_str +=  '<a class="" href="/activity/?b='+type_user[j]+'">'+type_user[j]+'</a>';
       }
        card_str += '</div>';
    }

    card_str += '<p>'+description+'</p></div>';
    card_str += '<a href="/profile/'+username+'" class="btn btn-primary btn-sm">View profile &raquo;</a></div> </div>';
    return card_str;
}