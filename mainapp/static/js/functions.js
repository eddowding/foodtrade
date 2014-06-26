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
		content += '<a href="/activity/?b='+biz_type+'" class="  small">'+biz_type+'</a> ';
	}
	content += '</div>';
	content += '<div class="media margin-none status">  ';
	content += '<div class="content">';
	content += '<div class="text  innerAll half"> ';
	content += '<p class="">'+user.description+'</p>';
	content += '</div>';
	content += '<div class="innerTB half border-top border-bottom"> ';
	content += '<span class="label label-default"><i class="fa fa-sign-in fa-fw"></i>BUYS</span> <b>';
	for(var index in user.foods.webuy_matches)
	{
		if(index>0)
		{
			content += ", ";
		}
		content += user.foods.webuy_matches[index];
	}

	content += '</b> &amp; '+(user.foods.webuy_count-user.foods.webuy_matches.length)+ ' more <br />';

	content += '<span class="label label-default"><i class="fa fa-sign-out fa-fw"></i>SELLS:</span> <b>';
	for(var index in user.foods.wesell_matches)
	{
		if(index>0)
		{
			content += ", ";
		}
		content += user.foods.wesell_matches[index];
	}
	content += '</b> &amp; '+(user.foods.wesell_count-user.foods.wesell_matches.length)+ ' more <br />';

	
	content += '</div> ';
	// content += '<div class="innerTB half clearfix"> ';
	// content += '<img src="http://pbs.twimg.com/profile_images/1690823879/Screen_shot_2011-12-13_at_12.21.20_bigger.png" alt="The Wallfish Bistro" class="img-responsive pull-left" style="width:40px; margin-right: 5px;">';
	// content += '<img src="http://pbs.twimg.com/profile_images/1690823879/Screen_shot_2011-12-13_at_12.21.20_bigger.png" alt="The Wallfish Bistro" class="img-responsive pull-left" style="width:40px; margin-right: 5px;">';
	// content += '<img src="http://pbs.twimg.com/profile_images/1690823879/Screen_shot_2011-12-13_at_12.21.20_bigger.png" alt="The Wallfish Bistro" class="img-responsive pull-left" style="width:40px; margin-right: 5px;">';
	// content += '<img src="http://pbs.twimg.com/profile_images/1690823879/Screen_shot_2011-12-13_at_12.21.20_bigger.png" alt="The Wallfish Bistro" class="img-responsive pull-left" style="width:40px; margin-right: 5px;">';
	// content += '</div> ';
	content += '</div>   ';
	content += '</div> ';
	content += '<div class="timeline-bottom innerTB half small border-top clearfix">';
	content += '<a href="http://maps.google.com/maps?saddr=51.4529956141,-2.62451568043&amp;daddr=51.454513,-2.58791" target="_blank" data-placement="top" data-toggle="tooltip" class="pull-left" rel="tooltip" title="" data-original-title="Get directions"> ';
	content += '<span class="hidden-sm hidden-xs truncate100 address">';
	content += '<i class="fa fa-map-marker fa-fw"></i>';
	content += user.address;
	content += '</span>';
	content += '</a> ';
	content += '<a href="http://maps.google.com/maps?saddr=51.4529956141,-2.62451568043&amp;daddr=51.4536248,-2.6241012" target="_blank" data-placement="top" data-toggle="tooltip" class="pull-right" rel="tooltip" title="" data-original-title="Get directions"> ';
	content += '<i class="fa fa-location-arrow fa-fw"></i> '+user.distance+' miles  ';
	content += '</a>';
	content += '</div>  ';
	content += '<div class="innerAll border-top bg-gray  reply" style="display: none;"> ';
	content += '<input class="form-control input-sm enterhandler reply_input" data-main="main" type="text" placeholder="Reply to @wallfishbristol" data-mentions="@wallfishbristol"> ';
	content += '</div>';
	content += '</div>';
	return content;

}







