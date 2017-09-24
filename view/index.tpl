
<!-- 
	this is the app's landing page

	fat header has 4 blocks which show the count and act as buttons for
		view organized links
		go to organize newly imported links
		view error causing links
		go to import new file page
	below it is the tag cloud, you can view project cloud by selecting projects from the dropdown
-->
<!-- 
	TODO: proper links for the four labels
 -->

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>Link Organizer v1.0.1</title>
	<link rel="stylesheet" href="static-reset.min.css">
	<!-- <link rel="stylesheet" href="static-pure-min.css"> -->
</head>
<body>

	<header>
		Welcome
		<a href="">Settings</a>
		<a href="">Link Cache</a>
		<!-- this is where your clicked-but-not-opened(cuzNSFWorVPN)-links-go -->
	</header>

	<div class="glance">
		<div class="label organized">
			<a href="/view_links">{{organized_count}} bookmarks organized</a>
		</div>

		<div class="label pending">
			<a href="/organize_links">{{pending_count}} bookmarks to organize</a>
		</div>

		<div class="label errors">
			<a href="">{{errors_count}} errors encountered when organizing bookmarks</a>
		</div>

		<div class="label import">
			<a href="/view_import">Import a new file into the database</a>
		</div>
	</div>

	<div>
		<select>
			<option value="tags" selected="selected">tags</option>
			<option value="projects">projects</option>
		</select>
		<div class="cloud"></div>
	</div>

	<footer>
		About
	</footer>

</body>
</html>
