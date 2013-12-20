<?php include '_header.php';?>

    <div class="container">
 


    <?php include '_sidebar.php';?>

  
      <div class="col-md-10">
   <pre>

DEVELOPER NOTES

- Use nexted sortable: http://johnny.github.io/jquery-sortable/
- Note there's a hidden div on the tag lists 

We'll add merge tags later, I'm just adding the icon since I'm here. 
   </pre>

<form  role="form" class="well">
      <div class="row">
        <div class="col-md-6">

          <div class="form-group"> 
            <input type="text" class="form-control" id="tag1"  value="Fish">
          </div> 

  <button type="submit" class="btn btn-sm btn-success">Add term</button>

        </div><!-- col md 5 -->
        <div class="col-md-6">

          <div class="form-group"> 
            <textarea class="form-control" rows="3" disabled="disabled" placeholder="Description" ></textarea> 
          </div> 
          <div class="form-group"> 
            <input type="file" class="form-control" disabled="disabled" id="file">
          </div>

        </div><!-- col md 5 -->
      </div>
</form>
   
 

<h3>All tags</h3>
<hr > 
   <ul class="tag_admin">


   <!-- tag item --> 
    <li class="tag_item_admin">
      <i class="fa fa-arrows text-muted"></i>
      <input type="checkbox"> 
      <span>Fish</span>
      <span class="pull-right">
        <i class="fa fa-edit"></i>
        <i class="fa fa-trash-o"></i>
        <i class="fa fa-compress" title="Merge selected"></i>
      </span>
      <!-- show this form on edit --> 
      <div class="hidden">

        <form role="form">
          <div class="form-group"> 
            <input type="text" class="form-control" id="tag1" value="Fish">
          </div>
          <div class="form-group"> 
            <textarea class="form-control" rows="3" placeholder="Description" disabled="disabled"></textarea> 
          </div> 
          <div class="form-group"> 
            <input type="text" class="form-control" id="tag1" disabled="disabled" placeholder="http://www.link.com">
          </div> 
          <div class="form-group">
            <label for="image">Image</label>
            <input type="file" class="form-control" disabled="disabled" id="file">
          </div>

          <button type="submit" class="btn btn-sm btn-success">Save</button>
        </form> 

      </div><!-- hidden-->
      <ull>
      <ul>
    </li>





    <li class="tag_item_admin">
      <i class="fa fa-arrows text-muted"></i>
      <input type="checkbox"> 
      <span>Fish</span>
      <span class="pull-right">
        <i class="fa fa-edit"></i>
        <i class="fa fa-trash-o"></i>
        <i class="fa fa-compress" title="Merge selected"></i>
      </span>
      <!-- show this form on edit --> 
      <div class="hidden">

        <form role="form">
          <div class="form-group"> 
            <input type="text" class="form-control" id="tag1" value="Fish">
          </div>
          <div class="form-group"> 
            <textarea class="form-control" rows="3" placeholder="Description" disabled="disabled"></textarea> 
          </div> 
          <div class="form-group"> 
            <input type="text" class="form-control" id="tag1" disabled="disabled" placeholder="http://www.link.com">
          </div> 
          <div class="form-group">
            <label for="image">Image</label>
            <input type="file" class="form-control" disabled="disabled" id="file">
          </div>

          <button type="submit" class="btn btn-sm btn-success">Save</button>
        </form> 

      </div><!-- hidden-->
    </li><li class="tag_item_admin">
      <i class="fa fa-arrows text-muted"></i>
      <input type="checkbox"> 
      <span>Fish</span>
      <span class="pull-right">
        <i class="fa fa-edit"></i>
        <i class="fa fa-trash-o"></i>
        <i class="fa fa-compress" title="Merge selected"></i>
      </span>
      <!-- show this form on edit --> 
      <div class="hidden">

        <form role="form">
          <div class="form-group"> 
            <input type="text" class="form-control" id="tag1" value="Fish">
          </div>
          <div class="form-group"> 
            <textarea class="form-control" rows="3" placeholder="Description" disabled="disabled"></textarea> 
          </div> 
          <div class="form-group"> 
            <input type="text" class="form-control" id="tag1" disabled="disabled" placeholder="http://www.link.com">
          </div> 
          <div class="form-group">
            <label for="image">Image</label>
            <input type="file" class="form-control" disabled="disabled" id="file">
          </div>

          <button type="submit" class="btn btn-sm btn-success">Save</button>
        </form> 

      </div><!-- hidden-->
    </li><li class="tag_item_admin">
      <i class="fa fa-arrows text-muted"></i>
      <input type="checkbox"> 
      <span>Fish</span>
      <span class="pull-right">
        <i class="fa fa-edit"></i>
        <i class="fa fa-trash-o"></i>
        <i class="fa fa-compress" title="Merge selected"></i>
      </span>
      <!-- show this form on edit --> 
      <div class="hidden">

        <form role="form">
          <div class="form-group"> 
            <input type="text" class="form-control" id="tag1" value="Fish">
          </div>
          <div class="form-group"> 
            <textarea class="form-control" rows="3" placeholder="Description" disabled="disabled"></textarea> 
          </div> 
          <div class="form-group"> 
            <input type="text" class="form-control" id="tag1" disabled="disabled" placeholder="http://www.link.com">
          </div> 
          <div class="form-group">
            <label for="image">Image</label>
            <input type="file" class="form-control" disabled="disabled" id="file">
          </div>

          <button type="submit" class="btn btn-sm btn-success">Save</button>
        </form> 

      </div><!-- hidden-->
    </li><li class="tag_item_admin">
      <i class="fa fa-arrows text-muted"></i>
      <input type="checkbox"> 
      <span>Fish</span>
      <span class="pull-right">
        <i class="fa fa-edit"></i>
        <i class="fa fa-trash-o"></i>
        <i class="fa fa-compress" title="Merge selected"></i>
      </span>
      <!-- show this form on edit --> 
      <div class="hidden">

        <form role="form">
          <div class="form-group"> 
            <input type="text" class="form-control" id="tag1" value="Fish">
          </div>
          <div class="form-group"> 
            <textarea class="form-control" rows="3" placeholder="Description" disabled="disabled"></textarea> 
          </div> 
          <div class="form-group"> 
            <input type="text" class="form-control" id="tag1" disabled="disabled" placeholder="http://www.link.com">
          </div> 
          <div class="form-group">
            <label for="image">Image</label>
            <input type="file" class="form-control" disabled="disabled" id="file">
          </div>

          <button type="submit" class="btn btn-sm btn-success">Save</button>
        </form> 

      </div><!-- hidden-->
    </li>







    <li>
    <ul>

    <li class="tag_item_admin">
      <i class="fa fa-arrows text-muted"></i>
      <input type="checkbox"> 
      <span>Fish</span>
      <span class="pull-right">
        <i class="fa fa-edit"></i>
        <i class="fa fa-trash-o"></i>
        <i class="fa fa-compress" title="Merge selected"></i>
      </span>
      <!-- show this form on edit --> 
      <div class="hidden">

        <form role="form">
          <div class="form-group"> 
            <input type="text" class="form-control" id="tag1" value="Fish">
          </div>
          <div class="form-group"> 
            <textarea class="form-control" rows="3" placeholder="Description" disabled="disabled"></textarea> 
          </div> 
          <div class="form-group"> 
            <input type="text" class="form-control" id="tag1" disabled="disabled" placeholder="http://www.link.com">
          </div> 
          <div class="form-group">
            <label for="image">Image</label>
            <input type="file" class="form-control" disabled="disabled" id="file">
          </div>

          <button type="submit" class="btn btn-sm btn-success">Save</button>
        </form> 

      </div><!-- hidden-->
    </li><li class="tag_item_admin">
      <i class="fa fa-arrows text-muted"></i>
      <input type="checkbox"> 
      <span>Fish</span>
      <span class="pull-right">
        <i class="fa fa-edit"></i>
        <i class="fa fa-trash-o"></i>
        <i class="fa fa-compress" title="Merge selected"></i>
      </span>
      <!-- show this form on edit --> 
      <div class="hidden">

        <form role="form">
          <div class="form-group"> 
            <input type="text" class="form-control" id="tag1" value="Fish">
          </div>
          <div class="form-group"> 
            <textarea class="form-control" rows="3" placeholder="Description" disabled="disabled"></textarea> 
          </div> 
          <div class="form-group"> 
            <input type="text" class="form-control" id="tag1" disabled="disabled" placeholder="http://www.link.com">
          </div> 
          <div class="form-group">
            <label for="image">Image</label>
            <input type="file" class="form-control" disabled="disabled" id="file">
          </div>

          <button type="submit" class="btn btn-sm btn-success">Save</button>
        </form> 

      </div><!-- hidden-->
    </li><li class="tag_item_admin">
      <i class="fa fa-arrows text-muted"></i>
      <input type="checkbox"> 
      <span>Fish</span>
      <span class="pull-right">
        <i class="fa fa-edit"></i>
        <i class="fa fa-trash-o"></i>
        <i class="fa fa-compress" title="Merge selected"></i>
      </span>
      <!-- show this form on edit --> 
      <div class="hidden">

        <form role="form">
          <div class="form-group"> 
            <input type="text" class="form-control" id="tag1" value="Fish">
          </div>
          <div class="form-group"> 
            <textarea class="form-control" rows="3" placeholder="Description" disabled="disabled"></textarea> 
          </div> 
          <div class="form-group"> 
            <input type="text" class="form-control" id="tag1" disabled="disabled" placeholder="http://www.link.com">
          </div> 
          <div class="form-group">
            <label for="image">Image</label>
            <input type="file" class="form-control" disabled="disabled" id="file">
          </div>

          <button type="submit" class="btn btn-sm btn-success">Save</button>
        </form> 

      </div><!-- hidden-->
    </li>
    </ul>
    </li>



    </ul>


       
      </div><!-- closes 10 -->
 
    </div> 


 <?php include '_footer.php';?>
