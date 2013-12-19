<?php include '_header.php';?>

    <div class="container">
 


    <?php include '_sidebar_search.php';?>
 
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
