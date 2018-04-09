/**
 * Created by ozgur on 6/13/15.
 */


$(function () {
    $("#user-details-div").css('display', 'block !important');
});


// User Add Form Script
$(function () {

    // Asagidaki function sadece form GET requestlerini dinamik yaparak modal icerigini doldurur
    //Post etmek icin asagidaki diger method kullanilir.
    $('.identityObjectAdd_FormRequest_Button').click(function () {

        // Assign handlers immediately after making the request,
        // and remember the jqxhr object for this request
        var jqxhr = $.get("add", function (data) {
            // alert("success");
            // alert(data);
            $("#addIdentityObjectModal .modal-body").html(data);
            $("#addIdentityObjectModal").modal('toggle');
        })
            .done(function () {
                // alert("second success");
            })
            .fail(function () {
                alert("error");
            })
            .always(function () {
                // alert("finished");
            });
    });


    $('#confirm-delete').on('show.bs.modal', function (e) {
        $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
    });

    $('#addIdentityObjectModal').on('hidden.bs.modal', function () {
        $("#addIdentity_ModalForm_Content").html("");
    });


    // Add butonu clicklendiginde
    $(document).on('click', '.button-class-addIdentityObject', function (e) {

        var objectType = $('#addIdentityObjectModal').attr('data-object-type');
        // alert(objectType);


        $.ajax({
            type: $('#form-id-addIdentityObject').attr('method'),
            url: $('#form-id-addIdentityObject').attr('action'),
            data: $('#form-id-addIdentityObject').serialize(),

            error: function (jqXHR, textStatus, errorThrown) {
                alert('fail: ' + errorThrown);    //if fails
            },

        }).done(function (data, textStatus, xhr) {
            // alert('request sent');
            // alert(data); // Sunucudan donen data

            // $('#createUserModal_id').find('.modal').html(data);

            $('#addIdentityObjectModal').find('.modal-body').html(data);

            //Done sadece querynin yapildigini gosterir. Dogru calisip
            // calismadigini gostermez. dolayisi ile eger cevap icinde
            // has-error alani yok ise cevap dogrudur
            if ($(data).find('.has-error').length > 0) {

                // alert(xhr.getElementById("createUserForm_id"));
                // e.preventDefault();
                $('#form-id-addIdentityObject').find('.modal').html(data);
            } else {
                $('#form-id-addIdentityObject').modal('toggle');
                window.location.replace("/identityManager/" + objectType + "/");
            }
        }).error(function (xhr, ajaxOptions, thrownError) {
                // handle response errors here
                alert('error');
            });
        // });
    });
});
