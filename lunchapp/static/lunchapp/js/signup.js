/*
	Add a person
	Use ajax on submit to dynamically update the database and then 
	refresh the lists of people who are signed up and not signed up
*/
$(document).ready(function() {
	var frm = $('#add-form');
	frm.submit(function(event) { 	
		event.preventDefault();
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
		$.ajax({
			type: frm.attr('method'),
			url: frm.attr('action'),
			data: frm.serialize(),
			success: function (stuff) {
                if ($('#signed-up-selector').children('option').length > 0) {
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
