function full2half(text){
    var z = ["０","１","２","３","４","５","６","７","８","９"];
    for(var i=0; i<10; i++) text = text.replace(new RegExp(z[i],"g"), i);
    text = text.replace(new RegExp("[ー－]","g"), '-');
    return text;
}
$(function(){
    $('tr.required th label').each(function(){
        var text = $(this).text()
        $(this).html( text.replace(':',':<span class="required">(必須)</span>'));
    });
    var nav = $('#gnavi');
    var path = location.pathname
    console.log(path);
    if( path == '/' || path == '' ){
        nav.find('.gnavi-01 a').addClass('hover');
    }else if( path.indexOf('/documents/') === 0 ){
        nav.find('.gnavi-02 a').addClass('hover');
    }else if(path.indexOf('/seminars/') === 0){
        nav.find('.gnavi-03 a').addClass('hover');
    }
});
