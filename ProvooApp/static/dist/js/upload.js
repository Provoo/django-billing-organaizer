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
                $("#ajaxMessage1").html(data.mensaje);
                //alert(data.mensaje);
            },
            error: function (data) {
                //$("#MESSAGE-DIV").html("Something went wrong!");
                alert("Something went wrong!");
            }

        });

    });

    var manualform = $('#gajax');
    manualform.click(function (e) {
        e.preventDefault();
        $.ajax({
            url: manualform.attr('action'),
            data: new FormData(this),
            processData: false,
            contentType: false,
            success: function (data) {
              $("#ajaxMessage2").html(data.mensaje);
            },
            error: function (data) {
                //$("#MESSAGE-DIV").html("Something went wrong!");
                alert("Something went wrong!");
            }

        });

    });
});
