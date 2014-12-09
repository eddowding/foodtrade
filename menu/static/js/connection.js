$(document).ready(function() {
    var establishments = new Bloodhound({
        name: 'establishments',
        remote: '/menu/establishment/lookup/name/?q=%QUERY',
        datumTokenizer: function(d) {
            return Bloodhound.tokenizers.whitespace(d);
        },
        queryTokenizer: Bloodhound.tokenizers.whitespace
    });

    establishments.initialize();

    $('.typeahead').typeahead(null, {
        name: 'establishments',
        displayKey: 'name',
        source: establishments.ttAdapter()
    });
});
