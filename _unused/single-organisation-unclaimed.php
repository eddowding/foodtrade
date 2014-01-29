<?php include '_header.php';?>

    <div  class="container">

    <?php include '_sidebar_search.php';?>

   

    <div class="col-md-10" id="single">

    <div class="container-responsive">
    <div id="header_box" class="clearfix">
      <div class="col-md-2" id="avatar">
        <img class="img-thumbnail center-block" src="https://pbs.twimg.com/profile_images/1690823879/Screen_shot_2011-12-13_at_12.21.20_bigger.png"  />
      </div>
     
      <div class="col-md-7">
         <h1><a href="#">Slow Food UK</a></h1>
  
         <hr />
         <p>Making GOOD, CLEAN and FAIR food happen. Join us!</p>        

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

     <button class="btn btn-default btn-block" data-toggle="modal" data-target="#modal_customer">
        <i class="fa fa-smile-o text-muted"></i> I'm a member
      </button> 
      <!-- if selected -->
     <button class="btn btn-success btn-block" data-toggle="modal" data-target="#modal_customer">
        <i class="fa fa-check "></i> I'm a member
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

      <p class="text-center text-muted small" style="margin-top: 20px;">Is this your business? Sign in!</p>


     <!-- modal_contact -->
      <div class="modal fade" id="modal_contact" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
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

      <!-- modal_customer -->
      <div class="modal fade" id="modal_customer" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
              <h4 class="modal-title" id="myModalLabel">You're a customer of Smales Farm?</h4>
            </div>
            <div class="modal-body">
 
            <p><strong>Thanks!</strong> Knowing where customers are is a win-win. BUSINESS NAME understands how it can better serve you, and in time we'll help them keep you informed about special local offers. </p> 
            <p>Examples might include home deliveries from your local shops, later opening hours, or working together with other local business to make things better. </p>
            <p>We'll show you as being a customer and put a small dot on the map near your location.</p>
   

            </div>
            <div class="modal-footer"> 
              <button type="button" class="btn btn-default">Cancel</button>
              <button type="button" class="btn btn-primary">Yes, I'm a happy customer!</button>
            </div>
          </div><!-- /.modal-content -->
        </div><!-- /.modal-dialog -->
      </div><!-- /.modal -->


 
      </div><!-- end header last -->

    </div>
    </div>


    <div class="row" >
     <div class="col-md-12">
        <ul class="nav nav-tabs ">
          <li class="active"><a href="#members" data-toggle="tab">Members <span class="badge ">2457</span></a></li>
          <li><a href="#foods" data-toggle="tab">Foods  <span class="badge">54556</span></a></li> 
          <li><a href="#team" data-toggle="tab">Team <span class="badge ">25</span></a></li> 
        </ul>
     </div>
    </div>

    <div class="row">
      <div class="col-md-8">
        <div class="container-responsive clearfix">

        <div class="tab-content">
          <div class="tab-pane active fade in " id="members">
            <div class="clearfix"> 
              <?php include 'card_business.php';?> 
              <?php include 'card_business.php';?> 
              <?php include 'card_business.php';?> 
              <?php include 'card_business.php';?> 
              <?php include 'card_business.php';?> 
              <?php include 'card_business.php';?> 
              <?php include 'card_business.php';?> 
              <?php include 'card_business.php';?> 
              <?php include 'card_business.php';?> 
              <?php include 'card_business.php';?> 
              <?php include 'card_business.php';?> 
              <?php include 'card_business.php';?> 
              <?php include 'card_business.php';?> 
              <?php include 'card_business.php';?> 
              <?php include 'card_business.php';?> 
            </div>
          </div>
          <div class="tab-pane fade" id="foods">
            <div class="container-responsive">
              <div class="row"> 
                <div class="col-md-12">
                  <form action="#" method="get">
                      <div class="input-group well well-sm">

                          <input class="form-control" id="system-search" name="q" placeholder="Search foods from Slow Food UK members..." required>
                          <span class="input-group-btn">
                              <button type="submit" class="btn btn-default"><i class="glyphicon glyphicon-search"></i></button>
                          </span>
                      </div>
                  </form>
                   <table class="table table-list-search">
                      <tbody>
                          <tr>
                              <td>Meat / <a href="/produce/beef">Beef</a></td>  
                              <td> 
                               <a href="#" class="pull-right"><i class="fa fa-thumbs-o-up text-muted" title="Vouch for this"></i></a> 
                              </td> 
                          </tr> 
                          <tr>
                              <td>Meat / <a href="/produce/beef">Chicken</a></td> 
                              
                              <td> 
                               <a href="#" class="pull-right"><i class="fa fa-thumbs-o-up text-muted" title="Vouch for this"></i></a> 
                              </td>  
                          </tr>
                      </tbody>
                      <tfoot>
                          <tr>
                              <td>Fruit / <a href="/produce/beef">Blackberries</a></td> 
                              <td> 
                               <a href="#" class="pull-right"><i class="fa fa-thumbs-o-up text-muted" title="Vouch for this"></i></a> 
                              </td> 
                          </tr> 
                      </tfoot>
                  </table>   
                </div>
              </div>
            </div>
          </div>
          

          <div class="tab-pane fade" id="team">

           <button class="btn btn-default">
              <i class="fa fa-smile-o "></i> I work here
            </button> 
            <div class="clearfix">
              <?php include 'card_team.php';?> 
              <?php include 'card_team.php';?> 
              <?php include 'card_team.php';?> 
              <?php include 'card_team.php';?> 
              <?php include 'card_team.php';?>  
            </div> 
          </div>

           


     

        
      </div>
 
 
        </div><!-- container responsive -->
  
      
 
   
      </div><!-- end col8 --> 


      <div class="col-md-4">
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