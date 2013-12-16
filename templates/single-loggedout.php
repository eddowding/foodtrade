<?php include '_header.php';?>

    <div  class="container">
 

    <div class="col-md-12" id="single">

    <div class="container-responsive">
    <div id="header_box" class="clearfix">
      <div class="col-md-2" id="avatar">
        <img class="img-thumbnail center-block" src="http://a0.twimg.com/profile_images/2596092158/afpecvf41m8f0juql78p_bigger.png"  />
      </div>
     
      <div class="col-md-7">
         <h1><a href="#">Smales Farm</a></h1>
 
          <div class="tags tags-biztype  ">  
           <a href="/type/livestock-farm">Bakery</a>
           <a href="/type/buther">Wholesale</a>  
           <a href="/type/buther">Distribution</a>  
           <a href="/type/buther">Livestock Farm</a>  
          </div> 

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
            
             
         </div> <!-- meta -->
  
      </div><!-- end header middle -->

      <div id="contact_info" class="col-md-3">

      <!-- if they dont't have an account yet -->
      <button class="btn btn-info btn-block">Sign in</button>


      

      <!-- Button trigger modal -->
      <button class="btn btn-default btn-block" disabled="disabled" data-toggle="modal" data-target="#modal_contact">
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


    <div class="row">
     <div class="col-md-12">
        <ul class="nav nav-tabs nav-justified">
          <li class="active"><a href="#produce" data-toggle="tab">Foods <span class="badge">42</span></a></li>
          <li><a href="#connections" data-toggle="tab">Connections <span class="badge">28</span></a> </li>
          <li><a href="#organisations" data-toggle="tab">Organisation</a> <span class="badge"></span></li>
          <li><a href="#customers" data-toggle="tab">Customers <span class="badge">4</span></a> </li>
          <li><a href="#activity" data-toggle="tab">Updates  <span class="badge">5</span></a></li> 
          <li><a href="#team" data-toggle="tab">Team <span class="badge">2</span></a></li>
        </ul>
     </div>
    </div>

    <div class="row">
      <div class="col-md-8">
        <div class="container-responsive clearfix">

      

   

<div class="container-responsive">
  <div class="row"> 
    <div class="col-md-12">
      <form action="#" method="get">
          <div class="input-group well well-sm">

              <input class="form-control" id="system-search" name="q" placeholder="Search their foods..." required>
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
                  <div class="pull-right">

                   <!-- hide if user has edit rights -->
                   <a href="#"><i class="fa fa-thumbs-o-up text-muted" title="Vouch for this"></i></a> 

                   <!-- if user has edit rights -->
                   <a href="#"><i class="fa fa-trash-o text-muted" title="Delete"></i></a> 
                   </div>
                  </td>  
              </tr> 
              <tr>
                  <td>Meat / <a href="/produce/beef">Chicken</a></td> 
                  
                  <td> 
                  <div class="pull-right">

                   <!-- hide if user has edit rights -->
                   <a href="#"><i class="fa fa-thumbs-o-up text-muted" title="Vouch for this"></i></a> 

                   <!-- if user has edit rights -->
                   <a href="#"><i class="fa fa-trash-o text-muted" title="Delete"></i></a> 
                   </div>
                  </td>  
              </tr>
              <tr>
                  <td>Fruit / <a href="/produce/beef">Blackberries</a></td> 
                  
                  <td> 
                  <div class="pull-right">

                   <!-- hide if user has edit rights -->
                   <a href="#"><i class="fa fa-thumbs-o-up text-muted" title="Vouch for this"></i></a> 

                   <!-- if user has edit rights -->
                   <a href="#"><i class="fa fa-trash-o text-muted" title="Delete"></i></a> 
                   </div>
                  </td>  
              </tr> 
          </tbody>
          <tfoot style="background: #eee;">
              <tr>
                  <td colspan="2">

                  <form action="#" method="get">
                      <div class="input-group">
                      <!-- link this to open food facts --> 
                            <input class="form-control" name="q" style="width:400px;" placeholder="Add foods you can buy here.">
                            <span class="input-group-btn">
                                <button type="submit" class="btn btn-success"> Add</button>
                            </span>
                          </div>
                      </div>
                  </form>
              </td> 
                  
              </tr> 
          </tfoot>
      </table>    

    </div>
  </div>
</div>


          <div class="clearfix">
          <h2>Connections</h2>
            
            <p>You must 
              <a class="btn btn-info" href="#">
                sign in 
              </a> 
              to see the connections. It's free, don't worry.</p>

          </div>
 

          <div class="clearfix">  
          <h2>Organisations</h2>

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
          <h2>Team</h2> 
            <p>You must 
              <a class="btn btn-info" href="#">
                sign in 
              </a> 
              to see the who works here. It's free, don't worry.</p>
          </div> 

     
        <h2>Updates</h2>


           <?php include 'card_activity.php';?> 
 
 
 
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