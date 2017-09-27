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

u("#clear_all").on("click", function (e) {
	alert("clearing all");
});

u("#save_details").on("click", function (e) {
	let i = 0;
	let ans = {};	// as opposed to Object
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
