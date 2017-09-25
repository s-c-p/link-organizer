	in the preview pane
		the top most box is where you enter tags, it pushes others down if it needs to expand
		the mid box shows related projects, it pushes others down if it needs to expand
		the lower most box contains the list of info fetched from from DB about that link
		  also it has a provision to add comments as info (limit length of info)
	about width left(list):right(preview)::60:40
	enter finalizes a tag, as in typing email ids in email webapps
	
-->

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>Organize recently imported links</title>
	<link rel="stylesheet" href="static-reset.min.css">
	<link rel="stylesheet" href="static-pure.min.css">
	<script type="text/javascript" src="static-umbrella.min.js"></script>
	<style type="text/css">
		/*body {overflow: hidden;}*/
		content {overflow:auto; position:absolute; top: 0px; left:0px; right:0px; bottom:0px; display: flex;}
		.master {background-color: red; overflow: scroll; flex: 0 0 60%;}
		.detail {background-color: green; overflow: scroll; flex: 1;}
		.save-on-enter {background-color: blue;}
		.notes {background-color: pink;}
	</style>
</head>
<body>
<content>

	<div class="master">
		<table class="pure-table">
		<tbody>
		<!-- JS will insert rows here -->
		</tbody>
		</table>
	</div>

	<div class="detail">
		<div class="save-on-enter"></div>
		<div class="notes"></div>
	</div>

</content>
</body>
<script type="text/javascript">
// the JSON database

DATA = {{json_data}};

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
	// delete if findin was successful without any errors
	u("div.detail").remove();
	// derive all needed variable from object for the following template
	template = `
		tags
		projects
		intelligence
		add-intel-btn
		save-btn
	`;
	u("div.detail").append(template);
};

// now, the functions which execute as soon as the page is loaded

json2table(DATA);

u("tr")
	.on("mouseover", function(e) {
		u(e.currentTarget).attr("style", "background-color: aqua;")
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
</script>
</html>
