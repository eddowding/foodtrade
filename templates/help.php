<?php include '_header.php';?>

    <div  class="container">

    <?php include '_sidebar_search.php';?>

   

    <div class="col-md-10" id="single">

    <div class="container-responsive">
    <div class="row">
     <div class="col-md-6">
     <h1>List of all pages</h1>

     <ul>

     <li><a href="home.php">home.php</a></li>
     <li>signup in header -> twitter authoriation -> <a href="register.php">register.php</a></li>
        
      <li><a href="single-loggedout.php">single-view or biz / org when logged out.php</a></li>  
     <li>
      Unknown type
        <ul>
        <li><a href="single-unknown.php">single-unknown.php</a></li>  
        </ul>
      </li>
     <li>
      Business
        <ul>
           <li><a href="single-business-empty.php">single-business-empty.php</a></li>
           <li><a href="single-business.php">single-business.php</a></li>
           <li><a href="single-business_edit.php">single-business-edit.php</a></li>

        </ul>
      </li>
     <li>
      Organisation
        <ul>
           <li><a href="single-organisation-unclaimed.php">single-organisation-unclaimed.php</a></li>
           <li><a href="single-organisation.php">single-organisation.php</a></li>

        </ul>
      </li>
     <li>
      Activity
        <ul>
           <li><a href="activity_single.php">single view</a></li>
           <li><a href="activity.php">home / search results</a></li>

        </ul>
      </li>
     
     <li>
      ADMIN
        <ul>
           <li><a href="admin_tags.php">Tags</a></li>  
        </ul>
      </li>
     </ul>


     <h1>Permissions</h1>

     <pre>

On unclaimed profiles (business or organsation)
- Any registered user can contribute information to it

ON CLAIMED BUSINESS

Owner controls:
- foods
- connections
--- anyone can add themselves
--- owner can remove
- organisations
- updates
- Team
--- anyone can add themselves
--- owner can remove

Owner does not control:
- customers (businesses <- individual relationship)



ON CLAIMED ORGANISATIONS

Owner controls:
- updates
- Team
--- anyone can add themselves
--- owner can remove
- Members
--- anyone can add themselves
--- owner can remove

Owner does not control:
- foods: this is just searching all foods by members of this organsation


Organisations     

     </pre>
</div>
     <div class="col-md-6">
     <h1>To do</h1>

     <pre>

PHUNKA 
-------
change sign up / sign in -> My account
fix new message modal - showing as shaded - blue botton on header bar
when you mouseover the cards / maps, make the other highlight 
After a customer has signed up, prompt them to tweet about it 
make active state of default buttons be the 'success' style
single-business.php shows two distances: first is distance to its location from yours; second (bullseye) is the distance between you and its nearest trade point
crowdtag produce


ED DOWDING
---------- 
add like on twitter / facebook to header
add activity feed card style for org / individial 

about us page
- pricing
- basic info
- data: odi, godan
- mission
- link to blog
- international: africa / gsm
- funding



0.2+ IDEAS
----------
single customer view
integreate with USDA’s Nutrient Database, Foodwiki.com, Nutsci.org and Open Food
http://en.openfoodfacts.org/
http://en.openfoodfacts.org/product/070157888646/crumbled-feta-cheese-treasure-cave


     </pre>

   
     </div>

     </div>
        
     </div>
        


    </div><!-- col10 --> 

   
 <?php include '_footer.php';?>