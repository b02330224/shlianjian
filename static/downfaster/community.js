$(document).ready(function() {
    var url = new URL(window.location.href);
    var bizcircle = url.searchParams.get("bizcircle");
    if (bizcircle) {
        $('#bizcircle').val(bizcircle);
        getcommunitybybizcircle()
    }

    $("#navtabs a").click(function() {
        var district = $(this).text();
        $.ajax({
            type: "get",
            url: appConfig.URL + "/api/bizcircle?district=" + district,
            dataType: "json",
            success: function(result) {
                $('#nav').empty();
                $.each(result.data, function(i, item) {
                    $('#nav').append("<li class=\"nav-item\"><a class=\"nav-link\" href=\"community.html?bizcircle=" + item.Bizcircle + "\">" + item.Bizcircle + "</a></li>");
                });
            },

            error: function() {
                $("#alert").html("<div class=\"alert alert-danger text-center\" role=\"alert\" id=\"alert\">服务器开小差啦<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>")
            },
        });

        $('#navtabs a').removeClass('active');
        $(this).addClass('active');
    });

    $(function() {
        //$("#mainNav").load("navbar.html");
        $("#footer").load("footer.html");
    });

});

function getcommunitybybizcircle() {
    var input = $('#bizcircle').val();

    $.ajax({
        type: "get", //请求方式
        url: appConfig.URL + "/api/community/bizcircle/info/" + input, //地址，就是json文件的请求路径
        //url: "http://localhost/community/bizcircle/" + input,
        dataType: "json", //数据类型可以为 text xml json  script  jsonp
        success: function(result) { //返回的参数就是 action里面所有的有get和set方法的参数
            if (result.data.length == 0) {
                $("#alert").html("<div class=\"alert alert-danger text-center\" role=\"alert\" id=\"alert\">不存在该商圈<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>")
            } else {
                addGraph(result.data)
                addCommunityTable(result.data);
            }
        },

        error: function() {
            $("#alert").html("<div class=\"alert alert-danger text-center\" role=\"alert\" id=\"alert\">服务器开小差啦<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>")
        },
    });

    function addGraph(data) {
        var x = [];
        var y = [];

        for (var i in data) {
            x.push(data[i].Title);
            y.push(data[i].Onsale);
        }

        var chartdata = {
            labels: x,
            datasets: [{
                label: '在售房源',
                backgroundColor: 'rgba(2,117,216,1)',
                borderColor: 'rgba(2,117,216,1)',
                hoverBackgroundColor: 'rgba(2,117,216,1)',
                hoverBorderColor: 'rgba(2,117,216,1)',
                data: y
            }]
        };

        $('#mycanvas').remove();
        $('#chart-container').append('<canvas id="mycanvas"></canvas>');

        var ctx = $("#mycanvas");

        var barGraph = new Chart(ctx, {
            type: 'bar',
            data: chartdata
        });
    }
}

function addCommunityTable(result) {
    addHeader(result);
    addData(result);

    function addHeader(result) {
        $("#records_table tr").remove();
        $("#table-head tr").remove();
        //$('<tr>').html("<td>搜索结果:" + result.length + "个小区</td>").appendTo('#records_table');
        $('<tr>').html("<th>名称</th><th>区县</th><th>参考均价</th><th>在售房源</th><th>在租房源</th><th>建筑年代</th><th>建筑类型</th><th>物业费</th><th>物业公司</th><th>开发商</th><th>楼栋总数</th><th>房屋总数</th>").appendTo('#table-head');
    }

    function addData(result) {
        if ($('#dataTable').hasClass('dataTable')) {
            dttable = $('#dataTable').dataTable();
            dttable.fnClearTable(); //清空一下table
            dttable.fnDestroy(); //还原初始化了的datatable
        }
        
        $.each(result, function(i, item) {
            $('<tr>').html(
                "<td><a href='map.html?community=" + result[i].Title + "'>" + result[i].Title + "</a></td><td>" +
                result[i].District + "</td><td>" +
                result[i].Price + "</td><td>" +
                result[i].Onsale + "</td><td>" +
                result[i].Onrent + "</td><td>" +
                result[i].Year + "</td><td>" +
                result[i].Housetype + "</td><td>" +
                result[i].Cost + "</td><td>" +
                result[i].Service + "</td><td>" +
                result[i].Company + "</td><td>" +
                result[i].BuildingNum + "</td><td>" +
                result[i].HouseNum + "</td>").appendTo('#records_table');
        });
        $('#dataTable').DataTable({"order": [[ 3, "desc" ]]});
    }
}