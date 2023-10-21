$(document).ready(function() {
    var baseurl = "http://119.65.155.91:30080";

    function hideSpinner() {
        $('.container').removeClass('blur'); // 흐려진 부분을 원래대로 복원
        $('.loading-spinner').hide();
    }

    function showSpinner() {
        $('.container').addClass('blur'); // 흐려지게 함
        $('.loading-spinner').show();
    }
    $("#addCCTVButton").click(function() {
        showSpinner();
        var cctv_name = $("#cctvName_add").val();
        var rtsp_url = $("#rtspURL_add").val();
        var requestData = {
            "cctv_name": cctv_name,
            "rtsp_url": rtsp_url
        };

        $.ajax({
            type: "POST",
            url: baseurl + "/cctvs",
            data: JSON.stringify(requestData),
            contentType: "application/json",
            success: function(response) {
                var message = cctv_name + " 추가 요청이 정상 처리되었습니다.";
                alert(message);
                window.location.reload();
                hideSpinner(); 
            },
            error: function(xhr, status, error) {
                alert("CCTV 추가 중 오류 발생:\n" + xhr.responseText);
                hideSpinner(); 
            }
        });
    });


    $("#updateCCTVButton").click(function() {
        showSpinner();
        var cctv_name = $("#cctvName_update").val();
        var rtsp_url = $("#rtspURL_update").val();
        var requestData = {
            "cctv_name": cctv_name,
            "rtsp_url": rtsp_url
        };

        $.ajax({
            type: "PUT",
            url: baseurl + "/cctvs/" + cctv_name,
            data: JSON.stringify(requestData),
            contentType: "application/json",
            success: function(response) {
                var message = cctv_name + " 주소 변경 요청이 정상 처리되었습니다.";
                alert(message);
                window.location.reload();
                hideSpinner(); 
            },
            error: function(xhr, status, error) {
                alert("CCTV 주소 변경 중 오류 발생:\n" + xhr.responseText);
                hideSpinner(); 
            }
        });
    });


    $("#deleteCCTVButton").click(function() {
        showSpinner();
        var cctv_name = $("#cctvName_delete").val();

        $.ajax({
            type: "Delete",
            url: baseurl + "/cctvs/" + cctv_name,
            success: function(response) {
                var message = cctv_name + " CCTV 삭제 요청이 정상 처리되었습니다.";
                alert(message);
                window.location.reload();
                hideSpinner(); 
            },
            error: function(xhr, status, error) {
                alert("CCTV 삭제 중 오류 발생:\n" + xhr.responseText);
                hideSpinner(); 
            }
        });
    });

    
    $("#getCCTVButton").click(function() {
        showSpinner();

        $.ajax({
            type: "GET",
            url: baseurl + "/cctvs/",
            dataType: "json",
            success: function(response) {
                hideSpinner();
                displayCCTVInfo(response);
            },
            error: function(xhr, status, error) {
                alert("CCTV 조회 중 오류 발생:\n" + xhr.responseText);
                hideSpinner();
            }
        });
    });

    // CCTV 정보를 표시하는 함수
    function displayCCTVInfo(data) {
        var cctvDataDiv = $("#cctvData");
        cctvDataDiv.empty();  // 이전 데이터를 비우고 새로운 데이터 추가

        var table = "<table><thead><tr><th>CCTV</th><th>READY</th><th>RTSP URL</th></tr></thead><tbody>";

        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                var cctvInfo = data[key];
                var ready = cctvInfo.ready;
                var rtspUrl = cctvInfo.rtsp_url;

                table += "<tr><td>" + key + "</td><td>" + ready + "</td><td>" + rtspUrl + "</td></tr>";
            }
        }

        table += "</tbody></table>";
        cctvDataDiv.append(table);
    }





    $("#getMVCCTVButton").click(function() {
        showSpinner();

        $.ajax({
            type: "GET",
            url: baseurl + "/cctvs/",
            dataType: "json",
            success: function(response) {
                hideSpinner();
                displayCCTV(response);
            },
            error: function(xhr, status, error) {
                alert("CCTV 조회 중 오류 발생:\n" + xhr.responseText);
                hideSpinner();
            }
        });
    });

    // CCTV 정보를 표시하는 함수
    function displayCCTV(data) {
        var cctvMV = $("#cctvMV");
        cctvMV.empty();  // 이전 데이터를 비우고 새로운 데이터 추가

        var table = "<table><thead><tr><th>CCTV</th><th>영상</th><th>위험</th></tr></thead><tbody>";

        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                var iframe = '<div style="width:576px; height:324px; overflow:hidden;"><iframe id = "videoFrame" src="'+baseurl +"/video/"+ key + '" width="1920" height="1080" frameborder="0"></iframe></div>';
                var statusCircle = '<div id="' + key + '-status" class="status-circle"></div>';
                table += "<tr><td>" + key + "</td><td>" + iframe + "</td><td>" + statusCircle + "</td></tr>";
            }
        }

        table += "</tbody></table>";
        cctvMV.append(table);
    }

    
})

var baseurl = "http://119.65.155.91:30080";
function alertGET(){
    $.ajax({
        type: "GET",
        url: baseurl + "/cctvs/",
        dataType: "json",
        success: function(response) {
            updateCCTVStatus(response);
        },
        error: function(xhr, status, error) {
            alert("CCTV 조회 중 오류 발생:\n" + xhr.responseText);
        }
    });
}

function updateCCTVStatus(data) {
    for (var key in data) {
        if (data.hasOwnProperty(key)) {
            (function(cctvKey){
                $.ajax({
                    type: "GET",
                    url: "http://119.65.155.91:30080/Alert/" + cctvKey,
                    dataType: "json",
                    success: function(response) {
                        console.log(cctvKey)
                        var statusElement = $("#" + cctvKey + "-status");

                        // API 응답이 "True"일 경우 빨간색, "False"일 경우 초록색으로 설정
                        if (response.Alert === 'True') {
                            statusElement.css("background-color", "red");
                            console.log(response.Alert)
                        } else {
                            statusElement.css("background-color", "green");
                            console.log(response.Alert)
                        }
                    },
                    error: function(xhr, status, error) {
                        alert("압사위험 조회 중 오류 발생:" + xhr.responseText);
                    }
                });
            })(key);
        }
    }
}

