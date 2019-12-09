function delete_p()
{
    $("#p1").empty();
    $("#p2").empty();
}

function input_change(content,ulLi)
{
    delete_p()
    $("#ant-input").val(content);
    $("#ant-input").css({'color':'rgba(196, 189, 189, 0.9)'});
    let ulLi_lin = "#" + ulLi;
//    console.log(ulLi);
    $("ul li").removeClass("onclick-style");
    $("ul li").addClass("content_li");
    $(ulLi_lin).removeClass("content_li");
    $(ulLi_lin).addClass("onclick-style");
    if (ulLi == "li1")
    {
        $("#span1").text("缩短网址")
    }
    else if (ulLi == "li2")
    {
        $("#span1").text("还原网址")
    }
    else if (ulLi == "li3")
    {
        $("#span1").text("生成加密")
    }
    
};

function timestamp_display(content,ulLi)
{
    input_change(content,ulLi);
    var time = String(Date.now()).substring(0,10);
    $("#ant-input").val(time);
    $("#p1").append("请输入加密的参数: timestamp url key");
//    console.log(time);
}


function md5_get()
{
    let request_content = $("#ant-input").val();
    let content = "content=" + request_content;
/*
    console.log($("#ant-input").val());
    console.log(content);
 */   
    $.ajax(
        { 
            url: "https://s.guanshizhai.online/md5", 
            type: "POST",
            data: content,
            dataType: "json", 
            success: function(data){
                if (data.code == "0")
                {
                     request_content = "request_content: "  + request_content;
                     md5_value = "md5_value: " + data.token_value;
                /*    console.log(data.code);
                    console.log(data.token_value);
                    console.log(data.request_content);*/
                    delete_p()
                    $("#p1").append(request_content);
                    $("#p2").append(md5_value);
                } 
                else
                {
                    response_content = "response_content: " + data.errormsg;
 
                    delete_p()
                    $("#p1").append(response_content);
                    $("#p2").append(response_content);
 
                /*    console.log(data.code);
                    console.log(data.errormsg);*/
                }
        }});
}

function query_short_url()
{
    let request_shorturl = $("#ant-input").val();
    let content = "shorturl=" + request_shorturl;
/*
    console.log($("#ant-input").val());
    console.log(content);
 */   
    $.ajax(
        { 
            url: "http://s.guanshizhai.online/urlquery", 
            type: "GET",
            data: content,
            dataType: "json", 
            success: function(data){
                if (data.code == "0")
                {
                    shorturl = "request_shorturl: " + request_shorturl;
                    originalurl = "originalurl: " + data.originalurl;
                /*    console.log(data.code);
                    console.log(data.token_value);
                    console.log(data.request_content);*/
                    
                    delete_p()
                    $("#p1").append(shorturl);
                    $("#p2").append(originalurl);
 
                } 
                else
                {
                    shorturl = "request_shorturl: " + request_shorturl;
                    originalurl = "originalurl: " + data.errormsg;
 
//                    response_content = request_shorturl  + " " + data.msg;
//                    response_content = request_shorturl + "not found;";
//                    console.log(response_content)

                    delete_p()
                    $("#p1").append(shorturl);
                    $("#p2").append(originalurl);
 
                /*    console.log(data.code);
                    console.log(data.errormsg);*/
                }
        }});
}

function insert_short_url()
{
    let source_url = $("#ant-input").val();
    $.ajax(
        { 
            url: "http://s.guanshizhai.online/urlinsert", 
            type: "POST",
            data: source_url,
            dataType: "json", 
            success: function(data)
            {
                if (data.code == "0")
                {
                    source_url = "source_url: " + data.source_url;
                    short_url = "short_url: " + data.shorturl;
                    
                    delete_p()
                    $("#p1").append(source_url);
                    $("#p2").append(short_url);
 
                } 
                else
                {
                    source_url = "source_url:  " + source_url;
                    response_content = "response msg:  " + data.errormsg;
                    delete_p()
                    $("#p1").append(source_url);
                    $("#p2").append(response_content);
 
                }
            },
            headers: {
                "Content-Type": "text/plain;charset=UTF-8"
            },
        });
}

function function_selection()
{
    let selsect_content = $(".onclick-style")
    if (selsect_content.length == 0){
        insert_short_url()
    }
    else {
        if (selsect_content[0]['id'] == "li1") {
            insert_short_url()
        } 
        else if (selsect_content[0]['id'] == "li2") {
           query_short_url()
        }
        else if (selsect_content[0]['id'] == "li3") {
            md5_get()
        }
    }
}