/* this is the site specific js, put anything wierd in here */
$(document).ready(function() {
    $('table tbody tr').bind("click", function() {
        var elem = $(this).find("a");
        if (elem.length != 0) {
            window.location = elem.attr("href");
        };
    return false;
    });   
    $('.expander').bind("click", function() {
        console.log($(this).parent());
        $($(this).parent()[0]).hide();
        $(this).parent().parent().find(".hidden").show()
    })
    $("#search input").labelify();
});
