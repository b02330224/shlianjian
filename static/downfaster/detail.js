$(document).ready(function() {
    var url = new URL(window.location.href);
    var community = url.searchParams.get("community");
    if (community) {
        $('#community').val(community);
        getcountbycommunity()
    }

    $(function() {
        //$("#mainNav").load("navbar.html");
        $("#footer").load("footer.html");
        document.getElementById('etime').valueAsDate = new Date();
        get_community_name();
    });

});

function getcountbycommunity() {
    var input = $('#community').val();
    var stime = $('#stime').val();
    var etime = $('#etime').val();
    var type = $('#type').val();

    $.ajax({
        type: "get", //请求方式
        url: appConfig.URL + "/api/sell/" + type + "/count/" + input +
            "?stime=" + stime +
            "&etime=" + etime, //地址，就是json文件的请求路径
        dataType: "json", //数据类型可以为 text xml json  script  jsonp
        success: function(result) { //返回的参数就是 action里面所有的有get和set方法的参数
            if (result.data.length == 0) {
                $("#alert").html("<div class=\"alert alert-danger text-center\" role=\"alert\" id=\"alert\">不存在该小区<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>")
            } else {
                addGraph(result.data, input);
                $.ajax({
                    type: "get", //请求方式
                    url: appConfig.URL + "/api/community/title/" + input, //地址，就是json文件的请求路径
                    dataType: "json", //数据类型可以为 text xml json  script  jsonp
                    success: function(result) { //返回的参数就是 action里面所有的有get和set方法的参数
                        addCommunityTable(result.data);
                    },
                    error: function() {
                        $("#alert").html("<div class=\"alert alert-danger text-center\" role=\"alert\" id=\"alert\">服务器开小差啦<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>")
                    },
                });
            }
        },

        error: function() {
            $("#alert").html("<div class=\"alert alert-danger text-center\" role=\"alert\" id=\"alert\">服务器开小差啦<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>")
        },
    });

    function addGraph(data, input) {
        var x = [];
        var y = [];
        var coloR = [];

        var dynamicColors = function() {
            var r = Math.floor(Math.random() * 255);
            var g = Math.floor(Math.random() * 255);
            var b = Math.floor(Math.random() * 255);
            return "rgb(" + r + "," + g + "," + b + ")";
        };

        for (var i in data) {
            x.push(data[i]["Type"]);
            y.push(data[i]["Total"]);
            coloR.push(dynamicColors());
        }

        var chartdata = {
            labels: x,
            datasets: [{
                label: input,
                backgroundColor: coloR,
                borderColor: 'rgba(151,187,205,1)',
                hoverBackgroundColor: 'rgba(200, 200, 200, 1)',
                hoverBorderColor: 'rgba(200, 200, 200, 1)',
                data: y
            }]
        };

        $('#mycanvas').remove();
        $('#chart-container').append('<canvas id="mycanvas"></canvas>');

        var ctx = $("#mycanvas");

        var barGraph = new Chart(ctx, {
            type: "pie",
            data: chartdata,
        });
    }
}

function addCommunityTable(result) {
    addHeader(result);
    if (result.length == 0) {
        $('<tr>').html("<td>搜索结果为空</td>").appendTo('#records_table');
    }
    addData(result);


    function addHeader(result) {
        $("#records_table tr").remove();
        $("#table-head tr").remove();
        $('<tr class="info">').html("<th>名称</th><th>区县</th><th>建筑年代</th><th>建筑类型</th><th>物业费</th><th>物业公司</th><th>开发商</th><th>楼栋总数</th><th>房屋总数</th>").appendTo('#table-head');
    }

    function addData(result) {
        if ($('#dataTable').hasClass('dataTable')) {
            dttable = $('#dataTable').dataTable();
            dttable.fnClearTable(); //清空一下table
            dttable.fnDestroy(); //还原初始化了的datatable
        }
        
        $.each(result, function(i, item) {
            $('<tr>').html(
                "<td><a href='sellinfo.html?community=" + result[i].Title + "'>" + result[i].Title + "</a></td><td>" +
                result[i].District + "</td><td>" +
                result[i].Year + "</td><td>" +
                result[i].Housetype + "</td><td>" +
                result[i].Cost + "</td><td>" +
                result[i].Service + "</td><td>" +
                result[i].Company + "</td><td>" +
                result[i].BuildingNum + "</td><td>" +
                result[i].HouseNum + "</td>").appendTo('#records_table');
        });
    }
}

function get_community_name() {
    $.ajax({
        type: "get",
        url: appConfig.URL + "/api/community/tips",
        dataType: "json",
        success: function(result) {
            var availableTags = []
            $.each(result.data, function(i, item) {
                availableTags.push(item.Title)
            });
            $(".autocomplete").autocomplete({
                source: availableTags
            });
        }
    });
}