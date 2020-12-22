//$(document),可以只写成$（），.ready()也可以不要，直接把函数写在$()中

$(document).ready(function(){
    var xuhao = 1;
    $('#add_row').click(function(){
        xuhao++;
        var my_html="<tr id='row"+xuhao+"' class='row'> \
                        <td>"+xuhao+"</td>\
                        <td><input type='text' name='color' value='13#'></td>\
                        <td><input type='text' name='length' value='100'></td>\
                        <td ><input type='text' name='price' value='8.3'></td>\
                    </tr>"
        $('#tb_tail').before(my_html);
        
    });

});
function delRow(){
    alert($(this).text());
};