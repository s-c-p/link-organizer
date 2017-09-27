<form>
	<input id=sfw  name=sfw type=checkbox >
	<label for=sfw>is this link Safe For Workplace</label>
	<br>
	<input id=vpn  name=vpn type=checkbox checked>
	<label for=vpn>should this link be hidden from ISP and other watchers?</label>

	<div class=labels>
		<ul class=tags>
			<li class=a-tag>sqlite3</li>
		</ul>
		<ul class=projects>
			<li class=a-project>mission impossible 3</li>
		</ul>
	</div>

	<input class=common-input type=text name=user_input placeholder="#tag @project notes">

	<ul class=notes>
		<li class=a-note>my name is rocky bhaiya</li>
	</ul>
</form>

<script type="text/javascript">
	let babe = 0;	// null
	u("tr").on("click", function(e){
		target = u(e.currentTarget).attr("id");
		if (babe) {
			if (babe.hasChanged) {
				ans = yes_no_prompt(`save changes you just made to "${babe.title}"?`);
				if (ans === 1) {
					u.async(babe, "/save");
				}
			}
			babe = 0;
		}
		babe = DATA[DATA.findIndex(function (dict) { return dict.id==target })]
	});
	draw(details);
	u.on(keypress)...;	// track UI && data changes both
	onSubmitButtonClick(send update data to server);
</script>

