<?php include '_header.php';?>

    <div class="container">

    <div class="col-md-2 sidebar" >

        <!-- show the logged in users account --> 
        <div id="account_info">
        
        <div class="clearfix" style="margin-bottom: 10px;">
          <!-- twitter 78px image - 'large' -->
          <!--https://dev.twitter.com/docs/user-profile-images-and-banners -->
          <img class="pull-left img-rounded" style="margin:0 8px 0 0; width:30px"  src="http://a0.twimg.com/profile_images/2596092158/afpecvf41m8f0juql78p_normal.png"  />

          <div class="content">
            <h4 style="margin:0;">Sujit Maharjan</h4>
            <small><a href="#" class="text-muted">Edit your profile</a></small>
          </div>
        </div>
         
        <p><a href="#">Trade connections <span class="badge pull-right">42</span></a></p>
        <p><a href="#">Foods <span class="badge pull-right">35</span></a></p>
        <p><a href="#">Organisations <span class="badge pull-right">4</span></a></p>
        <p><a href="#">Awards <span class="badge pull-right">42</span></a></p>
        
          
          <!-- PUT EMPTY ONES AT THE BOTTOM OF THE LIST -->
          <!-- if ZERO ON ANY OF THESE -->
        
        <div class="alert alert-info small"> 
          <p><b>Want a great profile?</b></p> 
         
            <a href="#">Add Awards</a>
            <br />
            <a href="#">Add Organisations</a>
        </div>
         
        </div><!-- /account_info -->
 
 
    <hr /> 

      <h4>Who's nearby</h4>
 

        <p><a href="#">Individuals <span class="badge pull-right">273</span></a></p>
        <p><a href="#">Businesses <span class="badge pull-right">38</span></a></p> 

     <!--    <div class="clearfix"> 
          <img class="pull-left img-rounded" style="margin:0 8px 0 0; width:30px"  src="https://pbs.twimg.com/profile_images/378800000006142190/2892beb0a4ee730cb98173e5d8660816_normal.jpeg" />
          <div class="content">
            <h6 style="margin:0;">Marriott Hotels</h6>
            <button type="button" class="btn btn-default btn-xs">Connect</button>
          </div>
        </div>
