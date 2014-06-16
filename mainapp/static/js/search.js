
var Search = {
    keyword :"",
    lng:"",
    lat:"",
    search_type:"food",
    filters:{food:{want:"all", location:"", usertype:"company", org:[], biz:[]},
    market:{want:"all", location:"", usertype:"company", org:[], biz:[]}},
    tab:"updates",
    load_state: function () {
        this.keyword = getParameterByName('q');
        this.lng = parseFloat(getParameterByName('lng'));
        this.lat = parseFloat(getParameterByName('lat'));
        this.search_type = getParameterByName('stype');



        this.filters.profile.location = getParameterByName('plocation');
        this.filters.profile.usertype = getParameterByName('put');
        this.filters.profile.org = getParameterByName('porg');
        this.filters.profile.biz = getParameterByName('pbiz');


        this.filters.market.want = getParameterByName('want');
        this.filters.market.location = getParameterByName('mlocation');
        this.filters.market.usertype = getParameterByName('mut');
        this.filters.market.org = getParameterByName('morg');
        this.filters.market.biz = getParameterByName('mbiz');
    }


    set_url:function(){
    	var query="/activity?";
    	var first_item = false;
    	if(this.keyword!="")
    	{

    		query += "q="+encodeURIComponent(this.keyword)+"&&";
    	}
    	if(this.stype!="")
    	{

    		query += "stype="+encodeURIComponent(this.search_type)+"&&";
    	}

    	if(this.filters.profile.location!="")
    	{
    		query += "plocation="+encodeURIComponent(this.filters.profile.location)+"&&";
    	}

    	if(this.filters.profile.usertype !="")
    	{
    		query += "put="+encodeURIComponent(this.filters.profile.usertype)+"&&";
    	}

    	if(this.filters.profile.org.length>0)
    	{
    		var porgs = this.filters.profile.org;
    		var porg = porgs[0];

    		for(var i = 1;i<progs.length;i++)
    		{
    			porg += ","+porgs[1]
    		}
    		porgs += "&&";
    		query += porgs;
    	}


    	window.history.pushState('Object', 'Title', '/activity'+query);

    }
}



function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

