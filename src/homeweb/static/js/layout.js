var contact_prefetch = null;
function get_contact_popover(info) {
	var container = $("<div>");
	var datapoints = [ [ 'name', 'Name' ], [ 'email', 'E-Mail' ],
			[ 'g+', 'Google+ Profile' ], [ 'phone', 'Phone' ], ];
	for ( var i in datapoints) {
		var key = datapoints[i][0];
		var tag = datapoints[i][1];
		var item = $("<p>");
		item.append($("<strong>", {
			"text" : tag + ": "
		}));
		item.append($("<span>", {
			"text" : info[key]
		}));
		container.append(item);
	}
	return container.prop("outerHTML");
}

$(document).ready(function() {
	$("#contact-btn").popover({
		"html" : true,
		"trigger": "focus",
		"placement" : "bottom",
		"title" : "Contact info",
		"content" : function() {
			if (contact_prefetch!==null) {
				return '<div id="layout-contact-popover">' + get_contact_popover(contact_prefetch) + '</div>';
			}

			$.post("/contact", {
				"this is a real contact info request" : "yup"
			}, function(data) {
				contact_prefetch = data;
				$("#contact-btn").popover("show");
			}, 'json');

			return '<div id="layout-contact-popover"><span>Loading...</span></div>';
		}
	});
});
