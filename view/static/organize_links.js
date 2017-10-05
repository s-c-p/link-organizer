let BASE_URL = "http://127.0.0.1:8080";

// borrowed from outer world -------------------------------------------------

String.prototype.formatUnicorn = String.prototype.formatUnicorn ||
function () {
	// stackoverflow.com/q/610406/
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

// templates -----------------------------------------------------------------

let details_editor = [];
details_editor.push(
'<div id="{link_id}" class=expendable-body>' +
'<input id=clear_all type=button name=clear_all>' +
'<input id=save_details type=submit name=save_details>' +
'<div id=link_details>' +
'	<input id=sfw  name=sfw type=checkbox {link_sfw}>' +
'	<label for=sfw>is this link Safe For Workplace</label>' +
'	<br>' +
'	<input id=vpn  name=vpn type=checkbox {link_vpn}>' +
'	<label for=vpn>should this link be hidden from ISP and other watchers?</label>' +
'	<div class=labels>' +
'		<ul class=tags>'
);			// <li class=a-tag>${}</li>
details_editor.push(
'		</ul>' +
'		<ul class=projects>'
);			// <li class=a-project>${}</li>
details_editor.push(
'		</ul>' +
'	</div>' +
'	<input class=common-input type=text name=user_input placeholder="#tag @project notes">' +
'	<ul class=notes>'
);			// <li class=a-note>${}</li>
details_editor.push(
'	</ul>' +
'</div>' +
'</div>'
);

// functions -----------------------------------------------------------------

/**
 * takes a JS object and draws a clickable row, form the single-y function to
 * be used with json2table as-in Array.map
 * @param {*object} dict a js object containing all details related to a link
 */
let dict2row = function (dict) {
	code = `
		<tr id="${dict.id}">
			<td>    <a href="${dict.url}">${dict.title}</a>    </td>
		</tr>
	`;
	u("table > tbody:last-child").append(code);
	return 0;
};

/**
 * required to draw the master list
 * @param {*Array} jsonArr the array of links returned by server
 */
let json2table = function(jsonArr) {
	jsonArr.map(dict2row)
};

/**
 * required to draw the detail section of the master-detail view, this
 * function also activates the necessary event listners because I don't
 * know how to activate them ass soon as they come into existance, making
 * those event listeners global doesn't work
 * @param {*Object} object the entire link's details in a single variable
 */
let show_details = function(object) {
	let i = 0;
	let link_id = object.id;
	let link_sfw = "" ? object.swf : "checked";
	let link_vpn = "checked" ? object.vpn : "";
	let tagString = "";
	for (i=0; i<object.tags.length; i++) {
		tagString += `<li class=a-tag>${object.tags[i]}</li>`;
	};
	let projectString = "";
	for (i=0; i<object.projects.length; i++) {
		projectString += `<li class=a-project>${object.projects[i]}</li>`;
	};
	let noteString = "";
	for (i=0; i<object.notes.length; i++) {
		noteString += `<li class=a-note>${object.notes[i]}</li>`;
	};
	// delete if findin was successful without any errors
	u(".expendable-body").remove();
	// build the final
	final = details_editor[0].formatUnicorn({
			link_id: link_id,
			link_sfw: link_sfw,
			link_vpn: link_vpn
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
		let ans = {};	// as opposed to Object(), best practice
		ans.id = document.querySelector(".expendable-body").id;
		ans.sfw = document.getElementById("sfw").checked;
		ans.vpn = document.getElementById("vpn").checked;
		let x = document.querySelectorAll(".a-tag");
		ans.tags = [];
		for (i=0; i<x.length; i++) {
			ans.tags.push(x[i].innerText);
		}
		let y = document.querySelectorAll(".a-project");
		ans.projects = [];
		for (i=0; i<y.length; i++) {
			ans.projects.push(y[i].innerText);
		}
		let z = document.querySelectorAll(".a-note");
		ans.notes = [];
		for (i=0; i<z.length; i++) {
			ans.notes.push(z[i].innerText);
		}
		// TODO: change this
		console.log(ans);
	});
	// activate delete button, bit.ly/2k4OWFf
	u("li[class^=a-]").on("click", function (e) {
		// the looks part i.e. show delete button on hover
		// is handled by CSS
		this.parentNode.removeChild(this);
	});
};

// finally, the functions which execute as soon as the page is loaded---------

let data = [];
let global_pageNum = 1;

let getPage = function (pageNum) {
	fetch(
		new Request(BASE_URL + `/populate?pageNum=${pageNum}`, {
		method: 'GET',
		mode: 'no-cors'
	}))
	.then(function (response) {
		if (!response.ok) {
			throw response.statusText
		}
		return response.json();
	})
	.then(function (jsondata) {
		data = jsondata;	// so that downloaded 'data' can be used later
		u(".pure-table > tbody").remove()
		u(".pure-table").append("<tbody></tbody>")
		json2table(data);
	})
	.catch(err => console.log(err));
};

window.onload = (function () {
	// fetch-draw-store first 10
	getPage(global_pageNum);
	// draw nex button && previous button if pageNum !=1
	// ensure page number is properly incremented / decremented
	global_pageNum += 1;
	// activate button behaviour
	u("tr")
	.on("mouseover", function(e) {
		u(e.currentTarget).attr("style", "background-color: #2ecc71;")
	})
	.on("mouseout", function(e) {
		u(e.currentTarget).attr("style", 'background-color: "";')
	})
	.on("click", function(e) {
		// find it first
		html_id = u(e.currentTarget).attr("id");
		// ``findIndex`` is better than ``filter``, because the later would scan
		// the whole array even after a match was found, thus wasting time,money
		index = data.findIndex(function (dict) { return dict.id===html_id });
		object = data[index];
		show_details(object);
	});
})();

