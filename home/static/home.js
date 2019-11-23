$("button.icon-star.unstarred").hide().addClass("unstarred");

// 未收藏的需要隐藏
$(".v_card").mouseenter(function () {
    $(this).find("button.icon-star").show();
}).mouseleave(function () {
    $(this).find("button.unstarred").hide();
});

// 点击后的事件 根据服务器返回值修改
$(".v_card").find("button.icon-star").click(function () {
    if($(this).attr("class").indexOf("unstarred") != -1) {
        $(this).removeClass("unstarred");
        $(this).addClass("starred");
    }
    else {
        $(this).removeClass("starred");
        $(this).addClass("unstarred");
    }
});
