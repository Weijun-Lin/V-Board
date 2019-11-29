// ----------------------------- CSRF For Ajax -------------------------------
// reference http://www.codingsoho.com/zh/blog/django-csrf/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// ---------------------------------JS For add_team.html-------------------------------------

// 禁止事件冒泡 否则不能回车 表单自动监听回车发送事件。。。
$('#add_team_desc').keydown(function (e) {
    e.stopPropagation();
})

// 点击上传
$("#submit_team_set").click(function () {
    data = {
        name: $("#add_team_nick_name").val(),
        desc: $("#add_team_desc").val(),
        member: [],
    }
    // 循环添加成员
    members = $("#teammates").find("input");
    for(i = 0;i < members.length;i++) {
        data.member.push(members[i].value);
    }
    $.ajax({
        type: "POST",
        url: "/add_team/",
        dataType: "json",
        data: JSON.stringify(data),
        beforeSend: function (xhr, settings) {
            var csrftoken = getCookie('csrftoken');
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) {
            console.log(data);
            status = data.status;
            if (status == 0) {

            } else if (status == 1) {

            } else if (status == 2) {

            } else if (status == 3) {

            } else if (status == 4) {

            }
        },
        error: function () {
            alert("添加看板失败");
        }
    });
});

//propertychange监听input里面的字符变化,属性改变事件 压缩input宽度刚好适应文本内容
function updateInputJS() {
    var team_member_label = document.querySelectorAll('.team_member_label');
    for (var i = 0; i < team_member_label.length; i++) {
        team_member_label[i].addEventListener('input', function () {
            t = this;
            t.style.width = "0px"; //让 scrollWidth 获取最小值，达到回缩的效果
            p = window.getComputedStyle(t, null).padding;
            t.style.width = parseInt(t.scrollWidth) + parseInt(p) + "px";
        })
    }
}

// 动态添加成员
$("#add_team_member").click(function () {
    var i = '<div class="d-flex mr-3 mb-2"> \
                <input class="form-control form-control-sm team_member_label" placeholder="email"> \
                <button type="button ml-3" class="close" aria-label="Close" style="outline:none;"> \
                <span aria-hidden="true">&times;</span> \
                </button>\
             </div>';
    $("#teammates").append(i);
    var last = $("#teammates").find('input').last(); // last为新加入的成员框
    last.focus();
    last.next().css('visibility', 'hidden'); // 关闭按钮默认不可见
    updateInputJS();
    // 失去焦点 如果没有输入则删除
    last.blur(function () {
        if ($(this).val().length == 0) {
            $(this).parent().remove();
        }
        $(this).attr('title', $(this).val());
    });
    // 如果输入中回车自动生成下一个
    last.keydown(function (e) {
        if (e.which == 13) {
            $('#add_team_member').focus();
            $('#add_team_member').click();
        }
    })
    // 产生移入显示关闭按钮 移出消除关闭按钮
    last.parent().mouseenter(function () {
        $(this).find('button').css('visibility', 'visible');
    }).mouseleave(function () {
        $(this).find('button').css('visibility', 'hidden');
    })
    // 关闭按钮事件
    last.next().click(function () {
        $(this).parent().remove();
    })
})

// ------------------------ JS For user_set.html --------------------------------

// 上传图片 按钮（图片）点击产出文件选择框
$("#button_avatar").click(function () {
    $("#form_change_avatar").find("input").click();
    $("#form_change_avatar").find("input").change(function () {
        // 点了取消选择文件
        if ($(this).val() == '') {
            return;
        }
        var formData = new FormData();
        formData.append('avatar', $(this)[0].files[0]);
        $.ajax({
            type: "POST",
            url: "/set_avatar/",
            data: formData,
            contentType: false,
            clearForm: true,
            processData: false,
            dataType: "text",
            beforeSend: function (xhr, settings) {
                var csrftoken = getCookie('csrftoken');
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function (data, status) {
                $(".avatar").attr('src', data);
                // 重新置为空字符串
                $(this).val('');
            },
            error: function () {
                alert("上传图片失败")
            }
        });
    })
})

// 上传自我介绍 昵称 密码等
$("#submit_usr_set").click(function () {
    data = {
        nickname: $("#user_set_nick_name").val(),
        desc: $("#use_set_desc").val(),
        srcpass: $("#user_set_srcpass").val(),
        newpass: $("#user_set_newpass").val(),
        repass: $("#user_set_repass").val(),
    };

    $.ajax({
        type: "POST",
        url: "/user_set/",
        dataType: "json",
        data: JSON.stringify(data),
        beforeSend: function (xhr, settings) {
            var csrftoken = getCookie('csrftoken');
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) {
            status = data.status;
            if (status == 0) {
                alert("密码修改成功 请重新登陆");
                $("#logout")[0].click(); // 登出重新登陆
            } else if (status == 1) {
                alert("密码错误 请重新输入原密码");
            } else if (status == 2) {
                alert("非法密码 请确认新密码");
            } else if (status == 3) {
                alert("密码不一致 请重新输入");
            } else if (status == 4) {
                // 不是修改密码
            }
        },
        error: function () {
            alert("创建失败");
        }
    });

})

// 用户修改了但是没有上传，需要恢复到原始状态
// 监听模态框隐藏事件
$(function () {
    $("#userSetModal").on('hidden.bs.modal', function () {
        $.get("/get_usrinfo/", function (data) {
            console.log(data.description)
            $("#user_set_nick_name").val(data.name);
            $("#use_set_desc").val(data.description);
        })
    })
});


// ------------------------------------- JS For Add_Board.html ------------------------
$("#submit_board").click(function () {
    if ($("#add_board").find("[name=title]").val() == '') {
        alert("标题不能为空");
        return
    }
    // 获取数据 标题 & 类型 & 是否公开
    data = {
        title: $("#add_board").find("[name=title]").val(),
        type: $("#add_board").find("select").val(),
        ispublic: $("#add_board_Switch").prop("checked")
    };

    $.ajax({
        type: "POST",
        url: "/add_board/",
        dataType: "text",
        data: JSON.stringify(data),
        clearForm: true,
        beforeSend: function (xhr, settings) {
            var csrftoken = getCookie('csrftoken');
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) {
            alert("上传成功");
            // 清空表单
            $("#form_add_board")[0].reset();

        },
        error: function () {
            alert("创建失败");
        }
    });
})