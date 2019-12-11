// 展开所有的列表 因为它默认是关闭的
$(".list_collapse").collapse('show')

// 点击折叠列表全部折叠
var collapse_lists = 1;
$("#collapse_lists").click(function () {
    if(collapse_lists == 1) {
        $(".list_collapse").collapse('hide');
    }
    else {
        $(".list_collapse").collapse('show');
    }
    collapse_lists = -collapse_lists;
})

// ------------------------ JS For board_info_set.html --------------------------------

// 上传看板名字，看板介绍
var submit_board_info = true;
$("#submit_board_info").click(function () {
    data = {
        bid : $("#board_top").attr("data-target"),
        kind : $("#board_top").attr("data-type"),
        board_name: $("#board_info_set_name").val(),
        desc: $("#board_info_set_desc").val(),
    };
    if(!submit_board_info) {
        return;
    }
    submit_board_info = false;
    $.ajax({
        type: "POST",
        url: "/board/set_board_info/",
        dataType: "json",
        data: JSON.stringify(data),
        beforeSend: function (xhr, settings) {
            var csrftoken = getCookie('csrftoken');
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (response) {
            status = response.status;
            submit_board_info = true;
            // 状态码 status: 0 success ; 1 empty title; 2 illegal title; 3 too long
            if (status == 0) {
                $(".board_title").text(data.board_name);
                $("#board_info_set").modal("hide");
            } else if (status == 1) {
                alert("看板名称不能为空");
            } else if (status == 2) {
                alert("看板名称重复");
            } else if (status == 3) {
                alert("看板名称过长");
            }
        },
        error: function () {
            submit_board_info = true;
            alert("某些原因。。 修改失败 sorry");
        }
    });
})

// 用户修改了但是没有上传，需要恢复到原始状态
// 监听模态框隐藏事件
$(function () {
    url = "/board/get_board_info/?id="+$("#board_top").attr("data-target")+"&kind="+$("#board_top").attr("data-type");    
    $("#board_info_set").on('hidden.bs.modal', function () {
        $.get(url, function (data) {
            $("#board_info_set_name").val(data.name);
            $("#board_info_set_desc").val(data.description);
        })
    })
});

// ---------------------------------------- 删除看板 ------------------------------------
// 删除之后重定向至首页
$("#delete_board").click(function () {
    // 删除之前提醒用户
    isdelete = confirm("删除看板: " + $(".board_title").text());
    if(!isdelete) {
        return;
    }
    url = "/delete/board/?id="+$("#board_top").attr("data-target")+"&kind="+$("#board_top").attr("data-type");
    $.get(url,
        function () {
            window.location.href = "/home/";
        }
    );
})
