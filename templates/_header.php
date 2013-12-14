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

        
          <button type="button" class="btn btn-primary navbar-btn pull-right" style="margin-left: 20px;"><i class="fa fa-edit"></i></button>
 
         <ul class="nav navbar-nav navbar-right">
                  <li><a href="#">Sign Up</a></li>
                  <li class="dropdown">
                     <a href="#" class="dropdown-toggle" data-toggle="dropdown">Sign in <b class="caret"></b></a>
                     <ul class="dropdown-menu" style="padding: 15px;min-width: 250px;">
                        <li>
                           <div class="row">
                              <div class="col-md-12">
                                 <form class="form" role="form" method="post" action="login" accept-charset="UTF-8" id="login-nav">
                                    <div class="form-group">
                                       <label class="sr-only" for="exampleInputEmail2">Email address</label>
                                       <input type="email" class="form-control" id="exampleInputEmail2" placeholder="Email address" required>
                                    </div>
                                    <div class="form-group">
                                       <label class="sr-only" for="exampleInputPassword2">Password</label>
                                       <input type="password" class="form-control" id="exampleInputPassword2" placeholder="Password" required>
                                    </div>
                                    <div class="checkbox">
                                       <label>
                                       <input type="checkbox"> Remember me
                                       </label>
                                    </div>
                                    <div class="form-group">
                                       <button type="submit" class="btn btn-success btn-block">Sign in</button>
                                    </div>
                                 </form>
                              </div>
                           </div>
                        </li>
                        <li class="divider"></li>
                        <li>
                           <input class="btn btn-primary btn-block" type="button" id="sign-in-google" value="Sign In with Google">
                           <input class="btn btn-primary btn-block" type="button" id="sign-in-twitter" value="Sign In with Twitter">
                        </li>
                     </ul>
                  </li>
               </ul>
 
        </div><!--/.nav-collapse -->
      </div>
    <div class="ftstrip ftstrip-mini"></div>
    </div>


   