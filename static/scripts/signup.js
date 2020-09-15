function user_validation(){
    var form = document.form;
    var error = false;
    document.querySelectorAll(".error").forEach((element)=>{
        element.remove();
    });
    const emailRegExp = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    for(const field of form){
        if(field.name == "username" && field.value.length < 4){
            let span = document.createElement('span');
            let text = "Username should be more than 4 characters";
            text = text.fontcolor("red");
            span.innerHTML = text;
            span.className = "error";
            span.style.color = "#ff0000";
            let user = document.getElementsByName(field.name)[0];
            user.parentElement.append(span);
            error = true;
        }
        if(field.name == "email" && !emailRegExp.test(field.value)){
            let span = document.createElement('span');
            let text = "Please enter correct email";
            text = text.fontcolor("red");
            span.innerHTML = text;
            span.className = "error";
            span.style.color = "#ff0000";
            let email = document.getElementsByName(field.name)[0];
            email.parentElement.append(span);
            error = true;
        }
        if(field.name == "password" && field.value.length < 8){
            let span = document.createElement('span');
            let text = "Password Length";
            text = text.fontcolor("red");
            span.innerHTML = text;
            span.className = "error";
            span.name = "error";
            span.style.color = "#ff0000";
            let passowrd = document.getElementsByName(field.name)[0];
            passowrd.parentElement.appendChild(span);
            error = true;
        }
        if(field.name == "password2" && 
        document.getElementsByName("password")[0].value != field.value){
            let span = document.createElement('span');
            let text = "Password doesn't match";
            text = text.fontcolor("red");
            span.innerHTML = text;
            span.className = "error";
            span.name = "span";
            span.style.color = "#ff0000";
            let passowrd = document.getElementsByName(field.name)[0];
            passowrd.parentElement.append(span);
            error = true;
        }
    }
    if(error == true){
        return false;
    }
    return true;
}
