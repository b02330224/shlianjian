$(document).ready(function() {
    $(function() {
        //$("#mainNav").load("navbar.html");
        $("#footer").load("footer.html");
        get_community_name();
    });

    var url = new URL(window.location.href);
    var community = url.searchParams.get("community");
    if (community) {
        $('#community').val(community);
        gethousebycommunity();
    }
});

function formatDate(date) {
    var day = date.getDate();
    var month = date.getMonth() + 1;
    var year = date.getFullYear();

    return year + '-' + month + '-' + day;
}

function gethousebycommunity() {
    var input = $('#community').val();
    var stime = new Date();
    stime.setDate(stime.getDate() - 1);

    gettablebycommunity(input, stime);
    getgraphbycommunity(input, stime);
}

function gettablebycommunity(input, stime) {
    $.ajax({
        type: "get", //请求方式
        url: appConfig.URL + "/api/house/info/" + input +
            "?stime=" + formatDate(stime),
        dataType: "json",
        success: function(result) {
            //addGraph(result.data);
            console.log("get /api/house/info/ success!")
            addHouseTable(result.data);
        },
        error: function(e) {

         console.log('error')
       }
    });

    function addGraph(data) {
        var x = [];
        var y = [];

        for (var i in data) {
            x.push(data[i].Housetype + data[i].Decoration);
            y.push(data[i].UnitPrice);
        }

        var chartdata = {
            labels: x,
            datasets: [{
                label: '均价',
                backgroundColor: 'rgba(151,187,205,0.5)',
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
            type: 'bar',
            data: chartdata
        });
    }
}

function addHouseTable(result) {
    console.log('addHouseTable');
    addHeader(result);
    addData(result);

    function addHeader(result) {
        $("#records_table tr").remove();
        $("#table-head tr").remove();
        //$('<tr>').html("<td>搜索结果:" + result.length + "个房源</td>").appendTo('#records_table');
        $('<tr>').html("<th>名称</th><th>单价</th><th>总价</th><th>户型</th><th>面积</th><th>楼层</th><th>朝向</th><th>装修</th><th>其他</th>").appendTo('#table-head');
    }

    function addData(result) {
        console.log('result',result);
        if ($('#dataTable').hasClass('dataTable')) {
            dttable = $('#dataTable').dataTable();
            dttable.fnClearTable(); //清空一下table
            dttable.fnDestroy(); //还原初始化了的datatable
        }
        
        $.each(result, function(i, item) {
            $('<tr>').html(

                "<td><a href=\"" + result[i].Link + "\"target=\"_blank\">" + result[i].Title + "</a></td><td>" +
                result[i].UnitPrice + "</td><td>" +
                result[i].TotalPrice + "</td><td>" +
                result[i].Housetype + "</td><td>" +
                result[i].Square + "</td><td>" +
                result[i].Years + "</td><td>" +
                result[i].Direction + "</td><td>" +
                result[i].Decoration + "</td><td>" +
                result[i].Taxtype + "</td>").appendTo('#records_table');
        });
        $('#dataTable').DataTable();
    }
}

function getgraphbycommunity(input, stime) {
    $.ajax({
        type: "get", //请求方式
        url: appConfig.URL + "/api/house/type/" + input +
            "?stime=" + formatDate(stime),
        dataType: "json",
        success: function(result) {
            addGraph(result.data);
        },

        error: function() {
            $("#alert").html("<div class=\"alert alert-danger text-center\" role=\"alert\" id=\"alert\">服务器开小差啦<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>")
        },
    });
}

function addGraph(data) {
    var x = [];
    var y = [];

    for (var i in data) {
        x.push(data[i].Zone);
        y.push(data[i].Price);
    }

    var chartdata = {
        labels: x,
        datasets: [{
            label: '均价',
            backgroundColor: 'rgba(2,117,216,1)',
            borderColor: 'rgba(2,117,216,1)',
            hoverBackgroundColor: 'rgba(2,117,216,1)',
            hoverBorderColor: 'rgba(2,117,216,1)',
            data: y
        }]
    };

    var chartOptions = {
        scales: {
            yAxes: [{
                display: true,
                ticks: {
                    suggestedMin: 0, // minimum will be 0, unless there is a lower value.
                }
            }]
        }
    };

    $('#mycanvas').remove();
    $('#chart-container').append('<canvas id="mycanvas"></canvas>');

    var ctx = $("#mycanvas");

    var barGraph = new Chart(ctx, {
        type: 'bar',
        data: chartdata,
        options: chartOptions,
    });
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