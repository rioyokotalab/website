function chglang() {
;	var url = window.location.href ;
	if ( url.match('/jp/')) {
		var nexturl = url.replace( '/jp/', '/en/' );
	}  else  {
		var nexturl = url.replace( '/en/', '/jp/' );
	}
	document.location = nexturl;
}
