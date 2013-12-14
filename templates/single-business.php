<?php include '_header.php';?>

    <div class="container">

    <?php include '_sidebar.php';?>

   

    <div class="col-md-10" id="single">


    <div id="header_box" class="row">
      <div class="col-md-2" id="avatar">

        <img class="img-thumbnail   center-block" src="http://a0.twimg.com/profile_images/2596092158/afpecvf41m8f0juql78p_bigger.png"  />

      </div>
     
      <div class="col-md-7">
         <h1><a href="#">Smales Farm</a></h1>

         <span class="label label-default">Mixed Farm</span>
         <span class="label label-default">Butcher</span>
         <span class="label label-default">Farm Shop</span>
     
         <div class="meta small text-muted">
            
            <i class="fa fa-map-marker"></i> <a href="http://maps.google.com/maps?saddr=current+location&daddr=Sydney+Opera+House,+Sydney+Opera+House,+Bennelong+Point,+Sydney+NSW+2000,+Australia" target="_blank" data-placement="top" data-toggle="tooltip" title="Get directions" class="text-muted">78 Example Street, Test Town</a>  
            
            <!-- if logged in or you've allows html5 browser location -->
            <i class="fa fa-location-arrow" style="margin-left: 20px;"></i> 87.2 miles  
            <!--  // if logged in or you've allows html5 browser location -->
 
            <i class="fa fa-star"></i> 
         </div> <!-- meta -->

         <hr />
         <p>Nullam quis risus eget urna mollis ornare vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam id dolor id nibh ultricies vehicula.</p>
         
         <hr />

          <div class="icons">
            <a href="#"><i class="fa fa-facebook-square"></i></a>
            <a href="#"><i class="fa fa-twitter-square"></i></a> 
            <a href="#"><i class="fa fa-phone-square"></i></a> 
            <a href="#"><i class="fa fa-rss-square"></i></a> 
            <a href="#"><i class="fa fa-envelope"></i></a> 
            <a href="#"><i class="fa fa-globe"></i></a> 
            <a href="#"><i class="fa fa-linkedin-square"></i></a> 
          </div> 
      </div>

      <div id="contact_info" class="col-md-3">

      <!-- if they dont't have an account yet -->
      <button class="btn btn-primary btn-block">Invite to connect</button>


      <!-- if they have an account --> 
      <div class="btn-group  btn-block ">
        <button type="button" class="btn btn-default btn-block dropdown-toggle" data-toggle="dropdown">
          <i class="fa fa-link"></i>
          Connect <span class="caret"></span>
        </button> 
        <ul class="dropdown-menu" role="menu">
          <li><a href="#" class="text-muted small">IF LOGGED IN = INDIVIDUAL</a></li>
          <li><a href="#"><i class="fa fa-shopping-cart text-muted pull-right"></i> I shop here</a></li>
          <li class="divider"></li>

          <li><a href="#" class="text-muted small">IF LOGGED IN = BUSINESS</a></li>
          <li><a href="#"><i class="fa fa-sign-in text-muted pull-right"></i> LOGGEDINNAME buys from them</a></li>
          <li><a href="#"><i class="fa fa-sign-out text-muted pull-right"></i> LOGGEDINNAME sells to them</a></li> 
      
          <li class="divider"></li>
          <li><a href="#"><i class="fa fa-envelope text-muted pull-right"></i> Contact</a></li>
          <li><a href="#"><i class="fa fa-facebook text-muted pull-right"></i>  Follow on twitter</a></li>
          <li><a href="#"><i class="fa fa-twitter text-muted pull-right"></i> Like on facebook</a></li>
        </ul>
      </div> <!-- /btn group --> 
   
      <!-- Button trigger modal -->
      <button class="btn btn-primary btn-block" data-toggle="modal" data-target="#myModal">
        Contact
      </button>  

      <!-- if not logged in show login prompt -->
      <button class="btn btn-primary btn-block">Login to see contact info</button>


         <!-- Modal -->
      <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
              <h4 class="modal-title" id="myModalLabel">Contact Smales Farm</h4>
            </div>
            <div class="modal-body">

            <div class="container-responsive">
              <div class="row">
                <div class="col-sm-4">
             
                  <address>
                    
          <a href="mailto:mail@smalesfarm.com" target="_blank"><i class="fa fa-envelope text-muted"></i> mail@smalesfarm.com </a><br />
          <a href="#"><i class="fa fa-twitter text-muted"></i> @smalesfarm</a><br />
          <a href="callto:0131 476 5333"><i class="fa fa-phone text-muted"></i> 0131 476 5333</a>
                  </address>
                </div>
                
                <div class="col-sm-8 contact-form">
                  <form id="contact" method="post" class="form" role="form">
                    <div class="row">
                      <div class="col-xs-6 col-md-6 form-group">
                        <input class="form-control" id="name" name="name" placeholder="Name (prefill if reg'd)" type="text" required autofocus />
                      </div>
                      <div class="col-xs-6 col-md-6 form-group">
                        <input class="form-control" id="email" name="email" placeholder="Email (prefill if reg'd)" type="email" required />
                      </div>
                    </div>
                    <textarea class="form-control" id="message" name="message" placeholder="Message" rows="5"></textarea>
                     
                     
                  </form>
                </div>
              </div>
            </div>
 
   

            </div>
            <div class="modal-footer"> 
              <button type="button" class="btn btn-primary">Tweet it</button>
              <button type="button" class="btn btn-primary">Email it</button>
            </div>
          </div><!-- /.modal-content -->
        </div><!-- /.modal-dialog -->
      </div><!-- /.modal -->

 
      </div>

    </div>

    <div class="row" style="margin-top: 50px;">
      <div class="col-md-12">
        <ul class="nav nav-tabs nav-justified">
          <li class="active"><a href="#">Home</a></li>
          <li><a href="#">Produce</a></li>
          <li><a href="#">Organisation</a></li>
          <li><a href="#">Customers</a></li>
          <li><a href="#">Activity</a></li>
          <li><a href="#">Reputation</a></li>
          <li><a href="#">Connections</a></li>
          <li><a href="#">People</a></li>
        </ul>
      </div> 
    </div>

    <ul>
    <li>Tags</li>
    <li>How many shop here</li>
    <li>Whats nearby</li>
    <li>Message</li>
    <li>Login to see details</li>
    <li>Add tags</li>
    <li>Add private notes</li>
    <li>Opentable</li>
    <li>Share</li>
    <li>Links (all, mebedly)</li>
    </ul>
  
  <div class="btn-toolbar">
    <div class="btn-group">
        <a href="#" class="btn btn-inverse disabled"><i class="fa-white fa-thumbs-up"></i></a>
        <a href="#" class="btn btn-inverse disabled"><i class="fa-white fa-heart"></i></a>
        <a href="#" class="btn btn-inverse disabled"><i class="fa-white fa-share-alt"></i></a>
    </div>
    <div class="btn-group">
        <a href="#" class="btn btn-inverse disabled"><i class="fa-white fa-trash"></i></a>
    </div>
  </div>

           <img src="http://maps.googleapis.com/maps/api/staticmap?zoom=15&size=320x240&maptype=roadmap&center=51.4583%2C-2.61156&sensor=false&client=gme-marktplaats&signature=AtzemkXpFWiPluPmUG_72gGAMxw=" width="100%">
 

        


    </div><!-- col10 --> 
 <?php include '_footer.php';?>