(function($){
    $(document).ready(function() {
      
        $.fn.editable.defaults.mode = 'inline';
        $('.editable').editable();

        //Activate tooltips
        $("[data-toggle='tooltip']").tooltip();
        $(".tooltip").tooltip();
        
        // Menu tree sortable
        /*$("ul.todo-list").sortable(
            
        );*/


        $("ul.my-tree").sortable();
         
    });
    
    
    
   
})(jQuery);