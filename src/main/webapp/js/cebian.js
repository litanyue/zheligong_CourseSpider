/* 侧边栏切换形态 */
$(".navbar-side a").click(function(){
    $("body").toggleClass("sidebar-collapse");
    if($("body").hasClass("sidebar-collapse")){
        $(".sidebar > h4").html("博客");
    }else{
        $(".sidebar > h4").html("博客管理系统(四月)");
    }
    return false;
})

$(".sidenav>li>a").click(function(){
    $(this).addClass("hover");
    $(this).next().slideToggle();    
    $(this).parent().siblings().children("a").removeClass("hover").next().slideUp();
    
})