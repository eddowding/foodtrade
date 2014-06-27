


var Search = {
    keyword :"",
    search_type:"produce",
    filters:{profile:{want:"all",lng:"",lat:"", location:"", usertype:"all", org:"[]", biz:"[]"},
    market:{want:"all",lng:"",lat:"", location:"", usertype:"all", org:"[]", biz:"[]"}},
    tab:"market",
    profile_results:{},
    market_results:{},
    load_state: function () {
        this.keyword = getParameterByName('q', this.keyword);

        this.search_type = getParameterByName('stype', this.search_type);
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
    		query += "porg"+encodeURIComponent(this.filters.profile.org)+'&';
        }
    	
        if(this.filters.profile.biz != "")
        {           
            query += "pbiz"+encodeURIComponent(this.filters.profile.biz)+'&';
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
            query += "mbiz"+encodeURIComponent(this.filters.market.biz)+'&';
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
            $("#search_type").html("<i class='fa fa-cutlery icon'></i> <span class='hidden-xs'>Produce</span><i class='fa fa-caret-down'></i>");
            $("#search_type_option").html("Profile");

        }
        else
        {
            $("#search_type").html("Profile");
            $("#search_type_option").html("Produce");
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
        var updates = this.market_results.result;
        var html_content = "";
         for(var i=0;i<updates.length;i++)
          {
            html_content += get_box_update(updates[i]);
          }
          $("#mkt_results").html(html_content);
          if(this.tab == "market")
          {
            show_connections_on_map();
          }
          $('.dropdown-toggle').dropdown();
    },

    show_profiles : function()
    {
        var profiles = this.profile_results.result;
        var html_content = "";
         for(var i=0;i<profiles.length;i++)
          {
            html_content += get_box_profile(profiles[i]);
          }
          $("#profile_results").html(html_content);
          if(this.tab == "profile")
          {
            show_connections_on_map();
          }
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
            if(with_filter==true)
            {
                req_obj.org = this.filters.profile.org;
                req_obj.biz = this.filters.profile.biz;
            }


        $.post( "/ajax-handler/search_profiles", req_obj, function( data ) {
        Search.profile_results = data;

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
            if(with_filter == true)
            {
                req_obj.org = this.filters.market.org;

                req_obj.biz = this.filters.market.biz;
            }

         $.post( "/ajax-handler/search_market", req_obj , function( data ) {
              Search.market_results = data;
              Search.show_market();
              if(!with_filter)
              {  
                    Search.set_market_filters();
                }

             }, "json"); 
     },

      set_market_filters : function()
    {
         $.post( "/ajax-handler/get_market_filter", { q: this.keyword, 
            search_type:this.search_type, 
            lng:this.filters.market.lng, 
            lat:this.filters.market.lat,
            want:this.filters.market.want,
            usertype: this.filters.market.usertype }, function( data ) {
                var results = data.result.org;
                var options = "";
                for(var i=0;i<results.length;i++)
                {
                    options += "<option>"+results[i]._id+"</option>";
                }
                $("#filter_mkt_org").html(options);
                var biz_results = data.result.biz;
                var biz_options = "";
                for(var i=0;i<biz_results.length;i++)
                {
                    biz_options += "<option>"+biz_results[i]._id+"</option>";
                }
                $("#filter_mkt_biz").html(biz_options);
                 $('.selectpicker').selectpicker('refresh');

                 listen_filters("mktplace");
 
            }, "json");

    },
          set_profile_filters : function()
    {
         $.post( "/ajax-handler/get_profile_filter", { q: this.keyword, 
            search_type:this.search_type, 
            lng:this.filters.profile.lng, 
            lat:this.filters.profile.lat,
            want:this.filters.profile.want,
            usertype: this.filters.profile.usertype }, function( data ) {
                var results = data.result.org;
                var options = "";
                for(var i=0;i<results.length;i++)
                {
                    options += "<option>"+results[i]._id+"</option>";
                }
                $("#filter_profile_org").html(options);
                var biz_results = data.result.biz;
                var biz_options = "";
                for(var i=0;i<biz_results.length;i++)
                {
                    biz_options += "<option>"+biz_results[i]._id+"</option>";
                }
                $("#filter_profile_biz").html(biz_options);
                 $('.selectpicker').selectpicker('refresh');
                 listen_filters("profiles");
 
}, "json");

    },


    search_start: function()
    {
        this.keyword = $("#search_query").val();
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
    Search.search_start();
    return false;
}




function listen_filters(filter_for)
{
    var filter_event = function () {
        var class_name = $(this).attr('class');
        console.log("ticked");
        if(class_name.indexOf('ticked')!=-1)
        {
            $(this).removeClass("ticked");

        }
        else
        {
            $(this).addClass("ticked");
        }

        
    var current_tab = "profile";
    if(Search.tab == "market")
    {
        current_tab = "mkt";
    }
    var filter_type = ["org","biz"];
    for(var i = 0;i<filter_type.length;i++)
    {
        var selects = $($("#filter_"+current_tab+"_"+filter_type[i]).parent()).find($("ul.dropdown-menu.selectpicker li.ticked a"));
        var filter_string = [];
        for(var j = 0;j<selects.length;j++)
        {            
                filter_string.push(selects[j].text);            
        }
       
        Search.filters[Search.tab][filter_type[i]] = JSON.stringify(filter_string);
        console.log(filter_string);
        Search.set_url();
    }
    if(Search.tab == "market")
    {

        Search.search_market(true);
    }
    else{
        Search.search_profiles(true);
    }
};
    $('div#'+filter_for+' ul.dropdown-menu.selectpicker li').on('click', filter_event);    
}




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
        $("#search_type").html("Profile");
        $("#search_type_option").html("Produce");

    }
    else if(Search.search_type=="profile")
    {
        Search.toggle_type();
        $("#search_type").html("Produce");
        $("#search_type_option").html("Profile");
    }
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
      Search.filters[address_for].lng = results[0].geometry.location.lng();
      Search.filters[address_for].lat = results[0].geometry.location.lat();
     Search.set_url();
     if(address_for=="market")
     {

        Search.search_market();
     }
     else
     {
        Search.search_profiles();
     }
              } 
            }
            else
            {
              alert("No address found");
            }
          });
    return false;  
}