function get_box_update(update)
{
	content ='<div class="box-generic">';
	content +='<div class="timeline-top-info   border-bottom clearfix">';
	content +='<div class="pull-right" style="margin-left: 5px;">';
	content +='<a type="button" class="dropdown-toggle" data-toggle="dropdown">';
	content +='<i class="fa fa-fw fa-cog text-muted"></i>';
	content +='<span class="sr-only">Toggle Dropdown</span>';
	content +='</a>';
	content +='<a type="button" class="btn btn-primary btn-xs" href="/CoconutChilli/post/476663147080974336">';
	content +='<i class="fa fa-arrow-right " style="color:#fff;"></i> ';
	content +='</a>';
	content +='<ul class="dropdown-menu" role="menu">  ';
	content +='<li><a href="http://www.facebook.com/sharer/sharer.php?u=http://foodtrade.com/CoconutChilli/post/476663147080974336" target="_blank"><i class="fa fa-facebook fa-fw facebook"></i> Share on Facebook</a></li>';
	content +='<li><a href="http://twitter.com/home?status=%40foodtradeHQ%20Did%20u%20read%20shocking%20%40guardian%20story%202ay%20about%20human%20slavery%20on%20boats%20catching%20shrimps%3F%20Truly%20horrific%20http%3A//t.co/SIXbWohPT6%20http://foodtrade.com/CoconutChilli/post/476663147080974336" target="_blank"><i class="fa fa-twitter fa-fw twitter "></i> Share on Twitter</a></li>';
	content +='<li><a type="button" href="/'+update.username+'">';
	content +='<i class="fa fa-info-circle fa-lg fa-fw"></i> View profile</a></li>   ';
	content +='<li><a href="#" onclick="click_activity(\'follow\',\'CoconutChilli\')"><i class="fa fa-star-o fa-fw"></i>  Follow on Twitter</a></li>';
	content +='<li><a href="#" class="deletetweet" data-tweet-id="476663147080974336"><i class="fa fa-trash-o fa-fw flag"></i> Delete</a></li>';
	content +='<li><a href="#" onclick="click_activity(\'spam\',\'476663147080974336 \')" class=" "><i class="fa fa-flag-o flag fa-fw"></i> Report</a></li>';
	content +='</ul>  ';
	content +='</div>  ';
	content +='<img src="'+update.profile_img+'" alt="Navina Bartlett" class="img-responsive pull-left" style="width:40px; margin-right: 5px;">';
	content +='<h4 class="margin0"><a href="/'+update.username+'" class="text-inverse"> ';
	content +='<strong>  '+update.name+'  </strong> </a> </h4>';
	content +='<a href="/activity/?b=Ready meals" class="innerR half small">Ready meals</a>';
	content +='</div>';
	content +='<div class="media margin-none status">   ';
	content +='<div class="innerTB ">';
	content +=update.updates.status;
	content +='</div>';
	content +='</div> ';
	content +='<div class="timeline-bottom small border-top clearfix">';
	content +='<a href="http://maps.google.com/maps?saddr='+update.latlng.coordinates[0]+',-'+update.latlng.coordinates[1]+'&amp;daddr=51.454513,-2.58791" target="_blank" data-placement="top" data-toggle="tooltip" class="pull-right" rel="tooltip" title="" data-original-title="Get directions"> ';
	content +='<span class="hidden-sm hidden-xs truncate100 address">';
	content +='<i class="fa fa-map-marker fa-fw"></i>';
	content += update.address;
	content +='</span>';
	content +='</a> ';
	content +='<a href="/'+update.username+'/post/'+update.updates.tweet_id+'">';
	content +='<i class="fa fa-calendar  fa-fw"></i>' + get_time_text(update.updates.time_stamp)+' ago';
	content +='</a>';
	content +='</div>  ';
	content +='<div class="innerAll half border-top bg-gray "> ';
	content +='<input class="form-control input-sm enterhandler reply_input" data-toggle="market-reply" data-tweet-id="'+update.updates.tweet_id+'" data-main="main" type="text" placeholder="Reply to '+update.username+'" data-mentions="@'+update.username+'"> ';
	content +='</div>';
	content +='</div>';
	return content;
}





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

function map_update_card(user)
{
  var con = user;
      var name = con.name;
      var status =  con.updates.status;
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

    card_str += '<p>'+status+'</p></div>';
    card_str += '<a href="/profile/'+username+'" class="btn btn-primary btn-sm">View profile &raquo;</a></div> </div>';
    return card_str;
}