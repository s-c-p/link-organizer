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
