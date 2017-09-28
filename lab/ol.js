let json2table = function (jsonArr) {
	console.log("inside the function");
	console.log(jsonArr);
	return 0;
}

console.log("start");

fetch(
	new Request("http://127.0.0.1:8080/populate", {
	method: 'GET',
	mode: 'no-cors'
}))
.then(function (response) {
	if (!response.ok) {
		throw response.statusText
	}
	return response.json();
})
.then(jsonData => json2table(jsonData))
.catch(err => console.log(err));

console.log("stop");
