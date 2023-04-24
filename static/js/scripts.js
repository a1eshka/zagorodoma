$(document).ready(function(){
	$(".ajaxLoader").hide();
	// Product Filter Start
	$("#PriceFilter").on('click',function(){
		var _filterObj={};
        var _minPrice=$('#minPrice').val();
        var _maxPrice=$('#maxPrice').val();
        _filterObj.minPrice=_minPrice;
        _filterObj.maxPrice=_maxPrice;
        var _minFloors=$('#minFloors').val();
        var _maxFloors=$('#maxFloors').val();
        _filterObj.minFloors=_minFloors;
        _filterObj.maxFloors=_maxFloors;
        var _minLand_area=$('#minLand_area').val();
        var _maxLand_area=$('#maxLand_area').val();
        _filterObj.minLand_area=_minLand_area;
        _filterObj.maxLand_area=_maxLand_area;
		var _minsquare=$('#minsquare').val();
        var _maxsquare=$('#maxsquare').val();
        _filterObj.minsquare=_minsquare;
        _filterObj.maxsquare=_maxsquare;
		$(".filter-checkbox").each(function(index,ele){
			var _filterVal=$(this).val();
			var _filterKey=$(this).data('filter');
			_filterObj[_filterKey]=Array.from(document.querySelectorAll('option[data-filter='+_filterKey+']:checked')).map(function(el){
			 	return el.value;
			});
		});
        
		// Run Ajax
		$.ajax({
			url:'/json-filter',
			data:_filterObj,
			dataType:'json',
			beforeSend:function(){
				
			},
			success:function(res){
				$(".btnload").hide();
				$("#filteredProducts").html(res.object_list);
			}
        });
	});
});

