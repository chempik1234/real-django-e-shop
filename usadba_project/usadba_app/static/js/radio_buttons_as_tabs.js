$('input[type="radio"]').click(function () {
    if ($(this).attr("value") == "False") {
        console.log("." + $(this).attr("name") + "_hide");
        $("." + $(this).attr("name") + "_hide_true").hide('slow');
        $("." + $(this).attr("name") + "_hide_false").show('slow');
    } else {
        $("." + $(this).attr("name") + "_hide_true").show('slow');
        $("." + $(this).attr("name") + "_hide_false").hide('slow');
    }
});

$('input[type="radio"]').trigger('click');  // trigger the event