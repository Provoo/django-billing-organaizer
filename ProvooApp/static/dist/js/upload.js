$(document).ready(function () {
    var fileSelect = document.getElementById('file-select');
    var frm = $('#uploadForm');
    frm.submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: new FormData(this),
            processData: false,
            contentType: false,
            success: function (data) {
                //$("#SOME-DIV").html(data);
                alert(data.mensaje);

            },
            error: function (data) {
                //$("#MESSAGE-DIV").html("Something went wrong!");
                alert("Something went wrong!");
            }

        });

    });
});
