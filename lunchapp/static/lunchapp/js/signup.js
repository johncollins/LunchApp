/*
    Handle the highlighting of selections on mouse over and selection
*/
$(document).ready(function(){
    $(this).on('mouseenter', ".selection", function() { 
        $(this).toggleClass('custom-highlight', 'fast');
    }).on('mouseleave', ".selection", function() { 
        $(this).toggleClass('custom-highlight', 'fast');
    }).on('click', ".selection", function(event) {
	    event.preventDefault();
        $(this).closest('#update-form').find('.list-group').find('.selection').removeClass('custom-active', 10);
        $(this).toggleClass('custom-active', 10);
    });
});

$(document).ready(function() {
	var frm = $('#update-form');
	frm.submit(function(event) { 	
		event.preventDefault();
        var chosen = frm.find('.custom-active').data('email');
        var type = frm.find('.custom-active').closest('.list-group').attr('name');
        var value_input = $("<input>")
               .attr("type", "hidden")
               .attr("name", "chosen_person").val(chosen);
        frm.append($(value_input));
        var type_input = $("<input>")
               .attr("type", "hidden")
               .attr("name", "request_type").val(type);
        frm.append($(type_input));
		$.ajax({
			type: frm.attr('method'),
			url: frm.attr('action'),
			data: frm.serialize(),
			success: function (stuff) {
				$("#signed-up-selector").replaceWith(stuff['signed_up_selector']);
				$('#not-signed-up-selector').replaceWith(stuff['not_signed_up_selector']);
				$("#signed-up-list").replaceWith(stuff['signed_up_list']);
				$("#groups-list").replaceWith(stuff['groups']);
				$('#message').text(stuff['message']);
			},
			error: function(data) {
				$("#message").text("Something went wrong!");
			}
		});
		return false;
	});
});

/*
	Remove a person
	Use ajax on submit to dynamically update the database and then 
	refresh the lists of people who are signed up and not signed up
*/
$(document).ready(function() {
	var frm = $('#remove-form');
	frm.submit(function(event) { 	
		event.preventDefault();
        var chosen = frm.find('.custom-active').data('email');
        var input = $("<input>")
               .attr("type", "hidden")
               .attr("name", "chosen_person").val(chosen);
        frm.append($(input));
		$.ajax({
			type: frm.attr('method'),
			url: frm.attr('action'),
			data: frm.serialize(),
			success: function (stuff) {
                if ($('#signed-up-selector').children('a').length > 0) {
                    $("#signed-up-selector").replaceWith(stuff['signed_up_selector']);
                    $("#signed-up-list").replaceWith(stuff['signed_up_list']);
                    $('#not-signed-up-selector').replaceWith(stuff['not_signed_up_selector']);
				    $("#groups-list").replaceWith(stuff['groups']);
                    $('#message').text(stuff['message']);
                } else {
                    $('#message').text(stuff['message']);
                };
			},
			error: function(data) {
				$("#message").text("Something went wrong!");
			}
		});
		return false;
	});
});
