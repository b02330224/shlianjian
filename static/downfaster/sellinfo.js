$(document).ready(function() {
    $(function() {
        //$("#mainNav").load("navbar.html");
        $("#footer").load("footer.html");
    });
    document.getElementById('etime').valueAsDate = new Date();
    get_community_name();

    var url = new URL(window.location.href);
    var community = url.searchParams.get("community");
    if (community) {
        $('#community').val(community);
        getsellbycommunity();
    }
});

$('#x_value').on('change', function() {
    var optionSelected = $("option:selected", this);
    var valueSelected = this.value;
    if (valueSelected == 'Dealdate') {
        $("#interval").show();
        $("#intervallabel").show();
    } else {
        $("#interval").hide();
        $("#intervallabel").hide();
    }
});

function getsellbycommunity() {
    var input = $('#community').val();
    var stime = $('#stime').val();
    var etime = $('#etime').val();
    var x_key = $('#x_value').val();
    var y_key = $('#y_value').val();
    var graphtype = $('#type').val();
    var interval = $('#interval').val();
    if ($('input[type="checkbox"]').is(":checked")) {
        var order = 'desc';
    } else {
        var order = 'asc';
    }

    $.ajax({
        type: "get", //请求方式
        url: appConfig.URL + "/api/sell/info/" + input +
            "?stime=" + stime +
            "&etime=" + etime +
            "&sort=" + x_key +
            "&order=" + order, //地址，就是json文件的请求路径
        dataType: "json", //数据类型可以为 text xml json  script  jsonp
        success: function(result) { //返回的参数就是 action里面所有的有get和set方法的参数
            if (result.data.length == 0) {
                $("#alert").html("<div class=\"alert alert-danger text-center\" role=\"alert\" id=\"alert\">不存在该小区<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>")
            } else {
                addGraph(result.data, x_key, y_key, graphtype, input, interval);
                addSellTable(result.data);
            }
        },

        error: function() {
            $("#alert").html("<div class=\"alert alert-danger text-center\" role=\"alert\" id=\"alert\">服务器开小差啦<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>")
        }
    });

}

function addGraph(data, x_key, y_key, graphtype, input, interval) {
    var x = [];
    var y = [];

    for (var i in data) {
        x.push(data[i][x_key]);
        y.push(data[i][y_key]);
    }

    var chartdata = {
        labels: x,
        datasets: [{
            label: input,
            backgroundColor: 'rgba(2,117,216,1)',
            borderColor: 'rgba(2,117,216,1)',
            hoverBackgroundColor: 'rgba(2,117,216,1)',
            hoverBorderColor: 'rgba(2,117,216,1)',
            data: y
        }]
    };
    if (x_key == "Dealdate") {
        var chartOptions = {
            scales: {
                xAxes: [{
                    type: "time",
                    barThickness: 6,
                    time: {
                        unit: 'month',
                        unitStepSize: interval,
                        round: 'month',
                        tooltipFormat: "MMM D YYYY",
                        displayFormats: {
                            hour: 'MMM D YYYY'
                        }
                    }
                }],
            }
        };
    } else {
        var chartOptions = {}
    }


    $('#mycanvas').remove();
    $('#chart-container').append('<canvas id="mycanvas"></canvas>');

    var ctx = $("#mycanvas");

    var barGraph = new Chart(ctx, {
        type: graphtype,
        data: chartdata,
        options: chartOptions
    });
}

function addSellTable(result) {
    addHeader(result);
    addData(result);

    function addHeader(result) {
        $("#records_table tr").remove();
        $("#table-head tr").remove();
        //$('<tr>').html("<td>搜索结果:" + result.length + "套房源</td>").appendTo('.table-bordered');
        $('<tr>').html("<th>房源</th><th>面积</th><th>均价</th><th>总价</th><th>成交日期</th><th>年代</th><th>户型</th><th>朝向</th><th>楼层</th><th>装修</th><th>来源</th>").appendTo('#table-head');
    }

    function addData(result) {
        if ($('#dataTable').hasClass('dataTable')) {
            dttable = $('#dataTable').dataTable();
            dttable.fnClearTable(); //清空一下table
            dttable.fnDestroy(); //还原初始化了的datatable
        }
        $.each(result, function(i, item) {
            $('<tr>').html(
                "<td>" + result[i].Title + "</td><td>" +
                result[i].Square + "</td><td>" +
                result[i].UnitPrice + "</td><td>" +
                result[i].TotalPrice + "</td><td>" +
                result[i].Dealdate + "</td><td>" +
                result[i].Years + "</td><td>" +
                result[i].Housetype + "</td><td>" +
                result[i].Direction + "</td><td>" +
                result[i].Floor + "</td><td>" +
                result[i].Status + "</td><td>" +
                result[i].Source + "</td>").appendTo('#records_table');
        });
        $('#dataTable').DataTable({"order": [[ 4, "desc" ]]});
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