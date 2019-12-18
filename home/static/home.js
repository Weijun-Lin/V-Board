$("button.icon-star.unstarred").hide().addClass("unstarred");
$("button.icon-trash").hide();

// 未收藏的需要隐藏
$(".v_card").mouseenter(function () {
    $(this).find("button.icon-star").show();
    $(this).find("button.icon-trash").show();
}).mouseleave(function () {
    $(this).find("button.unstarred").hide();
    $(this).find("button.icon-trash").hide();
});

// 点击后的事件 根据服务器返回值修改
$(".v_card").find("button.icon-star").click(function (event) {
    if($(this).attr("class").indexOf("unstarred") != -1) {
        $(this).removeClass("unstarred");
        $(this).addClass("starred");
    }
    else {
        $(this).removeClass("starred");
        $(this).addClass("unstarred");
    }
    event.stopPropagation();
});

// 新建看板div的点击事件 相当与 打开添加看板并且设置团队类别
// 个人看板
$(".add_personal_board").click(function () {
    $("#add_board").modal("show");
    // 个人对应的编号是 0
    $("#add_board").find("select").val(0);
})

$(".add_team_board").click(function () {
    $("#add_board").modal("show");
    $("#add_board").find("select").val($(this).attr("data-target"));
})

// 给div添加点击跳转
$(".v_card[data-type]").click(function () {
    window.location.href = "/board/?id="+$(this).attr("data-target")+"&kind="+$(this).attr("data-type");
})

// 删除一个看板
$(".v_card").find("button.icon-trash").click(function (event) {
    event.stopPropagation();    // 阻止冒泡 防止触发div的点击事件
    // 删除之前提醒用户
    isdelete = confirm("删除看板: " + $(this).parents(".v_card").find("h6").text())
    if(!isdelete) {
        return;
    }
    v_card = $(this).parents(".v_card");
    url = "/delete/board/?id="+$(this).parents(".v_card").attr("data-target")+"&kind="+$(this).parents(".v_card").attr("data-type");
    $.get(url,
        function () {
            v_card.remove();
        }
    );
})

// 删除一个团队 其下看板全部 gg
$(".home_delete_team").click(function () {
    // 删除之前提醒用户
    team_block = $(this).parents(".team_block")
    isdelete = confirm("删除团队: " + team_block.attr("data-name"))
    if(!isdelete) {
        return;
    }
    url = "/delete/team/?id="+team_block.attr("data-target")+"&kind=1";
    $.get(url,
        function () {
            team_block.remove();
        }
    );
})

$(".home_invite").click(function () {
    team_block = $(this).parents(".team_block");
    $("#invite_teammates").attr("data-target", team_block.attr("data-target"));
})

$("#invite_teammates").find("button").click(function (event) {
    event.stopPropagation();    // 阻止冒泡 防止触发div的点击事件
    url = "/invite/?tid="+$("#invite_teammates").attr("data-target")+"&email="+$("#invite_teammates").find("input").val();
    $.get(url,
        function (data) {
            status = data.status
            if(status == 0) {
                alert("邀请成功");
                window.location.reload();
            }
            else if (status == 1) {
                alert("请输入邮箱");
            }
            else if (status == 2) {
                alert(data.email+" 成员已存在");
            }
            else if (status == 3) {
                alert(data.email+" 邮箱不存在");
            }
        }
    );
})

// 鼠标移入显示
$(".teammate_list").find("button.icon-close").hide();
$(".teammate_list").mouseenter(function () {
    $(this).find("button.icon-close").show();
}).mouseleave(function () {
    $(this).find("button.icon-close").hide();
});

// 点击删除团队成员 只能创建者执行
$(".teammate_list").find("button.icon-close").click(function () {
    teammate_list = $(this).parents(".teammate_list");
    isdelete = confirm("删除成员: " + teammate_list.find("p").text());
    if(!isdelete) {
        return;
    }

    uid = teammate_list.find("p").attr("data-target");
    tid = teammate_list.parents(".team_block").attr("data-target");
    url = "/delete/teammate/?uid="+uid+"&tid="+tid+"&kind=1";
    $.get(url,
        function () {
            window.location.reload();
        }
    );
})

$(".home_rename_team").click(function () {
    team_block = $(this).parents(".team_block");
    $("#change_team_name").attr("data-target", team_block.attr("data-target"));
})

$("#change_team_name").find("button").click(function () {
    event.stopPropagation();    // 阻止冒泡 防止触发div的点击事件
    url = "/home/changeTeamName/?tid="+$("#change_team_name").attr("data-target")+"&name="+$("#change_team_name").find("input").val();
    $.get(url,
        function (data) {
            status = data.status
            if(status == 0) {
                alert("更改成功");
                window.location.reload();
            }
            else if (status == 1) {
                alert("名称不能为空");
            }
            else if (status == 2) {
                alert(data.name+" 团队已存在");
            }
        }
    );
})