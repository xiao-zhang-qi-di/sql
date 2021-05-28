$('#btnLogin').click(function () {
   authenticateUser()
});

function authenticateUser() {
    var inputUsername = $('#inputUsername');
    var inputPassword = $('#inputPassword');
    $.ajax({
        type: "post",
        url: "/authenticate/",
        dataType: "json",
        data: {
            username: inputUsername.val(),
            password: inputPassword.val()
        },
        complete: function () {

        },
        success: function (data) {
            if (data.status == 0) {
                $(location).attr('href', '/allworkflow/')
            } else {
                // html() 方法设置或返回被选元素的内容（innerHTML）
                $('#wrongpwd-modal-body').html(data.msg);
                $('#wrongpwd-modal').modal({
                    keyboard: true
                });
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(errorThrown);
        }
    })
}