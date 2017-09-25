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
		body {overflow: hidden;}
		content {
			overflow:auto; position:absolute; top: 0px; left:0px; right:0px; bottom:0px;
			display: flex;
		}
		.master {	flex: 0 0 65%; overflow: scroll;	}
		.detail {	flex: 1; overflow: scroll;		}
	</style>
</head>
<body>

	<content>

		<div class="master">
			<table class="pure-table">
				<tbody> <!-- JS magic happens here --> </tbody>
			</table>
		</div>

		<div class="detail"> <!-- JS magic happens here --> </div>

	</content>

</body>
<script type="text/javascript">
let DATA = {{json_data}};

let dict2row = function (dict) {
	code = `<tr id="${dict.id}"><td>  <a href="${dict.url}">${dict.title}</a>  </td></tr>`;
	u("table > tbody:last-child").append(code);
	return 0;
}

let json2table = function(jsonArr) {	jsonArr.map(dict2row)	};

json2table(DATA)
</script>
<script type="text/javascript">
let show_details = function(object) {
	// delete if findin was successful without any errors
	u("div.detail").remove();
	template = `
		tags
		projects
		intelligence
		add-intel-btn
		save-btn
	`;
	// // make a holder for html
	// holder = "";
	// // for key, value in dict: -- templateize
	// Object.keys(object)
	// 	.forEach( function (key) {
	// 		holder+= '<div class="info"><dt>' + key + "</dt>		<dd>" + object[key] + "</dd></div>";
	// });
	u("div.detail").append(holder);
};

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
		// findIndex better than filter, which would scan the whole array even if the match was found
		index = DATA.findIndex(function(dict){return dict.id==html_id});
		object = DATA[index];
		show_details(object);
	});
</script>
</html>
