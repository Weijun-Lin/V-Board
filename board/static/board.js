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