function showlentime() {
    var from = new Date("2018-12-02 20:40:00");
    from = from.getTime();
    var now = new Date();
    now = now.getTime();
    var lentime = new Date(now - from);
    var dayDiff = Math.floor(lentime / (24 * 3600 * 1000));//计算出相差天数
    var leave1=lentime%(24*3600*1000)    //计算天数后剩余的毫秒数
    var hours=Math.floor(leave1/(3600*1000))//计算出小时数
    //计算相差分钟数
    var leave2=leave1%(3600*1000)    //计算小时数后剩余的毫秒数
    var minutes=Math.floor(leave2/(60*1000))//计算相差分钟数
    //计算相差秒数
    var leave3=leave2%(60*1000)      //计算分钟数后剩余的毫秒数
    var seconds=Math.round(leave3/1000)

    document.getElementById("lengthtime").innerHTML = dayDiff + "天"+ hours + "时" + minutes + "分"+ seconds + "秒" ;
    setTimeout("showlentime()",1000);
}
