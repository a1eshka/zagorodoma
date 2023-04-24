$(".dropdown dt a").on('click', function() {
  $(".dropdown dd ul").slideToggle('fast');
});

$(".dropdown dd ul li a").on('click', function() {
  $(".dropdown dd ul").hide();
});

function getSelectedValue(id) {
  return $("#" + id).find("dt a span.value").html();
}

$(document).bind('click', function(e) {
  var $clicked = $(e.target);
  if (!$clicked.parents().hasClass("dropdown")) $(".dropdown dd ul").hide();
});

$('.mutliSelect input[type="checkbox"]').on('click', function() {

  var title = $(this).closest('.mutliSelect').find('input[type="checkbox"]').val(),
    title = $(this).val() + ",";

  if ($(this).is(':checked')) {
    var html = '<span title="' + title + '">' + title + '</span>';
    $('.multiSel').append(html);
    $(".hida").hide();
  } else {
    $('span[title="' + title + '"]').remove();
    var ret = $(".hida");
    $('.dropdown dt a').append(ret);

  }
});
$(function(){
        $('#line-wrap-example').multiSelect({
            positionMenuWithin: $('.position-menu-within')
        });
        $('#typeobj').multiSelect({
            noneText: 'Тип объекта',
            
        });
        $('#getstatus').multiSelect({
            noneText: 'Тип сделки',
            
        });
        $('#landstat').multiSelect({
            noneText: 'Статус участка',
            
        });
        $('#housematerial').multiSelect({
            noneText: 'Материал дома',
            
        });
        $('#district').multiSelect({
            noneText: 'Район',
            
        });
        $('#modal-example').multiSelect({
            'modalHTML': '<div class="multi-select-modal">'
        });
    });


    $(document).ready(function(){
    $("#showHideContent").click(function () {
        if ($("#Land_area").is(":hidden")) {
            $("#Land_area").show();
        } else {
            $("#Land_area").hide();
        }
        if ($("#square").is(":hidden")) {
            $("#square").show();
        } else {
            $("#square").hide();
        }
        if ($("#floors").is(":hidden")) {
            $("#floors").show();
        } else {
            $("#floors").hide();
        }
        if ($("#housemat").is(":hidden")) {
            $("#housemat").show();
        } else {
            $("#housemat").hide();
        }
        if ($("#distr").is(":hidden")) {
            $("#distr").show();
        } else {
            $("#distr").hide();
        }
        return false;
    });
});
