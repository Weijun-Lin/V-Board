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
$('#add_team_desc').keydown(function (e) {
    e.stopPropagation();
})
$("#submit_team_set").click(function () {
    // $("#form_usr_set").submit(); 暂时没有后端处理代码
    $("#add_team_modal").modal('hide');
});
 
//propertychange监听input里面的字符变化,属性改变事件
function updateInputJS() {     
    var team_member_label = document.querySelectorAll('.team_member_label');
    for(var i = 0;i < team_member_label.length;i++) {
        team_member_label[i].addEventListener('input',function(){
            t = this; 
            t.style.width="0px";//让 scrollWidth 获取最小值，达到回缩的效果
            p = window.getComputedStyle(t, null).padding;
            t.style.width=parseInt(t.scrollWidth)+parseInt(p)+"px";
        })
    }
}

// 动态添加成员
$("#add_team_member").click(function () {
    var i =  '<div class="d-flex mr-3 mb-2"> \
                <input class="form-control form-control-sm team_member_label" placeholder="email"> \
                <button type="button ml-3" class="close" aria-label="Close" style="outline:none;"> \
                <span aria-hidden="true">&times;</span> \
                </button>\
             </div>';
    $("#teammates").append(i);
    var last = $("#teammates").find('input').last();    // last为新加入的成员框
    last.focus();
    last.next().css('visibility', 'hidden');    // 关闭按钮默认不可见
    updateInputJS();
    // 失去焦点 如果没有输入则删除
    last.blur(function () {
        if($(this).val().length == 0) {
            $(this).parent().remove();
        }
        $(this).attr('title', $(this).val());
    });
    // 如果输入中回车自动生成下一个
    last.keydown(function(e){
        if(e.which == 13) {
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
    last.next().click(function() {
        $(this).parent().remove();
    })
})

// ------------------------ JS For user_set.html --------------------------------
// 按钮（图片）点击产出文件选择框
$("#submit_usr_set").click(function () {
    $("#userSetModal").modal('hide');
});

$("#button_avatar").click(function () {
    $("#form_change_avatar").find("input").click();
    $("#form_change_avatar").find("input").change(function(){    
        // 点了取消选择文件
        if($(this).val() == '') {
            return;
        }
        var formData = new FormData();
        formData.append('avatar', $(this)[0].files[0]);
        $.ajax({
            type: "POST",
            url: "/home/set_avatar/",
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
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert("上传图片失败")
            }
        });
    })
})