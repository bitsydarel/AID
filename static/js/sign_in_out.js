$(function () {

// hide invalid username message and message typing area
$('#invalidUsername').hide();
$('#chatEnabled').hide();

// focus cursor to sign in area on button click
$('#signInButton').click(function() {
	$('#username').focus();
});

// code to execute on user sign in button click
$('#userSignIn').click(function() {
	var username = $('#username').val();

	if (username == '') {
		$('#invalidUsername').show();
		return false;
	} else {
		$.ajax({
			data: { username: username },
			type: "GET",
			url: "insert_username.php",
			success: function() {
				$('#signInArea').html('<span class="welcome">Welcome <span id="loggedInUser">' + username + '</span></span>');
			}
		});

		$('#signInToChat').hide();
		$('#chatEnabled').show();
	}
});


});