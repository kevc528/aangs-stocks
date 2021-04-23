$(function() {
    $("#register-form").submit(function( event ) {
        if (($("#password-input").val() == $("#password-verify-input").val())) {
            let formData = {
                email : $("#email-input").val(),
                password : $("#password-input").val()
            }
            $.ajax({
                type: "POST",
                url: "/user",
                data: JSON.stringify(formData),
                success: function() {
                    alert("Successfully registered!")
                    window.location.replace("/login");
                },
                error: function() {
                    alert("An account with this username already exists!");
                },
                dataType: "json",
                contentType : "application/json"
            });
        } else {
            alert('The inputted passwords must be the same!');
        }
        event.preventDefault();
    });
});