// stackoverflow.com/q/610406/
String.prototype.formatUnicorn = String.prototype.formatUnicorn ||
function () {
	"use strict";
	var str = this.toString();
	if (arguments.length) {
		var t = typeof arguments[0];
		var key;
		var args = ("string" === t || "number" === t) ?
			Array.prototype.slice.call(arguments)
			: arguments[0];
		for (key in args) {
			str = str.replace(new RegExp("\\{" + key + "\\}", "gi"), args[key]);
		}
	}
	return str;
};

// templates

let details_editor = [];
details_editor.push(
'<div id="{link_id}" class=expendable-body>' +
'<input id=clear_all type=button name=clear_all>' +
'<input id=save_details type=submit name=save_details>' +
'<div id=link_details>' +
'	<input id=sfw  name=sfw type=checkbox {checked_if_sfw}>' +
'	<label for=sfw>is this link Safe For Workplace</label>' +
'	<br>' +
'	<input id=vpn  name=vpn type=checkbox {checked_if_not_vpn}>' +
'	<label for=vpn>should this link be hidden from ISP and other watchers?</label>' +
'	<div class=labels>' +
'		<ul class=tags>'
);	// <li class=a-tag>${}</li>
details_editor.push(
'		</ul>' +
'		<ul class=projects>'
);	// <li class=a-project>${}</li>
details_editor.push(
'		</ul>' +
'	</div>' +
'	<input class=common-input type=text name=user_input placeholder="#tag @project notes">' +
'	<ul class=notes>'
);	// <li class=a-note>${}</li>
details_editor.push(
'	</ul>' +
'</div>' +
'</div>'
);

// fetch(
// 	new Request("http://127.0.0.1:8080/populate", {
// 	method: 'GET',
// 	mode: 'no-cors'
// }))
// .then(function (response) {
// 	if (!response.ok) {
// 		throw response.statusText
// 	}
// 	return response.json();
// })
// .then(jsonData => json2table(jsonData))
// .catch(err => console.log(err));
// the JSON database
// DATA = {{json_data}};
DATA = 
[ {id: 1, url: "http://example.com", swf: true, vpn: false, title: "Does it really matter", tags: ["a", "b", "c"], projects: ["xx", "yy", "zz"], notes: ['id: 1', 'url: "http://example.com"', 'swf: true, vpn: false']}
, {id: 2, url: "http://example.com", swf: true, vpn: false, title: "I think it does", tags: ["a", "b", "c"], projects: ["xx", "yy", "zz"], notes: ['id: 2', 'url: "http://example.com"', 'swf: true, vpn: false']}
, {id: 3, url: "http://example.com", swf: true, vpn: false, title: "But who cares? Civil Law", tags: ["a", "b", "c"], projects: ["xx", "yy", "zz"], notes: ['id: 3', 'url: "http://example.com"', 'swf: true, vpn: false']}
, {id: 4, url: "http://example.com", swf: true, vpn: false, title: "The hitchhickers guide to galaxy", tags: ["a", "b", "c"], projects: ["xx", "yy", "zz"], notes: ['id: 4', 'url: "http://example.com"', 'swf: true, vpn: false']}
, {id: 5, url: "http://example.com", swf: true, vpn: false, title: "Trillian = Tricia MacMillan", tags: ["a", "b", "c"], projects: ["xx", "yy", "zz"], notes: ['id: 5', 'url: "http://example.com"', 'swf: true, vpn: false']}
, {id: 6, url: "http://example.com", swf: true, vpn: false, title: "Zaphod Beelebrox was an idiot", tags: ["a", "b", "c"], projects: ["xx", "yy", "zz"], notes: ['id: 6', 'url: "http://example.com"', 'swf: true, vpn: false']}
, {id: 7, url: "http://example.com", swf: true, vpn: false, title: "Benji mouse, I wanna be like him", tags: ["a", "b", "c"], projects: ["xx", "yy", "zz"], notes: ['id: 7', 'url: "http://example.com"', 'swf: true, vpn: false']}];

// functions required to draw the master list---------------------------------

let dict2row = function (dict) {
	code = `
		<tr id="${dict.id}">
			<td>    <a href="${dict.url}">${dict.title}</a>    </td>
		</tr>
	`;
	u("table > tbody:last-child").append(code);
	return 0;
};

let json2table = function(jsonArr) {
	jsonArr.map(dict2row)
};

// functions required to draw the detail section------------------------------

let show_details = function(object) {
	let i = 0;
	let link_id = object.id;
	let checked_if_sfw = "checked" ? object.swf : "";
	let checked_if_not_vpn = "" ? object.vpn : "checked";
	let tagString= "";
	for (i=0; i<object.tags.length; i++) {
		tagString+= `<li class=a-tag>${object.tags[i]}</li>`;
	};
	let projectString= "";
	for (i=0; i<object.projects.length; i++) {
		projectString+= `<li class=a-project>${object.projects[i]}</li>`;
	};
	let noteString= "";
	for (i=0; i<object.notes.length; i++) {
		noteString+= `<li class=a-note>${object.notes[i]}</li>`;
	};
	// delete if findin was successful without any errors
	u("div.expendable-body").remove();
	// build the final
	final = details_editor[0].formatUnicorn({
			link_id: link_id,
			checked_if_sfw: checked_if_sfw,
			checked_if_not_vpn: checked_if_not_vpn
		}) + tagString +
		details_editor[1] + projectString +
		details_editor[2] + noteString + 
		details_editor[3];
	// draw
	u("div.detail").append(final);
};







// now, the functions which execute as soon as the page is loaded

json2table(DATA);

u("tr")
	.on("mouseover", function(e) {
		u(e.currentTarget).attr("style", "background-color: aquamarine;")
	})
	.on("mouseout", function(e) {
		u(e.currentTarget).attr("style", 'background-color: "";')
	})
	.on("click", function(e) {
		// find it first
		html_id = u(e.currentTarget).attr("id");
		// findIndex better than filter, which would scan the whole array even if
		// a match was found
		index = DATA.findIndex(function (dict) { return dict.id==html_id });
		object = DATA[index];
		show_details(object);
	});
