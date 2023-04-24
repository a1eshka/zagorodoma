$(document).ready(function(){
	const alert = document.getElementById('alert');
    $("#loadMore").on('click',function(){
        var _currentPosts=$(".post-box").length;
        var _limit=$(this).attr('data-limit');
        var _total=$(this).attr('data-total');
        		// Run Ajax
		$.ajax({
			url:'/load-more-data',
			data:{
                limit:_limit,
                offset:_currentPosts,
            },
			dataType:'json',
			beforeSend:function(){
				$("#loadMore").attr('disabled',true)
			},
			success:function(res){
                $("#filteredProducts").append(res.object_list);
				$("#loadMore").attr('disabled',false)
				
				var _totalShowing=$(".post-box").length;
				if(_totalShowing==_total){
					$("#loadMore").remove();
					
				}
			}
        });
		
    });
});

