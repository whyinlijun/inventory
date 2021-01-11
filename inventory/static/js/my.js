var xuhao = 2;
        $(function(){
            //设置日期
            $("#order_date").val(myDate());
            $("#order_id").val(getOrderId($("#order_date").val(), $("#customer").val()));
            $("#customer").change(function(){
                $("#order_id").val(getOrderId($("#order_date").val(), $("#customer").val()));
            })
            $("#order_date").change(function(){
                $("#order_id").val(getOrderId($("#order_date").val(), $("#customer").val()));
            })
            $('.quantity').eq(0).focus()

            //获取需要重复的html
            var get_html=$('tbody').children().eq(0).html();

            $('#add_row').click(function(){
                //当有输入框数量没有输入时，不可以增加一行
                //var flag=checkQuantityInput();
                if(checkQuantityInput('.quantity')){
                    $('#last_row').before('<tr>'+get_html.replace('<td>1</td>','<td>'+ xuhao++ +'</td>')+'</tr>');
                    $('.quantity').eq(xuhao-2).focus()
                };
            });

            //输入框回车动作
            $('tbody').on("keydown", ".quantity",function(e){
                if(e.keyCode==13){
                   //$('select').focus();
                   $(this).blur()
                };
            })

            //输入框失去焦点动作
            $('tbody').on("blur", ".quantity",function(){
                //当数量输入框失去焦点时，计算小计，总计金额，总计数量,当输入框没有数量时
                //this 代表 input, parent 代表当前td
                var amount=Number($(this).parent().prev().text()) * Number($(this).val())
                if ($(this).val()==''){
                    $(this).focus();
                };
                //小计金额
                $(this).parent().next().text(amount)
                //总计金额
                $("#amount").text(mytotal(5));
                //总计数量
                $("#quantity").text(myQuantity());

            });

            $('tbody').on("change", "select",function(){
                //商品选择后，标出相应价格
                var url='/getprice?id='+$(this).val();
                var tar=$(this).parent().next();
                $.ajax({url:url,success:function(result){
                    tar.text(result);
                }});
                //var tr=$(this).parentsUntil('tbody')
                //$(tr).find(".quantity").val('10');
                $(tar).next().children('.quantity').focus();
            });

            $('#actions').click(function(){
                //判断数量有没有空的，没有就可以提交了
                if(checkQuantityInput('.quantity')){
                    $('#order_quantity').val($('#quantity').text())
                    $('#order_amount').val($('#amount').text())
                    $('form').submit()
                }
                else{
                    alert('有项目数量为空')
                }
                
            });

        });

        



        function delRow(id){
            // 删除一行并将序号栏重新编码，数据重新统计
            //设置序号为删除那一栏的序号
            var i=$(id).parents('tr').children().first().text();
            $(id).parents('tr').nextAll().not("#last_row").each(function(){
                $(this).children().first().text(i++);
            });
            $(id).parents('tr').remove();
            xuhao--;
            $("#amount").text(mytotal(5));
            $("#quantity").text(myQuantity());
        };

        function mytotal(td_index){
            //表格金额统计，参数为要计算的是第几列
            var i=0;
            $('tbody tr').siblings().not("#last_row").each(function(){
                i+=Number($(this).children().eq(td_index-1).text());
            });
            return i;
        };

        function myQuantity(){
            //件数统计
            var i=0;
            $('.quantity').each(function(){
                i+=Number($(this).val());
            });
            return i;
        };
        function checkQuantityInput(id){
            //判断输入框是否有数据，没有就设置
            var input_flag=true;
            $(id).each(function(){
                if ($(this).val()==''){
                    $(this).focus();
                    input_flag=false;
                };
            
            });
            
            return input_flag;
        };

        function myDate(){
            var d=new Date();
            year = d.getFullYear()
            month = d.getMonth() + 1
            if(month<10){month='0'+String(month)}
            date = d.getDate()
            if(date<10){date='0'+String(date)}
            return year + '-' + month + '-' + date
        };

        function getOrderId(ordate,name){
            var d=new Date()
            hour = d.getHours()
            if(hour<10){hour='0'+String(hour)}
            min = d.getMinutes()
            if(min<10){min='0'+String(min)}
            sec = d.getSeconds()
            if(sec<10){sec='0'+String(sec)}
            var c = new Date(ordate)
            year = c.getFullYear()
            month = c.getMonth() + 1
            if(month<10){month='0'+String(month)}
            day = c.getDate()
            if(day<10){day='0'+String(day)}
            return year+month+day+hour+min+sec+'-'+name
        };

