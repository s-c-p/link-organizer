	a nice fat header dedicated for searching
	below the header there is a paginated table, looking like
	Link(active/prompt/inactive)	tag-list-preview	project-list-preview
		prompt   ==> for !sfw links IFF familyMode==ON
		inactive ==> for vpn-required==true
		active	 ==> for every other links
	Also, the preview thingy is habdled entirely by CSS
-->

<!DOCTYPE html>
<html>
<head>
	<title>All your links</title>
</head>
<body>

	<header>
		<form action="/search">
			<input class="search" placeholder="Search: #tag @project words"></input>
			<button type="submit">Submit</button>
		</form>
	</header>

	<content>
		<table>
			<thead>
				<td>Link</td>
				<td>Tags</td>
				<td>Projects</td>
			</thead>
			<tbody>
			% for aRow in table_body:
				<tr>
				% for _ in aRow:
					<td> {{ _ }} </td>
				% end
				</tr>
			% end
			</tbody>
		</table>
	</content>

</body>
</html>
