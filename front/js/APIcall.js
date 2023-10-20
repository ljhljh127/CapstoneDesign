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
});
