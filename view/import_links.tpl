<!-- 
	select file, begin upload
-->

<!-- 
	TODO
	show progress bar
 -->

<!DOCTYPE html>
<html>
<head>
	<title>Import bookmarks file</title>
</head>
<body>

	<div class="import-fail" style="display: {{display_err_block}};">
		<p>Oops... This is embarassing but something went wrong and your file couldn't be imported</p>
		<pre>{{err_msg}}</pre>
	</div>

	<form action="/import_file" method="POST" enctype="">
		<input type="file" name="import_file" onchange="this.form.submit();" accept="">
	</form>

</body>
</html>
