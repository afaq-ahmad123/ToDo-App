function validate(){
    var form = document.form;
    var error = false;
    const emailRegExp = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    for(const field of form){
        if(field.name != "first_name" && field.name != "last_name" && 
        field.name != "csrfmiddlewaretoken" && field.name != ""){
            value = field.value || null;
            if(field.name == "username" && field.value.length < 4){
                if(!document.getElementById("user_error")){
                    let span = document.createElement('span');
                    let text = "Username should be more than 4 characters";
                    console.log("error");
                    text = text.fontcolor("red");
                    span.innerHTML = text;
                    span.id = "user_error";
                    span.style.color = "#ff0000";
                    let user = document.getElementsByName(field.name)[0];
                    user.parentElement.append(span);
                }
                error = true;
            }
            if(field.name == "email" && !emailRegExp.test(field.value)){
                if(!document.getElementById("email_error")){
                    let span = document.createElement('span');
                    let text = "Please enter correct email";
                    text = text.fontcolor("red");
                    span.innerHTML = text;
                    span.id = "email_error";
                    span.style.color = "#ff0000";
                    let email = document.getElementsByName(field.name)[0];
                    email.parentElement.append(span);
                }
                error = true;
            }
            if(field.name == "password" && field.value.length < 8){
                if(!document.getElementById("length_error")){
                    let span = document.createElement('span');
                    let text = "Password Length";
                    text = text.fontcolor("red");
                    span.innerHTML = text;
                    span.id = "length_error";
                    span.name = "error";
                    span.style.color = "#ff0000";
                    let passowrd = document.getElementsByName(field.name)[0];
                    passowrd.parentElement.appendChild(span);
                }
                error = true;
            }
            if(field.name == "password2" && 
            document.getElementsByName("password")[0].value != field.value){
                if(!document.getElementById("match_error")){
                    let span = document.createElement('span');
                    let text = "Password doesn't match";
                    text = text.fontcolor("red");
                    span.innerHTML = text;
                    span.id = "match_error";
                    span.name = "span";
                    span.style.color = "#ff0000";
                    let passowrd = document.getElementsByName(field.name)[0];
                    passowrd.parentElement.append(span);
                }
                error = true;
            }
        }

    }
    if(error == true){
        return false;
    }
    alert("ok");
    return true;
}
