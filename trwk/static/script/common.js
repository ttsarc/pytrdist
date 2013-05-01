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
});
