function validate(){
    var task_name = document.getElementById("textfield1");
    alert(task_name.value);
    if(!task_name.value){
        return false;
    }
    return true;
}

function update(){
    var form = document.form;
    for(const field of form){
        if(field.name == "name" && !field.value){
            alert(field.value);
            return false;
        }
    }
    return true;
}