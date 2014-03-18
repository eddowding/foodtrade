<?php include '_header.php';?>

    <div  class="container">

    <?php include '_sidebar_search.php';?>

   

    <div class="col-md-10" id="single">

    <div class="container-responsive">
    <div id="header_box" class="clearfix">
      <div class="col-md-2 cell" id="avatar">
        <img class="img-thumbnail center-block" src="https://pbs.twimg.com/profile_images/1690823879/Screen_shot_2011-12-13_at_12.21.20_bigger.png"  />
      </div>
     
      <div class="col-md-7 cell" >
         <h1><a href="#">Slow Food UK</a></h1>

         <hr />
         <p>Making GOOD, CLEAN and FAIR food happen. Join us!</p>        
 
         <hr /> 
     
         <div class="meta small text-muted">
            
            <i class="fa fa-map-marker"></i> <a href="http://maps.google.com/maps?saddr=current+location&daddr=Sydney+Opera+House,+Sydney+Opera+House,+Bennelong+Point,+Sydney+NSW+2000,+Australia" target="_blank" data-placement="top" data-toggle="tooltip" title="Get directions" class="text-muted">Notting Hill, London</a>  
            
            <!-- if logged in or you've allows html5 browser location -->
            <i class="fa fa-location-arrow" style="margin-left: 20px;"></i> 87.2 miles  
            <!--  // if logged in or you've allows html5 browser location -->
  
         </div> <!-- meta -->
  
      </div><!-- end header middle -->

      <div id="contact_info" class="col-md-3 cell">

      <!-- if they dont't have an account yet --> 
      <button class="btn btn-primary btn-block" style="margin-top:40px;" data-toggle="modal" data-target="#modal_invite">
         Invite to connect
      </button> 
      <?php include 'modal_invite.php';?>

  
      </div><!-- end header last -->

    </div>
    </div>

    <div class="row" style="margin-top: 30px;">
     <div class="col-md-12">

<div class="well well-sm">
  <h3 class="text-center"> Hi! What is @SlowFoodUK? </h3>

<div class="container">
    <div class="row">
      <ul class="thumbnails list-unstyled">
        <li class="col-md-3">
          <div class="thumbnail" style="padding: 0">  
            <div class="modal-header text-center">
              <button type="button" class="btn btn-lg btn-primary">Food business</button>
            </div>
            <div class="caption"> 
              <p><span class="help-block">Eg. Farms, restaurants, caterers, bakers, schools, hospitals...</span></p>
              <p>Any business or organisation which buys an sells food for a living. From farm to fork, small holder to supermarket.</p>
              
            </div> 
          </div>
        </li>

        <li class="col-md-3">
          <div class="thumbnail" style="padding: 0">  
            <div class="modal-header text-center">
              <button type="button" class="btn btn-lg btn-primary">Organisation</button>
            </div>
            <div class="caption"> 
              <p><span class="help-block">Eg. Soil Assocation, Slow Food, LEAF, The SRA, Catering Mark...</span></p>
              <p>Any membership group with an a strong interest in food, agriculture, or nutrition.</p>
              
            </div> 
          </div>
        </li>

        <li class="col-md-3">
          <div class="thumbnail" style="padding: 0">  
            <div class="modal-header text-center">
              <button type="button" class="btn btn-lg btn-primary">Individual</button>
            </div>
            <div class="caption"> 
              <p><span class="help-block">Eg. most of us: customers, chefs, bloggers, consultants... </span></p>
              <p>Did you know that the food system employs just over 400,000 workers in the UK?</p>
              
            </div> 
          </div>
        </li>  
      </ul>
    </div>
</div>
 
  <h4 class="text-center"> <small> <strong>This only shows once!</strong> As soon as we know what it is, others can start adding information to it. </small></h4> 
</div>
 
     </div>
    </div>

     
        
        


    </div><!-- col10 --> 

   
 <?php include '_footer.php';?>