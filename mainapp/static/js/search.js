

var initial_flag = true;
var Search = {
    keyword :"",
    search_type:"produce",
    filters:{profile:{want:"all",lng:"",lat:"", location:"", usertype:"all", org:"[]", biz:"[]"},
    market:{want:"all",lng:"",lat:"", location:"", usertype:"all", org:"[]", biz:"[]"}},
    tab:"profile",
    profile_results:[],
    market_results:[],
    load_state: function () {
        this.keyword = getParameterByName('q', this.keyword);

        this.search_type = getParameterByName('stype', this.search_type);
        $("#search_stype").val(this.search_type);
        
        this.tab= getParameterByName('tab', this.tab);
        
        this.filters.profile.want = getParameterByName('pwant', this.filters.profile.want);
        this.filters.profile.location = getParameterByName('plocation', this.filters.profile.location);
        this.filters.profile.lng = getParameterByName('plng', this.filters.profile.lng);
        this.filters.profile.lat = getParameterByName('plat', this.filters.profile.lat);
        this.filters.profile.usertype = getParameterByName('put', this.filters.profile.usertype);
        this.filters.profile.org = getParameterByName('porg', this.filters.profile.org);
        this.filters.profile.biz = getParameterByName('pbiz', this.filters.profile.biz);


        this.filters.market.want = getParameterByName('mwant', this.filters.market.want);
        this.filters.market.location = getParameterByName('mlocation', this.filters.market.location);
        this.filters.market.lng = getParameterByName('mlng', this.filters.market.lng);
        this.filters.market.lat = getParameterByName('mlat', this.filters.market.lat);
        this.filters.market.usertype = getParameterByName('mut', this.filters.market.usertype);
        
        this.filters.market.org = getParameterByName('morg', this.filters.market.org);
        
        this.filters.market.biz = getParameterByName('mbiz', this.filters.market.biz);
    },
    set_url:function(){
    	var query="?";
    	var first_item = false;
    	if(this.keyword!="")
    	{
    		query += "q="+encodeURIComponent(this.keyword)+"&";
    	}
        if(this.tab!="")
        {
            query += "tab="+encodeURIComponent(this.tab)+"&";
        }
    	if(this.stype!="")
    	{

    		query += "stype="+encodeURIComponent(this.search_type)+"&";
    	}


        // for profile
    	if(this.filters.profile.want!="")
    	{
    		query += "pwant="+encodeURIComponent(this.filters.profile.want)+"&";
    	}
        if(this.filters.profile.location!="")
        {
            query += "plocation="+encodeURIComponent(this.filters.profile.location)+"&";
        }
        if(this.filters.profile.lng!="")
        {
            query += "plng="+encodeURIComponent(this.filters.profile.lng)+"&";
        }
        if(this.filters.profile.lat!="")
        {
            query += "plat="+encodeURIComponent(this.filters.profile.lat)+"&";
        }

    	if(this.filters.profile.usertype !="")
    	{
    		query += "put="+encodeURIComponent(this.filters.profile.usertype)+"&";
    	}

    	if(this.filters.profile.org != "")
    	{    		
    		query += "porg="+encodeURIComponent(this.filters.profile.org)+'&';
        }
    	
        if(this.filters.profile.biz != "")
        {           
            query += "pbiz="+encodeURIComponent(this.filters.profile.biz)+'&';
        }


        // for market
        if(this.filters.market.want!="")
        {
            query += "mwant="+encodeURIComponent(this.filters.market.want)+"&";
        }
        if(this.filters.market.location!="")
        {
            query += "mlocation="+encodeURIComponent(this.filters.market.location)+"&";
        }
        if(this.filters.market.lng!="")
        {
            query += "mlng="+encodeURIComponent(this.filters.market.lng)+"&";
        }
        if(this.filters.market.lat!="")
        {
            query += "mlat="+encodeURIComponent(this.filters.market.lat)+"&";
        }

        if(this.filters.market.usertype !="")
        {
            query += "mut="+encodeURIComponent(this.filters.market.usertype)+"&";
        }

        if(this.filters.market.org != "")
        {           
            query += "morg="+encodeURIComponent(this.filters.market.org)+'&';
        }        
        if(this.filters.market.biz != "")
        {           
            query += "mbiz="+encodeURIComponent(this.filters.market.biz)+'&';
        }
        var last_item = query[query.length-1];
        if(last_item=='&')
        {
            query = query.substring(0, query.length - 1);
        }
    	window.history.pushState('Object', 'Title', '/activity'+query);
    },
    set_ui : function()
    {
        if(this.search_type=="produce")
        {
            $("#search_type").html(" <span class='hidden-xs'>in Produce</span><i class='fa fa-caret-down'></i>");
            $("#search_type_option").html("in Profiles ");

        }
        else
        {
            $("#search_type").html("in Profiles <i class='fa fa-caret-down'></i>");
            $("#search_type_option").html("in Produce");
            $("#result_tabs").addClass( "hidden" );
             $("#mktplace").removeClass("active");
            $("#profiles").addClass("active");
        }



        var want_btns = $(".btn-mwant");
        for(var i = 0; i<want_btns.length;i++)
        {
            if($(want_btns[i]).html()==this.filters.market.want)
            {
                $(want_btns[i]).addClass('active');
            }
        }


        var mut_btns = $(".btn-mut");
        for(var i = 0; i<mut_btns.length;i++)
        {
            if($(mut_btns[i]).html()==this.filters.market.usertype)
            {
                $(mut_btns[i]).addClass('active');
            }
        }




        $("#search_query").val(this.keyword);

    },
    toggle_type : function()
    {

        if(this.search_type=="produce")
        {
            this.search_type = "profile";
            $("#result_tabs").addClass( "hidden" );
            $("#mktplace").removeClass("active");
            $("#profiles").addClass("active");
            this.tab = "profile";
            

        }
        else if(this.search_type=="profile")
        {
            this.search_type = "produce";
            $("#result_tabs").removeClass( "hidden" );
        }

    },
    show_market : function()
    {
        var updates = this.market_results;
        var html_content = "";
        if(updates.length==0)
        {
            html_content = "<div class='innerAll'><p><b>Sorry! There are no results for this search.</b></p>  <p>Things to try:</p><ul><li>check the spelling</li><li> removing filters</li><li>broadening your search term  (e.g. instead of 'truffles' search 'confectionary')</li><li>zooming out to cover a larger area</li></ul><p>We're getting bigger and better everyday, but it might be that no one has added this to the food web yet. </p><div class='innerTB text-center'><button type='button' class='btn btn-primary' data-toggle='collapse' data-target='#newtwitterpost' style='font-weight: normal;' onclick='window.scrollTo(0,0);'><i class='fa fa-bullhorn fa-lg fa-fw'></i>Post a request in the marketplace</button></div></div>";        }
        else
        {
            show_connections_on_map();
        }
         for(var i=0;i<updates.length;i++)
          {
            html_content += get_box_update(updates[i]);
          }
          $("#mkt_results").html(html_content);
          correct_image_load_errors();
          
          $('.dropdown-toggle').dropdown();
    },

    show_profiles : function()
    {
        var profiles = this.profile_results;
        var html_content = "";
        if(profiles.length==0)
        {
            html_content = "<div class='innerAll'><p><b>Sorry! There are no results for this search.</b></p>  <p>Things to try:</p><ul><li>check the spelling</li><li> removing filters</li><li>broadening your search term  (e.g. instead of 'truffles' search 'confectionary')</li><li>zooming out to cover a larger area</li></ul><p>We're getting bigger and better everyday, but it might be that no one has added this to the food web yet. </p><div class='innerTB text-center'><button type='button' class='btn btn-primary' data-toggle='collapse' data-target='#newtwitterpost' style='font-weight: normal;' onclick='window.scrollTo(0,0);'><i class='fa fa-bullhorn fa-lg fa-fw'></i>Post a request in the marketplace</button></div></div>";
        }
        else
        {
            show_connections_on_map();
        }
         for(var i=0;i<profiles.length;i++)
          {
            html_content += get_box_profile(profiles[i]);
          }
          $("#profile_results").html(html_content);
          correct_image_load_errors();
          
          $('.dropdown-toggle').dropdown();

    },
    search_profiles : function(with_filter)
    {
        var req_obj = { q: this.keyword, 
            search_type:this.search_type, 
            lng:this.filters.profile.lng, 
            lat:this.filters.profile.lat,
            want:this.filters.profile.want,
            usertype:this.filters.profile.usertype
            };
            
                req_obj.org = this.filters.profile.org;
                req_obj.biz = this.filters.profile.biz;
            
        $.post( "/ajax-handler/search_profiles", req_obj, function( data ) {
        Search.profile_results = data.result;

        Search.show_profiles();
        if(!with_filter)
        {
            Search.set_profile_filters();
        }

        }, "json");

    },
    search_market : function(with_filter)
    {
        var req_obj = { q: this.keyword, 
            search_type:this.search_type, 
            lng:this.filters.market.lng, 
            lat:this.filters.market.lat,
            want:this.filters.market.want,
            usertype: this.filters.market.usertype };
            
            req_obj.org = this.filters.market.org;

            req_obj.biz = this.filters.market.biz;
            

         $.post( "/ajax-handler/search_market", req_obj , function( data ) {
              Search.market_results = data.result;
              Search.show_market();
              if(!with_filter)
              {  
                    Search.set_market_filters();
                }

             }, "json"); 
     },
     clear_filters : function(filter_type)
     {
        Search.filters[filter_type].org = "[]";
        Search.filters[filter_type].biz = "[]";
     },

      set_market_filters : function()
    {
        var that = this;
         $.post( "/ajax-handler/get_market_filter", { q: this.keyword, 
            search_type:this.search_type, 
            lng:this.filters.market.lng, 
            lat:this.filters.market.lat,
            want:this.filters.market.want,
            usertype: this.filters.market.usertype }, function( data ) {
                var results = data.result.org;
                var options = "";
                var market_filters_org = JSON.parse(Search.filters.market.org);
                for(var i=0;i<results.length;i++)
                {
                    var selected_text = " ";
                    if(market_filters_org.indexOf(results[i]._id)>=0)
                    {
                        selected_text = " selected ";
                    }
                    options += "<option"+selected_text+"value='"+results[i]._id+"'>"+results[i]._id+"</option>";
                }
                $("#filter_mkt_org").html(options);
                var biz_results = data.result.biz;
                var biz_options = "";
                var market_filters_biz = JSON.parse(Search.filters.market.biz);
                for(var i=0;i<biz_results.length;i++)
                {
                    var selected_text = " ";
                    if(market_filters_biz.indexOf(biz_results[i]._id)>=0)
                    {
                        selected_text = " selected ";
                    }
                    biz_options += "<option"+selected_text+"value='"+biz_results[i]._id+"'>"+biz_results[i]._id+"</option>";
                }

                $("#filter_mkt_biz").html(biz_options);
                 $('.selectpicker').selectpicker('refresh');
                 // $("#filter_mkt_biz").selectpicker('val', market_filters_biz); 


                 // $("#filter_mkt_org").selectpicker('val', market_filters_org); 
               
            }, "json");

    },
          set_profile_filters : function()
    {
        var that = this;
         $.post( "/ajax-handler/get_profile_filter", { q: this.keyword, 
            search_type:this.search_type, 
            lng:this.filters.profile.lng, 
            lat:this.filters.profile.lat,
            want:this.filters.profile.want,
            usertype: this.filters.profile.usertype }, function( data ) {
                var results = data.result.org;
                var options = "";

                var profile_filters_org = JSON.parse(Search.filters.profile.org);
                for(var i=0;i<results.length;i++)
                {
                    var selected_text = " ";
                    if(profile_filters_org.indexOf(results[i]._id)>=0)
                    {
                        selected_text = " selected ";
                    }
                    options += "<option"+selected_text+"value='"+results[i]._id+"'>"+results[i]._id+"</option>";
                }
                $("#filter_profile_org").html(options);

                var biz_results = data.result.biz;
                var biz_options = "";
                var profile_filters_biz = JSON.parse(Search.filters.profile.biz);
                for(var i=0;i<biz_results.length;i++)
                {
                    var selected_text = " ";
                    if(profile_filters_biz.indexOf(biz_results[i]._id)>=0)
                    {
                        selected_text = " selected ";
                    }
                    biz_options += "<option"+selected_text+"value='"+biz_results[i]._id+"'>"+biz_results[i]._id+"</option>";
                }

                $("#filter_profile_biz").html(biz_options);
                 $('.selectpicker').selectpicker('refresh');
                 // $("#filter_profile_biz").selectpicker('val', profile_filters_biz); 
                 // $("#filter_profile_org").selectpicker('val', profile_filters_org);  
}, "json"); },


    search_start: function()
    {
        this.keyword = $("#search_query").val();
        this.clear_filters("market");
        this.clear_filters("profile");
        this.set_url();
        if(this.search_type=="produce")
        {
            
       
            this.search_market();
        }
        this.search_profiles();
    },
    init : function()
    {
        this.load_state();
        this.set_ui();
        if(this.tab == "profile")
        {
            $("#profile_tab").parent().addClass('active');
            $("#mkt_tab").parent().removeClass('active');
            $("#profiles").addClass('active');
            $("#mktplace").removeClass('active');
        }
        else
        {
            $("#mkt_tab").parent().addClass('active');
            $("#profile_tab").parent().removeClass('active');


             $("#profiles").removeClass('active');
            $("#mktplace").addClass('active');
        }
        if(this.search_type=="produce")
        {
            this.search_market();
        }
        this.search_profiles();
        var lng = parseFloat(this.filters[this.tab].lng);
        var lat = parseFloat(this.filters[this.tab].lat);
        load_map(lat,lng);


    }

}


