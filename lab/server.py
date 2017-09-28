import json
import bottle

DATA = \
[ {"id": 1, "url": "http://example.com", "swf": True, "vpn": False, "title": "Does it really matter", "tags": ["a", "b", "c"], "projects": ["xx", "yy", "zz"], "notes": ['id: 1', 'url: "http://example.com"', 'swf: true, vpn: false']}
, {"id": 2, "url": "http://example.com", "swf": True, "vpn": False, "title": "I think it does", "tags": ["a", "b", "c"], "projects": ["xx", "yy", "zz"], "notes": ['id: 2', 'url: "http://example.com"', 'swf: true, vpn: false']}
, {"id": 3, "url": "http://example.com", "swf": True, "vpn": False, "title": "But who cares? Civil Law", "tags": ["a", "b", "c"], "projects": ["xx", "yy", "zz"], "notes": ['id: 3', 'url: "http://example.com"', 'swf: true, vpn: false']}
, {"id": 4, "url": "http://example.com", "swf": True, "vpn": False, "title": "The hitchhickers guide to galaxy", "tags": ["a", "b", "c"], "projects": ["xx", "yy", "zz"], "notes": ['id: 4', 'url: "http://example.com"', 'swf: true, vpn: false']}
, {"id": 5, "url": "http://example.com", "swf": True, "vpn": False, "title": "Trillian = Tricia MacMillan", "tags": ["a", "b", "c"], "projects": ["xx", "yy", "zz"], "notes": ['id: 5', 'url: "http://example.com"', 'swf: true, vpn: false']}
, {"id": 6, "url": "http://example.com", "swf": True, "vpn": False, "title": "Zaphod Beelebrox was an idiot", "tags": ["a", "b", "c"], "projects": ["xx", "yy", "zz"], "notes": ['id: 6', 'url: "http://example.com"', 'swf: true, vpn: false']}
, {"id": 7, "url": "http://example.com", "swf": True, "vpn": False, "title": "Benji mouse, I wanna be like him", "tags": ["a", "b", "c"], "projects": ["xx", "yy", "zz"], "notes": ['id: 7', 'url: "http://example.com"', 'swf: true, vpn: false']}];


@bottle.route("/populate")
def populate():
    return json.dumps(DATA)


if __name__ == '__main__':
    bottle.run(debug=True, reloader=True)
