function task_validations(){
    var task_name = document.getElementById("textfield1");
    document.querySelectorAll(".error").forEach((element)=>{
        element.remove();
    });
    if(!task_name.value){
        let span = document.createElement('span');
        let text = "Enter Any task Description/Name";
        text = text.fontcolor("red");
        span.innerHTML = text;
        span.className = "error";
        span.style.color = "#ff0000";
        task_name.parentElement.prepend(span);
        return false;
    }
    return true;
}

function update_validations(){
    var form = document.form;
    document.querySelectorAll(".error").forEach((element)=>{
        element.remove();
    });
    for(const field of form){
        if(field.name == "name" && !field.value){
            let span = document.createElement('span');
            let text = "Enter Any task Description/Name";
            text = text.fontcolor("red");
            span.innerHTML = text;
            span.className = "error";
            span.style.color = "#ff0000";
            field.parentElement.prepend(span);
            return false;
        }
    }
    return true;
}