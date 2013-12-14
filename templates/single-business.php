<?php include '_header.php';?>

    <div class="container">

    <?php include '_sidebar.php';?>

   

    <div class="col-md-10" id="single">

    <div class="container-responsive">
    <div id="header_box" class="clearfix">
      <div class="col-md-2" id="avatar">
        <img class="img-thumbnail center-block" src="http://a0.twimg.com/profile_images/2596092158/afpecvf41m8f0juql78p_bigger.png"  />
      </div>
     
      <div class="col-md-7">
         <h1><a href="#">Smales Farm</a></h1>
 
         <span class="label label-default">Livestock Farm</span>
         <span class="label label-default">Butcher</span>
         <span class="label label-default">Wholesaler</span>
         <span class="label label-default">Distribution</span>
         <span class="label label-default">Farm Shop</span>
 

         <hr />
         <p>Nullam quis risus eget urna mollis ornare vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam id dolor id nibh ultricies vehicula.</p>        

          <div class="tags">  
           <a href="/tag/TAG">Box Scheme</a>
           <a href="/tag/TAG">Butcher</a>
           <a href="/tag/TAG">family</a>
           <a href="/tag/TAG">organic</a> 
          </div>
         <hr /> 
     
         <div class="meta small text-muted">
            
            <i class="fa fa-map-marker"></i> <a href="http://maps.google.com/maps?saddr=current+location&daddr=Sydney+Opera+House,+Sydney+Opera+House,+Bennelong+Point,+Sydney+NSW+2000,+Australia" target="_blank" data-placement="top" data-toggle="tooltip" title="Get directions" class="text-muted">78 Example Street, Test Town</a>  
            
            <!-- if logged in or you've allows html5 browser location -->
            <i class="fa fa-location-arrow" style="margin-left: 20px;"></i> 87.2 miles  
            <!--  // if logged in or you've allows html5 browser location -->
  
         </div> <!-- meta -->
  
      </div><!-- end header middle -->

      <div id="contact_info" class="col-md-3">

      <!-- if they dont't have an account yet -->
      <button class="btn btn-primary btn-block">Invite to connect</button>


      <!-- if logged in users = individual -->
      <button class="btn btn-default btn-block"><i class="fa fa-shopping-cart text-muted"></i> I am a customer</button>


      <!-- if they have an account --> 
      <div class="btn-group  btn-block ">
        <button type="button" class="btn btn-default btn-block dropdown-toggle" data-toggle="dropdown">
          <i class="fa fa-link text-muted"></i>
          We trade with them <span class="caret"></span>
        </button> 
        <ul class="dropdown-menu" role="menu">  
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

 

      <button class="btn btn-default btn-block" data-toggle="modal" data-target="#sharer">
        <i class="fa fa-share-square-o text-muted"></i> Share
      </button>

      <!-- Modal -->
      <div class="modal fade" id="sharer" tabindex="-1" role="dialog" aria-labelledby="sharer" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-body"> 

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
                    <textarea class="form-control counted" name="message" placeholder="Type in your message" rows="5"></textarea>
                    <h6 class="pull-right" id="counter">320 characters remaining</h6>
                     
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

 
      </div><!-- end header last -->

    </div>
    </div>


    <div class="row" style="margin-top: -1px;">
     <div class="col-md-12">
        <ul class="nav nav-tabs nav-justified">

          <li class="active"><a href="#home" data-toggle="tab">Home</a></li>
          <li><a href="#produce" data-toggle="tab">Produce</a></li>
          <li><a href="#organisations" data-toggle="tab">Organisation</a></li>
          <li><a href="#customers" data-toggle="tab">Customers</a></li>
          <li><a href="#activity" data-toggle="tab">Activity</a></li> 
          <li><a href="#connections" data-toggle="tab">Connections</a></li>
          <li><a href="#people" data-toggle="tab">People</a></li>
        </ul>
     </div>
    </div>

    <div class="row">
      <div class="col-md-8">
        
        <div class="container-responsive clearfix">

        <div class="tab-content hidden">
          <div class="tab-pane active fade in " id="home">.ADD FSA..</div>
          <div class="tab-pane fade" id="produce">.d..</div>
          <div class="tab-pane fade" id="organisations">.d.d.</div>
          <div class="tab-pane fade" id="customers">.d.dg.</div>
        </div>


  


 We sell the following produce
MEAT
Beef Chicken Lamb Pork
EGGS

          <div class="clearfix">  
          <h2>Tags </h2>
           <a href="/tag/TAG">Box Scheme</a>
           <a href="/tag/TAG">Butcher</a>
           <a href="/tag/TAG">family</a>
           <a href="/tag/TAG">organic</a> 
          </div>


          <div class="clearfix">  
          <h2>Organisations </h2>
          
          <?php include 'card_organisation.php';?> 
          <?php include 'card_organisation.php';?> 
          <?php include 'card_organisation.php';?> 
          <?php include 'card_organisation.php';?> 
          <?php include 'card_organisation.php';?> 
          <?php include 'card_organisation.php';?> 
          <?php include 'card_organisation.php';?> 
          </div>

          <div class="clearfix">
          <h2>Customers</h2>
          <?php include 'card_individual.php';?> 
          <?php include 'card_individual.php';?> 
          <?php include 'card_individual.php';?> 
          <?php include 'card_individual.php';?> 
          <?php include 'card_individual.php';?> 
          <?php include 'card_individual.php';?>  
          </div> 

          <div class="clearfix">
          <h2>Businesses</h2>
          <?php include 'card_business.php';?> 
          <?php include 'card_business.php';?> 
          <?php include 'card_business.php';?> 
          <?php include 'card_business.php';?> 
          <?php include 'card_business.php';?> 
          </div>
     
        </div><!-- container responsive -->
  
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

        <a class="twitter-timeline" href="https://twitter.com/foodtradeHQ" data-widget-id="411852499260145664">Tweets by @foodtradeHQ</a>
        <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>


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
 
   
      </div><!-- end col8 --> 


      <div class="col-md-4">
        Map showing customers as clusters / dots, and trade connections as lines
        <img src="map.png" style="width: 100%;" />


      </div><!-- end col4 -->

    </div><!-- row -->

   


        


    </div><!-- col10 --> 
 <?php include '_footer.php';?>