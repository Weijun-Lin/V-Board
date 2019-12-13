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
    url = "/board/get_info/board/?id="+$("#board_top").attr("data-target")+"&kind="+$("#board_top").attr("data-type");    
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

// -------------------------------- 修改列表 & 卡片标题 -------------------------------------
// 相同名字不需要重传
var pirorListName;
$(".list_title").focus(function (e) {
    pirorListName = $(this).val();
})
$(".list_title").blur(function () {
    $this = $(this);
    if($(this).val() != pirorListName) {
        data = {
            kind : $("#board_top").attr("data-type"),
            lid : $(this).parents(".list").attr("data-target"),
            bid : $("#board_top").attr("data-target"),
            name: $(this).val(),
        };
        $.ajax({
            type: "POST",
            url: "/board/set_list_name/",
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
                // 状态码 status: 0 success ; 1 empty title; 2 illegal title; 3 too long
                if (status == 0) {
                    // do nothing
                } else if (status == 1) {
                    alert("列表名称不能为空");
                } else if (status == 2) {
                    alert("列表名称重复");
                } else if (status == 3) {
                    alert("列表名称过长");
                }
                if(status != 0) {
                    console.log(pirorListName)
                    console.log($this.val())
                    $this.val(pirorListName);
                }
            },
            error: function () {
                alert("某些原因。。 修改失败 sorry");
            }
        });
    }
})

var pirorCardName;
$(".list_card").find("input").focus(function (e) {
    pirorCardName = $(this).val();
})
$(".list_card").find("input").blur(function () {
    $this = $(this);
    if($(this).val() != pirorCardName) {
        data = {
            kind : $("#board_top").attr("data-type"),
            lid : $(this).parents(".list").attr("data-target"),
            cid : $this.parent().attr("data-target"),
            name: $(this).val(),
        };
        console.log(data);
        $.ajax({
            type: "POST",
            url: "/board/set_card_name/",
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
                // 状态码 status: 0 success ; 1 empty title; 2 illegal title; 3 too long
                if (status == 0) {
                    // do nothing
                } else if (status == 1) {
                    alert("卡片名称不能为空");
                } else if (status == 2) {
                    alert("卡片名称重复");
                } else if (status == 3) {
                    alert("卡片名称过长");
                }
                if(status != 0) {
                    $this.val(pirorCardName);
                }
            },
            error: function () {
                alert("某些原因。。 修改失败 sorry");
            }
        });
    }
})

// ------------------------------ 添加卡片 或者 列表 -------------------------------------
$("#add_list").find("button").click(function () {
    data = {
        kind : $("#board_top").attr("data-type"),
        bid : $("#board_top").attr("data-target"),
        name: $("#add_list").find("input").val(),
    };
    console.log(data);
    $.ajax({
        type: "POST",
        url: "/board/add/list/",
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
            // 状态码 status: 0 success ; 1 empty title; 2 illegal title; 3 too long
            if (status == 0) {
                // 以后可以改为动态绑定 此时仅为刷新
                window.location.reload();
            } else if (status == 1) {
                alert("列表名称不能为空");
            } else if (status == 2) {
                alert("列表名称重复");
            } else if (status == 3) {
                alert("列表名称过长");
            }
        },
        error: function () {
            alert("某些原因。。 添加失败 sorry");
        }
    });
})

$(".add_card_btn").click(function () {
    $("#add_card").attr("data-target", $(this).parents(".list").attr("data-target"));
})

$("#add_card").find("button").click(function () {
    data = {
        kind : $("#board_top").attr("data-type"),
        lid : $("#add_card").attr("data-target"),
        name: $("#add_card").find("input").val(),
    };
    $.ajax({
        type: "POST",
        url: "/board/add/card/",
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
            // 状态码 status: 0 success ; 1 empty title; 2 illegal title; 3 too long
            if (status == 0) {
                // 以后可以改为动态绑定 此时仅为刷新
                window.location.reload();
            } else if (status == 1) {
                alert("卡片名称不能为空");
            } else if (status == 2) {
                alert("卡片名称重复");
            } else if (status == 3) {
                alert("卡片名称过长");
            }
        },
        error: function () {
            alert("某些原因。。 添加失败 sorry");
        }
    });    
})

// ------------------------- 删除列表 ----------------------------------
$(".delete_list").click(function () {
    // 删除之前提醒用户
    list = $(this).parents(".list");
    console.log(list)
    isdelete = confirm("删除列表: " + list.find("input").val());
    if(!isdelete) {
        return;
    }
    url = "/delete/list/?id="+list.attr("data-target")+"&kind="+$("#board_top").attr("data-type");
    $.get(url,
        function () {
            list.parent().remove();
        }
    );    
})


// ------------------------ 卡片模态框 -------------------------------------------------------

// 更新模态框数据
$(".btn_card_modal").click(function () {
    cid = $(this).parents(".list_card").attr("data-target");
    kind = $("#board_top").attr("data-type");
    url = "/board/get_info/card/"+"?id="+cid+"&kind="+kind;
    $.get(url, function (data) {
        console.log(data);
        card_modal = $("#card_modal");
        card_modal.attr("data-target", data.CID);
        card_modal.attr("data-parent", data.LID);
        $("#card_modal_title").val(data.name);
        $("#card_modal_desc").text(data.description);
    })
})

// -------------- 删除卡片 ----------------
$("#delete_card").click(function () {
    // 删除之前提醒用户
    isdelete = confirm("删除列表: " + $("#card_modal_title").val());
    if(!isdelete) {
        return;
    }
    cid = $("#card_modal").attr("data-target");
    url = "/delete/card/?id="+cid+"&kind="+$("#board_top").attr("data-type");
    $.get(url,
        function () {
            $("#card_modal").modal("hide");
            $(`.list_card[data-target='${cid}']`).remove();
        }
    );        
})

// ----------------- 模态框内修改标题
$("#card_modal_title").focus(function (e) {
    pirorCardName = $(this).val();
})
$("#card_modal_title").blur(function () {
    $this = $(this);
    if($(this).val() != pirorCardName) {
        data = {
            kind : $("#board_top").attr("data-type"),
            lid : $("#card_modal").attr("data-parent"),
            cid : $("#card_modal").attr("data-target"),
            name: $(this).val(),
        };
        console.log(data);
        $.ajax({
            type: "POST",
            url: "/board/set_card_name/",
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
                // 状态码 status: 0 success ; 1 empty title; 2 illegal title; 3 too long
                if (status == 0) {
                    $(`.list_card[data-target='${data.cid}']`).find("input").val(data.name);
                } else if (status == 1) {
                    alert("卡片名称不能为空");
                } else if (status == 2) {
                    alert("卡片名称重复");
                } else if (status == 3) {
                    alert("卡片名称过长");
                }
                if(status != 0) {
                    $this.val(pirorCardName);
                }
            },
            error: function () {
                alert("某些原因。。 修改失败 sorry");
            }
        });
    }
})

// ------------- 修改卡片描述 ---------------
$("#card_modal_desc").blur(function () {
    data = {
        kind : $("#board_top").attr("data-type"),
        cid : $("#card_modal").attr("data-target"),
        desc: $(this).val(),
    };
    console.log(data);
    $.ajax({
        type: "POST",
        url: "/board/set_card_desc/",
        dataType: "json",
        data: JSON.stringify(data),
        beforeSend: function (xhr, settings) {
            var csrftoken = getCookie('csrftoken');
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (response) {
            
        },
        error: function () {
            alert("某些原因。。 修改失败 sorry");
        }
    });    
})