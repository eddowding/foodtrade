<?php include '_header.php';?>

    <div id="activity_single" class="container">

    <?php include '_sidebar.php';?>

   

    <div class="col-md-10" id="single">

    <div class="container-responsive">
    <div id="header_box" class="clearfix">


      <div class="col-md-2" id="avatar">
        <img class="img-thumbnail center-block" src="http://a0.twimg.com/profile_images/2596092158/afpecvf41m8f0juql78p_bigger.png"  />
      </div>
     
      <div class="col-md-7">

         <p style="font-size: 20px; font-weight: 200; padding-top: 20px;">
          Nullam quis risus eget urna mollis ornare vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam id dolor id nibh ultricies vehicula.</p>        

 <hr />

         <h1><a href="#">Smales Farm</a></h1>

        
          <div class="tags tags-biztype  ">  
           <a href="/type/livestock-farm">Bakery</a>
           <a href="/type/buther">Wholesale</a>  
           <a href="/type/buther">Distribution</a>  
           <a href="/type/buther">Livestock Farm</a>  
          </div> 
   
     
         <div class="meta small text-muted">
            
            <i class="fa fa-map-marker"></i> 78 Example Street, Test Town  
            
            <!-- if logged in or you've allows html5 browser location -->
            <a href="http://maps.google.com/maps?saddr=current+location&daddr=Sydney+Opera+House,+Sydney+Opera+House,+Bennelong+Point,+Sydney+NSW+2000,+Australia" target="_blank" data-placement="top" data-toggle="tooltip" title="Get directions" class="text-muted">
            <i class="fa fa-location-arrow" style="margin-left: 20px;"></i> 87.2 miles</a>  
            <!--  // if logged in or you've allows html5 browser location -->
  
         </div> <!-- meta -->
  
      </div><!-- end header middle -->

      <div id="contact_info" class="col-md-3">
 
      <!-- if logged in users = individual --> 
      <button class="btn btn-default btn-block" data-toggle="modal" data-target="#modal_customer">
        <i class="fa fa-smile-o text-muted"></i> I am a customer
      </button> 

      <!-- if logged in users = business --> 
      <div class="btn-group btn-block" data-toggle="buttons">
        <label class="btn btn-default" style="width:50%;" title="LOGGEDINUSER buys from PROFILENAME">
          <input type="checkbox"> Buy from
        </label>
        <!-- showing active mode if button is selected -->
        <label class="btn btn-success" style="width:50%;" title="LOGGEDINUSER sells to PROFILENAME">
          <input type="checkbox"> Sell to
        </label> 
      </div>
 

      <!-- Button trigger modal -->
      <button class="btn btn-primary btn-block" data-toggle="modal" data-target="#modal_contact">
        Contact
      </button>   
 

      <button class="btn btn-default btn-block" data-toggle="modal" data-target="#sharer">
        <i class="fa fa-share-square-o text-muted"></i> Share
      </button>

      <!--SHARER  Modal -->
      <div class="modal fade" id="sharer" tabindex="-1" role="dialog" aria-labelledby="sharer" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-body"> 



        <div class="container-responsive">
          <div class="row">
            <div class="col-sm-6">

              <a href="#" class="btn btn-block  btn-social btn-facebook" onclick="window.open(
                    'https://www.facebook.com/sharer/sharer.php?u='+encodeURIComponent('URL') +'&amp;t=' + encodeURIComponent('TITLE'), 
                    'facebook-share-dialog', 
                    'width=626,height=436,top='+((screen.height - 436) / 2)+',left='+((screen.width - 626)/2 )); 
                  return false;">
                <i class="fa fa-facebook"></i>  Share on Facebook
              </a>

              <a href="#" class="btn btn-block  btn-social btn-twitter" onclick="window.open(
                    'https://twitter.com/share?url='+encodeURIComponent('URL')+'&amp;text='+encodeURIComponent('@THEIRNAME on @foodtradeHQ') + '&amp;count=none/', 
                    'twitter-share-dialog', 
                    'width=626,height=436,top='+((screen.height - 436) / 2)+',left='+((screen.width - 626)/2 )); 
                  return false;">
                <i class="fa fa-twitter"></i>  Share on Twitter
              </a>
  
              <a class="btn  btn-block  btn-social btn-pinterest" href="http://pinterest.com/pin/create/button/?url={URI-encoded URL of the page to pin}&media={URI-encoded URL of the image to pin}&description={optional URI-encoded description}" class="pin-it-button" count-layout="horizontal">
                <i class="fa fa-pinterest"></i>
                Share on Pinterest
              </a>
            </div>
            <div class="col-sm-6">
              <a  class="btn btn-social btn-block btn-google-plus" href="https://plus.google.com/share?url=myline">
                <i class="fa fa-google-plus"></i>
                Share on Google+
              </a>

              <a  class="btn btn-block btn-social btn-tumblr" href="http://www.tumblr.com/share" title="Share on Tumblr">
                <i class="fa fa-tumblr"></i>
                Share on Tumblr
              </a>
                 
              <a  class="btn btn-block  btn-social btn-bitbucket" href="http://www.linkedin.com/shareArticle?mini=true&url=THEURL&title=TITLE&summary=SUMMARY&source=">
                <i class="fa fa-linkedin"></i>
                Share on LinkedIn
              </a>
            </div>
            </div>
            </div>
              <script type="text/javascript" src="http://platform.tumblr.com/v1/share.js"></script>

            </div> 
          </div><!-- /.modal-content -->
        </div><!-- /.modal-dialog -->
      </div><!-- /.modal -->

      <div class="icons text-center" style="font-size:25px">
        <a href="#"><i class="fa fa-facebook-square"></i></a>
        <a href="#"><i class="fa fa-twitter-square"></i></a> 
        <a href="#"><i class="fa fa-phone-square"></i></a> 
        <a href="#"><i class="fa fa-rss-square"></i></a> 
        <a href="#"><i class="fa fa-envelope"></i></a> 
        <a href="#"><i class="fa fa-globe"></i></a> 
        <a href="#"><i class="fa fa-youtube"></i></a> 
        <a href="#"><i class="fa fa-linkedin-square"></i></a> 
      </div> 


      


 
      </div><!-- end header last -->

    </div>
    </div> 

    <div class="row" style="margin-top: 30px;">
      <div class="col-md-6">
        <div class="container-responsive clearfix">
          <div id="activity"> 
           <?php include 'card_activity.php';?>  
          </div> 
         </div>
      </div><!-- end col8 --> 


      <div class="col-md-6">
        <img src="map.png" style="width: 100%;" />

        <div class="alert alert-warning">
          <p>This map shows 
          Customers as points
          Stockist as organge lines and 
          Supplieras as purple lines</p>

          <p>There are radius lines at 15, 30, and 100 miles.</p>
        </div>


      </div><!-- end col4 -->

    </div><!-- row -->

   


        


    </div><!-- col10 --> 

   
 <?php include '_footer.php';?>