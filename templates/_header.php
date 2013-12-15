<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="shortcut icon" href="http://foodtrade.com/wp-content/uploads/2013/09/favi22.png">

    <title>FoodTrade</title>

    <!-- CSS -->
    <link href="css/bootstrap.css" rel="stylesheet">
    <link href="css/foodtrade.css" rel="stylesheet">
    <link href="//netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.css" rel="stylesheet">
 

    <!-- Custom styles for this template -->
    <link href="http://getbootstrap.com/examples/navbar-fixed-top/navbar-fixed-top.css" rel="stylesheet">
 
    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <!-- Fixed navbar -->
    <div class="navbar navbar-default navbar-fixed-top" role="navigation">
      <div class="ftstrip"></div>
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">FoodTrade</a>
        </div>
        <div class="navbar-collapse collapse">
          
          <form class="navbar-form navbar-left nav-justified" role="search">
            <div class="form-group" style="margin-right:5px;">
              <input type="text" class="form-control" placeholder="What?"> 
            </div>
            <div class="form-group" style="margin-right:5px;">
              <input type="text" class="form-control" placeholder="Where?">
            </div>
            <button type="submit" class="btn btn-default"><i class="fa fa-search"></i></button>

          </form>

        
          <button type="button" class="btn btn-primary navbar-btn pull-right" style="margin-left: 20px;"  data-toggle="modal" data-target="#newpost">
            <i class="fa fa-edit"></i>
          </button>
  
          <!-- New post Modal -->
          <div class="modal fade" id="newpost" tabindex="-1" role="dialog" aria-labelledby="newpost" aria-hidden="true">
            <div class="modal-dialog">
              <div class="modal-content"> 
                <div class="modal-body">               
                  <form accept-charset="UTF-8" action="" method="POST">
                      <textarea class="form-control counted" name="message" placeholder="Type in your message" rows="5" ></textarea>
                  </form> 
                </div>
                <div class="modal-footer">
                  <h6 class="pull-left" id="counter">320 characters remaining</h6> 
                  <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                  <button type="button" class="btn btn-primary">Post update</button>
                </div>
              </div><!-- /.modal-content -->
            </div><!-- /.modal-dialog -->
          </div><!-- /.modal -->


         <ul class="nav navbar-nav navbar-center">
          <li><a href="/">Activity</a></li>
          <li><a href="/">Pricing</a></li>
          <li><a href="/">About us</a></li>
         </ul>
 

         <ul class="nav navbar-nav navbar-right">
                  <li><a href="register.php">Sign Up</a></li>
                  <li><a href="#" data-toggle="modal" data-target="#modal_login">Sign In</a></li>
               </ul>
 
        </div><!--/.nav-collapse -->
      </div>
    <div class="ftstrip ftstrip-mini"></div>
    </div>

      <?php include 'modal_login.php';?>


   