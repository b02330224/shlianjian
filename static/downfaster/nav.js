$(document).ready(function() {
    $.ajax({
        type: "get",
        url: appConfig.URL + "/api/user/info",
        dataType: "json",
        xhrFields: { withCredentials: true },
        success: function(result) {
            $("#setting-username").attr("value", result.data.Username);
            $('#register').hide()
            $('#login').hide()
            $('#nav-right').append('<li class="nav-item"><a class="nav-link" href="userinfo.html" id="userinfo"><i class="fa fa-fw fa-user"></i>' + result.data.Username + '</a></li>');
            $('#nav-right').append('<li class="nav-item"><a class="nav-link" href="setting.html" id="setting"><i class="fa fa-fw fa-cog"></i>设置</a></li>');
            $('#nav-right').append('<li class="nav-item"><a class="nav-link" href="#" id="logout" onclick=logout()><i class="fa fa-fw fa-sign-out"></i>注销</a></li>');
        }
    });

});

function logout() {
    var confirmText = "确定要登出吗？";
    if (confirm(confirmText)) {
        $.ajax({
            type: "get",
            url: appConfig.URL + "/api/user/logout",
            dataType: "json",
            xhrFields: { withCredentials: true },
            success: function(result) {
                $('#userinfo').hide()
                $('#logout').hide()
                $('#setting').hide()
                $('#register').show()
                $('#login').show()
            },

            error: function() {
                $("#alert").html("<div class=\"alert alert-danger text-center\" role=\"alert\" id=\"alert\">服务器开小差啦<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>")
            },
        });
    }
}