<?php include '_header.php';?>

<style type="text/css">
    
    .panel-body input[type=checkbox]:checked + label { 

        color: #c00; 
    } 

</style>

<div class="container">
    <div class="row">

 <div class="panel-body">
                    <ul class="list-group">
                        <li class="list-group-item clearfix">
                            <div class="pull-right action-buttons">
                             <button class="btn btn-default">Buys from</button>
                             <button class="btn btn-default">Sells to</button>
                            </div>
                            <div class="checkbox">
                                <input type="checkbox" id="checkbox" />
                                <label for="checkbox">
                                     <img src="https://pbs.twimg.com/profile_images/67617802/thoughtful_logo_bigger.jpg" alt="THEIRNAME"
          class=" img-responsive pull-left" style="width:20px; margin-right: 5px;" /> 
                                    List group item heading
                                </label>
                            </div>
                        </li>
                        <li class="list-group-item clearfix">
                            <div class="pull-right action-buttons">
                             <button class="btn btn-default">Buys from</button>
                             <button class="btn btn-default">Sells to</button>
                            </div>
                            <div class="checkbox">
                                <input type="checkbox" id="checkbox" />
                                <label for="checkbox">
                                    List group item heading
                                </label>
                            </div>
                        </li>
                        <li class="list-group-item clearfix">
                            <div class="pull-right action-buttons">
                             <button class="btn btn-default">Buys from</button>
                             <button class="btn btn-default">Sells to</button>
                            </div>
                            <div class="checkbox">
                                <input type="checkbox" id="checkbox" />
                                <label for="checkbox">
                                    List group item heading
                                </label>
                            </div>
                        </li>
                        
                        </ul>
                        </div>


        <div class="col-md-12 well well-sm">
            <form action="#" method="get">
                <div class="input-group">
                    <!-- USE TWITTER TYPEAHEAD JSON WITH API TO SEARCH -->
                    <input class="form-control" id="system-search" name="q" placeholder="Search for" required>
                    <span class="input-group-btn">
                        <button type="submit" class="btn btn-default"><i class="glyphicon glyphicon-search"></i></button>
                    </span>
                </div>
            </form>
        </div>
        <div class="col-md-12">
         <table class="table table-list-search">
            <thead>
                <tr>
                    <th>cb</th>
                    <th>av / name</th>
                    <th>action</th> 
                </tr>
            </thead>
            <tbody style="height: 300px; overflow: scroll-y;">
                <tr>
                    <td colspan="3">
                     <div class="checkbox">
                        <input type="checkbox" id="checkbox" />
                        <label for="checkbox">
                            List group item heading
                        </label>
                     </div>
                    <div class="pull-right">
                     <button class="btn btn-default">Buys from</button>
                     <button class="btn btn-default">Sells to</button>
                    </div>

                    </td> 
                </tr>
               
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="3" class="text-right"><button class="btn btn-primary">Invite selected</button>
                </tr>
            </tfoot>
        </table>   
        </div>
    </div>
</div>



 
 
<?php include '_footer.php';?>


