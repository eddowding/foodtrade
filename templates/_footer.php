</div>



setup footer
- about us 
- pricing
- blog
- facebook / twitter 


<div class="container" id="footer">    

  <div class="row">
    <div class="col-lg-12">
        <div class="ftstrip"></div>
    </div>
  </div>
  <div class="row">
    <div class="col-lg-12" id="footer_container">
      <div class="col-md-3">
        <ul class="list-unstyled">
          <li>GitHub<li>
          <li><a href="/about.html">About us</a></li>
          <li><a href="http://digest.foodtrade.com/" target="_blank">Blog</a></li>
          <li><a href="/contact.html">Contact & support</a></li>
         </ul>
      </div>
      <div class="col-md-3">
        <ul class="list-unstyled">
          <li>Applications<li>
          <li><a href="#">Product for Mac</a></li>
          <li><a href="#">Product for Windows</a></li>
          <li><a href="#">Product for Eclipse</a></li>
          <li><a href="#">Product mobile apps</a></li>              
        </ul>
      </div>
      <div class="col-md-3">
        <ul class="list-unstyled">
          <li>Services<li>
          <li><a href="#">Web analytics</a></li>
          <li><a href="#">Presentations</a></li>
          <li><a href="#">Code snippets</a></li>
          <li><a href="#">Job board</a></li>              
        </ul>
      </div>
      <div class="col-md-3">
        <ul class="list-unstyled">
          <li>Stay connected<li>
          <li><a href="http://www.facebook.com/foodtradeHQ"><i class="fa fa-facebook"></i></a> <a href="http://www.twitter.com/foodtradeHQ"><i class="fa fa-twitter"></i></a></li>
          <li><a href="#">Product Markdown</a></li>
          <li><a href="#">Product Pages</a></li>              
        </ul>
      </div>  
    </div>
  </div>
  <hr>
  <div class="row">
    <div class="col-lg-12">
      <div class="col-md-8">
        <a href="/terms">Terms of Service</a>    
        <a href="/privacy">Privacy</a>  
      </div>
      <div class="col-md-4">
        <p class="muted pull-right">&copy; 2013 Foodtrade. All rights reserved</p>
      </div>
    </div>
  </div>
</div>


<!-- UserVoice JavaScript SDK (only needed once on a page) -->
<script>(function(){var uv=document.createElement('script');uv.type='text/javascript';uv.async=true;uv.src='//widget.uservoice.com/HloB2aRxdk7fbhWMOI5AlQ.js';var s=document.getElementsByTagName('script')[0];s.parentNode.insertBefore(uv,s)})()</script>

<!-- A tab to launch the Classic Widget -->
<script>UserVoice=window.UserVoice||[];UserVoice.push(['showTab','classic_widget',{mode:'full',primary_color:'#f08119',link_color:'#61ae32',default_mode:'support',forum_id:231923,tab_label:'Feedback & Support',tab_color:'#cc6d00',tab_position:'middle-right',tab_inverted:false}]);</script>



    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://code.jquery.com/jquery-1.10.2.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
     <script type="text/javascript">
$(document).ready(function() {
    var activeSystemClass = $('.list-group-item.active');

    //something is entered in search form
    $('#system-search').keyup( function() {
       var that = this;
        // affect all table rows on in systems table
        var tableBody = $('.table-list-search tbody');
        var tableRowsClass = $('.table-list-search tbody tr');
        $('.search-sf').remove();
        tableRowsClass.each( function(i, val) {
        
            //Lower text for case insensitive
            var rowText = $(val).text().toLowerCase();
            var inputText = $(that).val().toLowerCase();
            if(inputText != '')
            {
                $('.search-query-sf').remove();
                tableBody.prepend('<tr class="search-query-sf"><td colspan="6"><strong>Searching for: "'
                    + $(that).val()
                    + '"</strong></td></tr>');
            }
            else
            {
                $('.search-query-sf').remove();
            }

            if( rowText.indexOf( inputText ) == -1 )
            {
                //hide rows
                tableRowsClass.eq(i).hide();
                
            }
            else
            {
                $('.search-sf').remove();
                tableRowsClass.eq(i).show();
            }
        });
        //all tr elements are hidden
        if(tableRowsClass.children(':visible').length == 0)
        {
            tableBody.append('<tr class="search-sf"><td class="text-muted" colspan="6">No entries found.</td></tr>');
        }
    });
});
    </script>

    <script type="text/javascript">


      $('.tip').tooltip()

      /**
 *
 * jquery.charcounter.js version 1.2
 * requires jQuery version 1.2 or higher
 * Copyright (c) 2007 Tom Deater (http://www.tomdeater.com)
 * Licensed under the MIT License:
 * http://www.opensource.org/licenses/mit-license.php
 * 
 */
 
(function($) {
    /**
	 * attaches a character counter to each textarea element in the jQuery object
	 * usage: $("#myTextArea").charCounter(max, settings);
	 */
	
	$.fn.charCounter = function (max, settings) {
		max = max || 100;
		settings = $.extend({
			container: "<span></span>",
			classname: "charcounter",
			format: "(%1 characters remaining)",
			pulse: true,
			delay: 0
		}, settings);
		var p, timeout;
		
		function count(el, container) {
			el = $(el);
			if (el.val().length > max) {
			    el.val(el.val().substring(0, max));
			    if (settings.pulse && !p) {
			    	pulse(container, true);
			    };
			};
			if (settings.delay > 0) {
				if (timeout) {
					window.clearTimeout(timeout);
				}
				timeout = window.setTimeout(function () {
					container.html(settings.format.replace(/%1/, (max - el.val().length)));
				}, settings.delay);
			} else {
				container.html(settings.format.replace(/%1/, (max - el.val().length)));
			}
		};
		
		function pulse(el, again) {
			if (p) {
				window.clearTimeout(p);
				p = null;
			};
			el.animate({ opacity: 0.1 }, 100, function () {
				$(this).animate({ opacity: 1.0 }, 100);
			});
			if (again) {
				p = window.setTimeout(function () { pulse(el) }, 200);
			};
		};
		
		return this.each(function () {
			var container;
			if (!settings.container.match(/^<.+>$/)) {
				// use existing element to hold counter message
				container = $(settings.container);
			} else {
				// append element to hold counter message (clean up old element first)
				$(this).next("." + settings.classname).remove();
				container = $(settings.container)
								.insertAfter(this)
								.addClass(settings.classname);
			}
			$(this)
				.unbind(".charCounter")
				.bind("keydown.charCounter", function () { count(this, container); })
				.bind("keypress.charCounter", function () { count(this, container); })
				.bind("keyup.charCounter", function () { count(this, container); })
				.bind("focus.charCounter", function () { count(this, container); })
				.bind("mouseover.charCounter", function () { count(this, container); })
				.bind("mouseout.charCounter", function () { count(this, container); })
				.bind("paste.charCounter", function () { 
					var me = this;
					setTimeout(function () { count(me, container); }, 10);
				});
			if (this.addEventListener) {
				this.addEventListener('input', function () { count(this, container); }, false);
			};
			count(this, container);
		});
	};

})(jQuery);

$(function() {
    $(".counted").charCounter(320,{container: "#counter"});
});

    </script>
  </body>
</html>
  