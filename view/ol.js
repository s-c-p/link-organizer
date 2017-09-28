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
	u(".expendable-body").remove();
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
	// activate input region
	u(".common-input").on("keydown", function (e) {
		if (e.which == 13) {
			// avoid form submission on enter key press
			e.preventDefault();
			// now on to the logic
			let val = document.querySelector(".common-input").value;
			let code = "";
			let target = "";
			switch (val[0]) {
				case "#":
					code = "<li class=a-tag>" + val;
					target = ".tags";
					break;
				case "@":
					code = "<li class=a-project>" + val;
					target = ".projects";
					break;
				default:
					code = "<li class=a-note>" + val;
					target = ".notes";
					break;
			}
			code += "</li>";
			u(target).append(code);
			// clear the input field
			document.querySelector(".common-input").value = "";
		}
	});
	// activate clear_all button
	u("#clear_all").on("click", function (e) {
		u(".expendable-body").remove();
	});
	// activate submit
	u("#save_details").on("click", function (e) {
		let i = 0;
		let ans = {};	// as opposed to Object
		ans.id = document.querySelector(".expendable-body").id;
		ans.sfw = document.getElementById("sfw").checked;
		ans.vpn = document.getElementById("vpn").checked;
		let x = document.querySelectorAll(".a-tag");
		ans.tags = [];
		for (i=0; i<x.length; i++) {ans.tags.push(x[i].innerText);}
		let y = document.querySelectorAll(".a-project");
		ans.projects = [];
		for (i=0; i<y.length; i++) {ans.projects.push(y[i].innerText);}
		let z = document.querySelectorAll(".a-note");
		ans.notes = [];
		for (i=0; i<z.length; i++) {ans.notes.push(z[i].innerText);}
		console.log(ans);
	});
	// activate delete button, bit.ly/2k4OWFf
	u("li[class^=a-]").on("click", function (e) {
			this.parentNode.removeChild(this);
	});
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
