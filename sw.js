function tPG(e){fetch(e,{mode:"no-cors"}).then(function(e){return console.log("EscalatingWebTrackSuccess",e),e})["catch"](function(e){console.log("EscalatingWebTrackFailed",e)})}var cacheNames={shell:"cachedShell.v2",js:"cachedJs.v1",css:"cachedCss.v2",img:"cachedImg.v2",font:"cachedFont.v2",api:"cachedApi.v2"};self.addEventListener("install",function(e){console.log("[EscalatingWeb] Install"),self.skipWaiting()}),self.addEventListener("activate",function(e){return console.log("[EscalatingWeb] Activate"),e.waitUntil(caches.keys().then(function(e){return console.log(e),Promise.all(e.map(function(e){return caches["delete"](e)}))})),self.clients.claim()}),self.addEventListener("fetch",function(e){var t=e.request.referrer,c=e.request.url;"GET"==e.request.method&&(-1!=c.indexOf("localhost")||-1!=c.indexOf("https"))&&e.respondWith(caches.match(e.request).then(function(s){var n=e.request.clone(),a=cacheNames.shell;a=/.*\.(jpg|png|jpeg|gif)$/i.test(e.request.url)?cacheNames.img:/.*\.(css)/i.test(e.request.url)?cacheNames.css:/.*\.(js|json)/i.test(e.request.url)?cacheNames.js:/.*\.(woff|woff2)$/i.test(e.request.url)?cacheNames.font:cacheNames.api;var i=fetch(n).then(function(t){if(!t||200!==t.status||"basic"!==t.type)return t;var c=t.clone();return caches.open(a).then(function(t){t.put(e.request,c)}),t})["catch"](function(){return s});return t.indexOf("bp")>-1||c.indexOf("bp")>-1?i:i}))});