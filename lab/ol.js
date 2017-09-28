// let jj = JSON.parse('[{"vpn": false, "id": 1, "title": "Does it really matter", "projects": ["xx", "yy", "zz"], "swf": true, "tags": ["a", "b", "c"], "notes": ["id: 1", "url: \\"http://example.com\\"", "swf: true, vpn: false"], "url": "http://example.com"}, {"vpn": false, "id": 2, "title": "I think it does", "projects": ["xx", "yy", "zz"], "swf": true, "tags": ["a", "b", "c"], "notes": ["id: 2", "url: \\"http://example.com\\"", "swf: true, vpn: false"], "url": "http://example.com"}, {"vpn": false, "id": 3, "title": "But who cares? Civil Law", "projects": ["xx", "yy", "zz"], "swf": true, "tags": ["a", "b", "c"], "notes": ["id: 3", "url: \\"http://example.com\\"", "swf: true, vpn: false"], "url": "http://example.com"}, {"vpn": false, "id": 4, "title": "The hitchhickers guide to galaxy", "projects": ["xx", "yy", "zz"], "swf": true, "tags": ["a", "b", "c"], "notes": ["id: 4", "url: \\"http://example.com\\"", "swf: true, vpn: false"], "url": "http://example.com"}, {"vpn": false, "id": 5, "title": "Trillian = Tricia MacMillan", "projects": ["xx", "yy", "zz"], "swf": true, "tags": ["a", "b", "c"], "notes": ["id: 5", "url: \\"http://example.com\\"", "swf: true, vpn: false"], "url": "http://example.com"}, {"vpn": false, "id": 6, "title": "Zaphod Beelebrox was an idiot", "projects": ["xx", "yy", "zz"], "swf": true, "tags": ["a", "b", "c"], "notes": ["id: 6", "url: \\"http://example.com\\"", "swf: true, vpn: false"], "url": "http://example.com"}, {"vpn": false, "id": 7, "title": "Benji mouse, I wanna be like him", "projects": ["xx", "yy", "zz"], "swf": true, "tags": ["a", "b", "c"], "notes": ["id: 7", "url: \\"http://example.com\\"", "swf: true, vpn: false"], "url": "http://example.com"}]')

// console.log(jj)

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