function start_search()
{
    initial_flag = true;
    console.log("nepal");
    Search.search_start();

    return false;

    if(this.tab == "profile"&& this.search_type=="produce")
          {
            


            if(this.market_results.length>0 && profiles.length == 0)
            {
                this.tab = "market"
                $("#mkt_tab").parent().addClass('active');
            $("#profile_tab").parent().removeClass('active');


             $("#profiles").removeClass('active');
            $("#mktplace").addClass('active');
       
            }
          }
          if(this.tab == "market")
          {
            


            if(this.profile_results.length>0 && updates.length == 0)
            {
                this.tab = "profile"
                $("#profile_tab").parent().addClass('active');
            $("#mkt_tab").parent().removeClass('active');
            $("#profiles").addClass('active');
            $("#mktplace").removeClass('active');
       
            }
          }
}

$(".selectpicker").change(function(){
    var current_tab = "profile";
    if(Search.tab == "market")
    {
        current_tab = "mkt";
    }
    
     var filter_type = ["org","biz"];
    for(var i = 0;i<filter_type.length;i++)
    {
        var current_filters = $("#filter_"+current_tab+"_"+filter_type[i]).val();
        if(current_filters==null)
        {
            
        
            current_filters = [];
        }
        Search.filters[Search.tab][filter_type[i]] = JSON.stringify(current_filters);
    }   
     Search.set_url();
    
    if(Search.tab == "market")
    {

        Search.search_market(true);
    }
    else{
        Search.search_profiles(true);
    }
});



