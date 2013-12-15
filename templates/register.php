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
  opacity: 1;
  margin-top:30px;
  }
  .form-group.last { margin-bottom:0px; }
</style>

    <div class="container">
    <div class="row">
        <div class="col-md-6 col-md-offset-3">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <i class="fa fa-lock"></i> Let's help people find you</div>
                <div class="panel-body">
                    <form class="form-horizontal" role="form">

                    <div class="alert alert-danger">This shows up just after you authorize twitter </div>


                    <div class="container-responsive">
                        <div id=" " class="clearfix">
                          <div class="col-md-3" id="avatar">
                            <img class="img-thumbnail center-block" style="width:70px;" src="http://a0.twimg.com/profile_images/2596092158/afpecvf41m8f0juql78p_bigger.png"  />
                          </div>
                         
                          <div class="col-md-9">
                             <h1>Smales Farm</h1>
                            
                          </div><!-- end header middle -->
                        </div>
                    </div>
  <hr /> 
                         

                    <div class="form-group">
                        <label for="inputEmail3" class="col-sm-3 control-label">
                            Description</label>
                        <div class="col-sm-9">
                            <textarea class="form-control" id="description" rows="5" required>Load from twitter description ------> quis risus eget urna mollis ornare vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam id dolor id nibh ultricies vehicula.</textarea>
                        </div>
                    </div>


                    <div class="form-group">
                        <label for="business_type" class="col-sm-3 control-label">
                             Sign up as</label>


                        <div class="col-sm-9">

                          <div class="btn-group" data-toggle="buttons">
                            <label class="btn btn-default">
                              <input type="radio" name="options" id="option1"> Individual
                            </label>

                            <!-- on click show the BUSIENSS TYPE field -->
                            <label class="btn btn-default">
                              <input type="radio" name="options" id="option2"> Food Business
                            </label>
                            <label class="btn btn-success active">
                              <input type="radio" name="options" id="option3"> Organisation
                            </label>
                          </div>

                        </div>
                    </div>


                    <!-- if they click FOOD BUSINESS, SHOW THIS 
                            AUTOCOMPLETE / TYPEAHEAD ON BUSINESS TYPE TAGS
                            -->
                    <div class="form-group">
                        <label for="inputEmail3" class="col-sm-3 control-label">
                            Type</label>
                        <div class="col-sm-9">
                            <input type="text" class="form-control" id="business_type" placeholder="Farm, wholesaler, restaurant, bakery..." required>
                        </div>
                    </div> 

                    <div class="form-group">
                        <label for="inputEmail3" class="col-sm-3 control-label">
                            Address</label>
                        <div class="col-sm-9">

                            <!-- autocomplete from google-->
                            <input type="text" class="form-control" id="location" placeholder="Address" required>

                        <span class="help-block">   
                            Area, Town from Twitter
                        </span>
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
                 
            </div>
        </div>
    </div>
</div>


    </div><!-- col10 --> 
 <?php include '_footer.php';?>