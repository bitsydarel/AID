function submitForm() {
    var http = new XMLHttpRequest();
    http.open("POST", "{{ url_for('send_command') }}", true);
    http.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    var params = "search=" + <<get search value>>; // probably use document.getElementById(...).value
    http.send(params);
    http.onload = function() {
        alert(http.responseText);
    }
};