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
        getrentbycommunity()
    }
});

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

function formatDate(date) {
    var day = date.getDate();
    var month = date.getMonth() + 1;
    var year = date.getFullYear();

    return year + '-' + month + '-' + day;
}

function getrentbycommunity() {
    var pastseason = new Date()
    pastseason.setMonth(pastseason.getMonth() - 4)
    var input = $('#community').val();
    var stime = formatDate(pastseason);
    var etime = formatDate(new Date());

    gettablebycommunity(input, stime, etime);
    getgraphbycommunity(input, stime, etime);
}

function gettablebycommunity(input, stime, etime) {
    $.ajax({
        type: "get", //请求方式
        url: appConfig.URL + "/api/rent/info/" + input +
            "?stime=" + stime +
            "&etime=" + etime,
        dataType: "json",
        success: function(result) {
            addRentTable(result.data);
        },

        error: function() {
            $("#alert").html("<div class=\"alert alert-danger text-center\" role=\"alert\" id=\"alert\">服务器开小差啦<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>")
        },
    });
}

function getgraphbycommunity(input, stime, etime) {
    $.ajax({
        type: "get", //请求方式
        url: appConfig.URL + "/api/rent/zone/" + input +
            "?stime=" + stime +
            "&etime=" + etime,
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
            label: '价格',
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

function addRentTable(result) {
    addHeader(result);
    addData(result);

    function addHeader(result) {
        $("#records_table tr").remove();
        $("#table-head tr").remove();
        //$('<tr>').html("<td>搜索结果:" + result.length + "个房源</td>").appendTo('#records_table');
        $('<tr>').html("<th>户型</th><th>面积</th><th>价格</th><th>装修</th><th>供暖</th><th>其他</th>").appendTo('#table-head');
    }

    function addData(result) {
        $.each(result, function(i, item) {
            $('<tr>').html(
                "<td>" +
                result[i].Zone + "</td><td>" +
                result[i].Meters + "</td><td>" +
                result[i].Price + "</td><td>" +
                result[i].Decoration + "</td><td>" +
                result[i].Heating + "</td><td>" +
                result[i].Other + "</td>").appendTo('#records_table');
        });
        $('#dataTable').DataTable();
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