$("#profile_tab").click(function(){
Search.tab = "profile";
Search.set_url();
show_connections_on_map();

});



$("#mkt_tab").click(function(){
Search.tab = "market";
Search.set_url();
show_connections_on_map();

});

$("#search_type_option").click(function(){
    if(Search.search_type=="produce")
    {
        Search.toggle_type();
        $("#search_type").html("in Profiles");
        $("#search_type_option").html("in Produce");

    }
    else if(Search.search_type=="profile")
    {
        Search.toggle_type();
        $("#search_type").html("in Produce");
        $("#search_type_option").html("in Profiles");
    }
});


$(".tab-content").on("mouseenter",".box-generic",function(){
var box_username = $(this).attr('data-username');
var ctrl = Search.map_controls[box_username];
var latlng = ctrl.getLatLng();
var lat = latlng.lat;
var lng = latlng.lng;

var box_userid = $(this).attr('data-userid');


highlight_connections(box_userid);

// markers.removeLayer(ctrl);
// ctrl.addTo(map)
// .openPopup();
ctrl.openPopup();

map.panTo(new L.LatLng(lat,lng));

// ctrl.openPopup({keepInView:true});

}).on('mouseleave','.box-generic',function(){
    var box_username = $(this).attr('data-username');
    var ctrl = Search.map_controls[box_username];


    var box_userid = $(this).attr('data-userid');


unhightlight_connections(box_userid);
// markers.addLayer(ctrl);
// map.removeLayer(ctrl);
    ctrl.closePopup();
});