<hr />
        <div class="clearfix"> 
          <img class="pull-left img-rounded" style="margin:0 8px 0 0; width:30px"  src="https://pbs.twimg.com/profile_images/1241297538/C-square_normal.gif" />
          <div class="content">
            <h5 style="">City Chef</h5>
            <button type="button" class="btn btn-default btn-xs">Connect</button>
          </div>
        </div>
 -->
    
    <div class="foodtrade-sidebar">

    <hr />

    <div class="alert alert-success">If a search term is set, then show the filters below, and remove everything above up until "Edit your profile"</div>
    <hr>
     
    <!-- consider using this for search filter http://harvesthq.github.io/chosen/ -->
    <form role="form">
      <div class="form-group"> 
        <input type="email" class="form-control" id="filter_organisation" placeholder="Filter by food">
      </div>
    </form>


    <ul class="foodtrade-tag-list">
    <li data-id="ALL" class="foodtrade-tag foodtrade-tag-click foodtrade-tag-all"><div class="foodtrade-tag-checkbox-column"><input type="checkbox" checked="checked" aria-label="All Partners" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">All Foods</div><div class="foodtrade-tag-count">51</div></li><li data-id="8" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="Johns Hopkins " class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Bread </div><div class="foodtrade-tag-count">6</div></li><li data-id="1" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="Stanford University" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Cheese</div><div class="foodtrade-tag-count">5</div></li><li data-id="16" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="École Polytechnique Fédérale de Lausanne" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Vegetables </div><div class="foodtrade-tag-count">4</div></li><li data-id="4" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="Princeton University" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Ham</div><div class="foodtrade-tag-count">3</div></li><li data-id="15" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="University of Washington" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text"> Milk</div><div class="foodtrade-tag-count">3</div></li><li class="foodtrade-tag-showmore">show more</li>
    </ul>

     <hr>
 
    <!-- consider using this for search filter http://harvesthq.github.io/chosen/ -->
    <form role="form">
      <div class="form-group"> 
        <input type="email" class="form-control" id="filter_organisation" placeholder="Filter Business Type">
      </div>
    </form>


    <ul class="foodtrade-tag-list">
    <li data-id="ALL" class="foodtrade-tag foodtrade-tag-click foodtrade-tag-all"><div class="foodtrade-tag-checkbox-column"><input type="checkbox" checked="checked" aria-label="All Partners" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">All Businesses</div><div class="foodtrade-tag-count">51</div></li><li data-id="8" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="Johns Hopkins " class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Wholesaler </div><div class="foodtrade-tag-count">6</div></li><li data-id="1" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="Stanford University" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Farmer</div><div class="foodtrade-tag-count">5</div></li><li data-id="16" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="École Polytechnique Fédérale de Lausanne" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Caterer </div><div class="foodtrade-tag-count">4</div></li><li data-id="4" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="Princeton University" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">University</div><div class="foodtrade-tag-count">3</div></li><li data-id="15" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="University of Washington" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Abbatoir</div><div class="foodtrade-tag-count">3</div></li><li class="foodtrade-tag-showmore">show more</li>
    </ul>

    <hr />
     
    <!-- consider using this for search filter http://harvesthq.github.io/chosen/ -->
    <form role="form">
      <div class="form-group"> 
        <input type="email" class="form-control" id="filter_organisation" placeholder="Filter organisation">
      </div>
    </form>


    <ul class="foodtrade-tag-list">
    <li data-id="ALL" class="foodtrade-tag foodtrade-tag-click foodtrade-tag-all"><div class="foodtrade-tag-checkbox-column"><input type="checkbox" checked="checked" aria-label="All Partners" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">All Organisations</div><div class="foodtrade-tag-count">51</div></li><li data-id="8" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="Johns Hopkins " class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Soil Association </div><div class="foodtrade-tag-count">6</div></li><li data-id="1" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="Stanford University" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">NFU</div><div class="foodtrade-tag-count">5</div></li><li data-id="16" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="École Polytechnique Fédérale de Lausanne" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Plunkett Foundation </div><div class="foodtrade-tag-count">4</div></li><li data-id="4" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="Princeton University" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Organic institute</div><div class="foodtrade-tag-count">3</div></li><li data-id="15" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="University of Washington" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text"> Slow Food</div><div class="foodtrade-tag-count">3</div></li><li class="foodtrade-tag-showmore">show more</li>
    </ul>

    </div>
    </div>

    <div class="col-md-5">
 
 
 

  <div id="update" class="well well-sm">
    <form action="#" method="get">
        <div class="input-group"> 
          <input class="form-control" name="q"  placeholder="What #food do you have to #buy, #sell, or #surplus?">
          <span class="input-group-btn">
              <button type="submit" class="btn btn-success"> Post</button>
          </span>
        </div>
    </form>
    <div class="help-block small">
    <ul>
    <li>300kg #surplus conference #pears for #sale or #surplus</li>
    <li>I want to  #buy organic #honey for my farm shop.</li>
    </ul>
    </div>
  </div> 

 
  <div id="activity"> 
         <?php include 'card_activity.php';?>  
  </div>



     
    </div><!-- closes 5 -->

    <div class="col-md-5">

    <!-- FIX THE MAP POSITION SO IT DOES NOT SCROLL --> 
      <div style="width:100%; height: 1000px; "  data-spy="affix" data-offset-top="30">
        
        <img src="map.png" style="width: 100%;" />

        <div class="alert alert-warning">
          <p>This map shows 
          Customers as points
          Stockist as organge lines and 
          Supplieras as purple lines</p>

          <p>There are radius lines at 15, 30, and 100 miles.</p>
        </div>

      </div>
    </div>

    </div>


 <?php include '_footer.php';?>
