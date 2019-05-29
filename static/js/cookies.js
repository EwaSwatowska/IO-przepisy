function CookieInit() {
    var CookieArray=[];
    $.cookie('CookieArr',JSON.stringify(CookieArray),{expires: 7, path: '/'});
}

function setCookie(){
    var StoredArray=JSON.parse($.cookie('CookieArr'));
    StoredArray.push("{{ id }}");
    $.cookie('CookieArr',JSON.stringify(StoredArray),{expires: 7, path: '/'});
}

function getCookie(){
    var StoredArray=JSON.parse($.cookie('CookieArr'));
    return StoredArray;
}