function getParameterByName(name,initial) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? initial : decodeURIComponent(results[1].replace(/\+/g, " "));
}

Search.init();

$(".btn-mwant").on('click', function(e){  
    if(Search.filters.market.want == $(this).html())
    {
        Search.filters.market.want = "all";
        $(this).removeClass("active").siblings().removeClass('active');
    }
    else
    {
        Search.filters.market.want = $(this).html();
        $(this).addClass("active").siblings().removeClass('active');
    }
    Search.set_url();
    Search.search_market();
});

$(".btn-mut").on('click', function(e){  
    if(Search.filters.market.usertype == $(this).html())
    {
        Search.filters.market.usertype = "all";
        $(this).removeClass("active").siblings().removeClass('active');
    }
    else
    {
        Search.filters.market.usertype = $(this).html();
        $(this).addClass("active").siblings().removeClass('active');
    }
    Search.set_url();
    Search.search_market();
});



$(".btn-pwant").on('click', function(e){  
    if(Search.filters.profile.want == $(this).html())
    {
        Search.filters.profile.want = "all";
        $(this).removeClass("active").siblings().removeClass('active');
    }
    else
    {
        Search.filters.profile.want = $(this).html();
        $(this).addClass("active").siblings().removeClass('active');
    }
    Search.set_url();
    Search.search_profiles();
});

$(".btn-put").on('click', function(e){  
    if(Search.filters.profile.usertype == $(this).html())
    {
        Search.filters.profile.usertype = "all";
        $(this).removeClass("active").siblings().removeClass('active');
    }
    else
    {
        Search.filters.profile.usertype = $(this).html();
        $(this).addClass("active").siblings().removeClass('active');
    }
    Search.set_url();
    Search.search_profiles();
});



function get_address(address_for) {

  var input = (document.getElementById('pac_input_'+address_for));
    geocoder = new google.maps.Geocoder();
    geocoder.geocode({'address': input.value}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
              if (results[0]) {
                var formatted_address = results[0].formatted_address;

      input.value = formatted_address;
      var lat = results[0].geometry.location.lat();
      var lng = results[0].geometry.location.lng();
      Search.filters[address_for].lng = lng;
      Search.filters[address_for].lat = lat;
     Search.set_url();
     if(address_for=="market")
     {
        Search.clear_filters("market");
        Search.search_market();
        
     }
     else
     {
        Search.clear_filters("profile");
        Search.search_profiles();
     }
     map.panTo(new L.LatLng(lat,lng));
              } 
            }
            else
            {
              alert("No address found");
            }
          });
    return false;  
}


     