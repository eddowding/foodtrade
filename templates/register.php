<?php include '_header.php';?>

<style typ="text/css">
  body { 
    background: url(http://upload.wikimedia.org/wikipedia/commons/5/5a/Milan_Vegetable_Market.jpg) no-repeat center center fixed; 
    -webkit-background-size: cover;
    -moz-background-size: cover;
    -o-background-size: cover;
    background-size: cover;
  }

  .panel-default {
  opacity: 0.95;
  margin-top:30px;
  }
  .form-group.last { margin-bottom:0px; }
</style>

    <div class="container">
    <div class="row">
        <div class="col-md-5 col-md-offset-3">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <span class="glyphicon glyphicon-lock"></span> Login</div>
                <div class="panel-body">
                    <form class="form-horizontal" role="form">

                    <div class="form-group">
                        <label for="inputEmail3" class="col-sm-3 control-label">
                             Sign up as</label>


                        <div class="col-sm-9">

                          <div class="btn-group" data-toggle="buttons">
                            <label class="btn btn-default">
                              <input type="radio" name="options" id="option1"> Individual
                            </label>
                            <label class="btn btn-default">
                              <input type="radio" name="options" id="option2"> Food Business
                            </label>
                            <label class="btn btn-default">
                              <input type="radio" name="options" id="option3"> Organisation
                            </label>
                          </div>

                        </div>
                    </div>

                    <div class="form-group">
                        <label for="inputEmail3" class="col-sm-3 control-label">
                            Address</label>
                        <div class="col-sm-9">

                            <!-- autocomplete frorm 
                            <input type="text" class="form-control" id="location" placeholder="Address" required>
                        </div>
                    </div>


                    <div class="form-group">
                        <label for="inputEmail3" class="col-sm-3 control-label">
                            Email</label>
                        <div class="col-sm-9">
                            <input type="email" class="form-control" id="inputEmail3" placeholder="Email" required>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="inputPassword3" class="col-sm-3 control-label">
                            Password</label>
                        <div class="col-sm-9">
                            <input type="password" class="form-control" id="inputPassword3" placeholder="Password" required>
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="col-sm-offset-3 col-sm-9">
                            <div class="checkbox">
                                <label>
                                    <input type="checkbox"/>
                                    Remember me
                                </label>
                            </div>
                        </div>
                    </div>
                    <div class="form-group last">
                        <div class="col-sm-offset-3 col-sm-9">
                            <button type="submit" class="btn btn-success btn-sm">
                                Sign in</button>
                                 <button type="reset" class="btn btn-default btn-sm">
                                Reset</button>
                        </div>
                    </div>
                    </form>
                </div>
                <div class="panel-footer">
                    Not Registred? <a href="#">Register here</a></div>
            </div>
        </div>
    </div>
</div>


    </div><!-- col10 --> 
 <?php include '_footer.php';?>