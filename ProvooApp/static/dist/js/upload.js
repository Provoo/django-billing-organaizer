$(document).ready(function () {
    var frm = $('#uploadForm');
    var data = new FormData($('form').get(0));
    frm.submit(function () {
        console.log("create post is working!") // sanity check
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                //$("#SOME-DIV").html(data);
                alert(data);

            },
            error: function (data) {
                //$("#MESSAGE-DIV").html("Something went wrong!");
                alert("Something went wrong!");
            }
        });
        return {name: "hola"};
    });
});
