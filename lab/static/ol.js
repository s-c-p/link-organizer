let json2div = function (jsonArr) {
	console.log(jsonArr);
	return 0;
}

let x = fetch(
	new Request("http://127.0.0.1:8080/populate", {
	method: 'GET',
	mode: 'no-cors'
}))
.then(function (response) {
	// if (!response.ok) {
	// 	throw response.statusText
	// }
	return response.json();
})
.then(jsonData => json2div(jsonData))
// .catch(err => console.log(err));

