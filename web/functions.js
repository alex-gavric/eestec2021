String.prototype.format = function () {
    var a = this;
    for (var k in arguments) {
        a = a.replace(new RegExp("\\{" + k + "\\}", 'g'), arguments[k]);
    }
    return a
}

let modules = []

  $(document).ready(function () {

    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/list",
        processData: false,
        contentType: false,
        cache: false,
        timeout: 80000000,
        success: function (data) {
            modules = data['modules'];

            let htmlData = "";
            let element = '<p class="mb-4" >{0}</p>';

            modules.forEach(function (module) {
                console.log(module);
                htmlData += element.format(module);
            });
            
            $("#divLists").html(htmlData);
            console.log("SUCCESS : ", data);
            $("#searchButton").prop("disabled", false);

        },
        error: function (e) {

            $("#serverResponse").text(e.responseText);
            console.log("ERROR : ", e);
            $("#searchButton").prop("disabled", false);

        }
    });


    $("#searchButton").click(function (event) {
        event.preventDefault();
        var form = $('#inputForm')[0];
        var data = new FormData(form);
        var queryString = $("#queryStringInput").val();
        console.log(queryString)
        $("#searchButton").prop("disabled", true);
        data.append("queryString", queryString)
        $.ajax({
            type: "POST",
            enctype: 'multipart/form-data',
            url: "http://127.0.0.1:5000/search",
            data: data,
            processData: false,
            contentType: false,
            cache: false,
            timeout: 80000000,
            success: function (data) {

            let modules = data['modules']; 
            $("#serverResponse").text("Number of detections (RISK FACTOR):" + data['risk']);  
            let htmlData = "";
            let element = '<form action="#" class="bg-white rounded pb_form_v1">\
              <h2 class="mb-6 mt-0 "><b>{0}</b></h2>\
              <h4 class="mb-4 mt-0 ">{1}</h4>\
              </form>\
            <br/>';

                modules.forEach(function (module) {
                    console.log(module['name']);
                    htmlData += element.format(module['name'], module['message']);
                });
                
                $("#divLists").html(htmlData);

                console.log("SUCCESS : ", data);
                $("#searchButton").prop("disabled", false);
 
            },
            error: function (e) {
 
                $("#serverResponse").text(e.responseText);
                console.log("ERROR : ", e);
                $("#searchButton").prop("disabled", false);
 
            }
        });
    });
});
