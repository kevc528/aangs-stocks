$(function() {
    $("#login-form").submit(function( event ) {
        let formData = {
            email : $("#email-input").val(),
            password : $("#password-input").val()
        }
        $.ajax({
            type: "POST",
            url: "/user/login",
            data: JSON.stringify(formData),
            success: function() {
                window.location.replace("/");
            },
            error: function() {
                alert("Incorrect email or password!");
            },
            dataType: "json",
            contentType : "application/json"
        });
        event.preventDefault();
    });
});