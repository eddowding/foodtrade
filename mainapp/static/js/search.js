


var Search = {
    keyword :"",
    search_type:"produce",
    filters:{profile:{want:"all",lng:"",lat:"", location:"", usertype:"company", org:[], biz:[]},
    market:{want:"all",lng:"",lat:"", location:"", usertype:"company", org:[], biz:[]}},
    tab:"market",
    profile_results:{},
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
            $("#search_type").html("Produce");
            $("#search_type_option").html("Profile");

        }
        else
        {
            $("#search_type").html("Profile");
            $("#search_type_option").html("Produce");

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
        

    }
    else if(this.search_type=="profile")
    {
        this.search_type = "produce";
        $("#result_tabs").removeClass( "hidden" );
    }

    },
    load_results : function()
    {
        this.show_profiles();
        show_connections_on_map();
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

    },
    search_profiles : function()
    {
        $.post( "/ajax-handler/search_profiles", { q: this.keyword, search_type:this.search_type, lng:this.filters.profile.lng, lat:this.filters.profile.lat }, function( data ) {
  Search.profile_results = data;
  Search.load_results();
 
}, "json");

    },

    search_start: function()
    {
        this.keyword = $("#search_query").val();
        this.set_url();
        if(this.tab=="profile")
        {
            this.search_profiles();
        }
        else
        {
            this.search_profiles();
        }
        
    },


    init : function()
    {
        this.load_state();
        this.set_ui();
        if(this.tab == "profile")
        {
            console.log("profile");
            this.search_profiles();
            $("#profile_tab").parent().addClass('active');
            $("#mkt_tab").parent().removeClass('active');
            $("#profiles").addClass('active');
            $("#mktplace").removeClass('active');
        }
        else
        {
            this.search_profiles();
            $("#mkt_tab").parent().addClass('active');
            $("#profile_tab").parent().removeClass('active');


             $("#profiles").removeClass('active');
            $("#mktplace").addClass('active');
        }
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



$("#profile_tab").click(function(){
Search.tab = "profile";
Search.set_url();
show_connections_on_map();
});

$("#mkt_tab").click(function(){
Search.tab = "market";
Search.set_url();

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




$(".btn-pwant").click(function(){
    $(".btn-pwant").removeClass('active');
    that =  this;
    $(this).addClass('active');
})