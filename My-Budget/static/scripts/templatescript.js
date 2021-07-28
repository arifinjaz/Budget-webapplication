// JavaScript source code
function checkinsert() {
    if (document.getElementById("password").value === "" || document.getElementById("username").value === "") {
        alert("please enter a valid ID / Passowrd");
        /*window.location.href = '/login.html';*/
        return;
    }
    else {
        document.getElementById("login").submit();
    }
}

function checkinsert1() {
    if (document.getElementById("fname").value === "" || document.getElementById("lname").value === "") {
        alert("please enter a valid name");
        return;
    }
    else if (document.getElementById("email").value === "") {
        alert("please enter a valid emailid to proceed");
        return;
    }
    else if (document.getElementById("password").value === "" || document.getElementById("username").value === "") {
        alert("please enter a valid ID / Passowrd");
        /*window.location.href = '/login.html';*/
        return;
    }
    else if (document.getElementById("password").value != document.getElementById("confirmpassword").value) {
        alert("Passwords entered do not match");
        return;
    }
    else {
        document.getElementById("register").submit();
    }
}


function validateForm() {

    var x = document.forms["category"]["category"].value;

    if (x == "") {
        alert("Please enter a valid category name");
        return false;
    }
}

function ValidateAmount(amount) {
    var amt = document.getElementById("subcat-amt").value;
    if (amount < amt) {
        alert("Amount exceeds the budget!!!. Either increace the main Budget or decrease the amout");
        document.getElementById("subcat-amt").value = "";
        return false;
    }
}

function flash_alert() {
    alert('yes');
    return;
}





function editEntry(id) {
    //alert(id);
    var x = document.getElementById(id).parentNode;

    // Container <div> where dynamic content will be placed
    var container = document.getElementById("edit-budget");

    var number = document.getElementById(x.id).childElementCount;
    //var data = document.getElementById(x.id).value
    var res = x.id.substring(0, 3);

    var particular = document.getElementById("particular-fexp").children;

    if (res === 'cat') {
        var particular = document.getElementById("category-names").children;
        //alert('yes' + x.id);
    }
    var c = document.getElementById(x.id).children;


    //alert(number);

    // Clear previous contents of the container
    while (container.hasChildNodes()) {
        container.removeChild(container.lastChild);
    }

    var message = document.createElement("h3");
    message.innerHTML = "Append the details or delete the entry";


    container.appendChild(message);

    container.appendChild(document.createElement("hr"));

    for (i = 0; i < number; i++) {

        if (i == (number - 1)) {


            //1st button

            var button = document.createElement("input");
            button.setAttribute("type", "submit");
            button.setAttribute("value", "Append");
            button.setAttribute("class", "btn btn-primary")
            button.setAttribute("name", "append")
            container.appendChild(button);

            container.appendChild(document.createElement("hr"));

            //2nd button
            var button = document.createElement("input");
            button.setAttribute("type", "submit");
            button.setAttribute("value", "Delete");
            button.setAttribute("class", "btn btn-primary")
            button.setAttribute("name", "delete")
            container.appendChild(button);
            // Append a line break 
            container.appendChild(document.createElement("hr"));
            return;
        }

        // Append a node with a label
        var name = particular[i].textContent;
        var label = document.createElement("label");
        label.innerHTML = name;
        if (name === 'id') {
            label.innerHTML = '';
        }
        label.setAttribute("for", name);
        label.style = "text-allign:left;"
        container.appendChild(label)

        // Append a node with a particular
        //container.appendChild(document.createTextNode(name));

        // Create an <input> element, set its type and name attributes

        var input = document.createElement("input");
        
        input.type = "text";
        input.name = name;
        input.value = c[i].textContent;
        input.class = "form-control";
        if (name === 'id') {
            input.setAttribute('hidden', '');
        }
        container.appendChild(input);

        // Append a line break 
        container.appendChild(document.createElement("br"));
        container.appendChild(document.createElement("br"));
    }


}





function editsubcategory(id) {
    var x = document.getElementById(id).parentNode;

    // Container <div> where dynamic content will be placed
    var container = document.getElementById("edit-subcat");

    var number = document.getElementById(x.id).childElementCount;

    var particular = document.getElementById("subcat-particular").children;

    var c = document.getElementById(x.id).children;


    //alert(number);

    // Clear previous contents of the container
    while (container.hasChildNodes()) {
        container.removeChild(container.lastChild);
    }

    var message = document.createElement("h3");
    message.innerHTML = "Append the details or delete the entry";
    container.appendChild(message);

    container.appendChild(document.createElement("hr"));

    for (i = 2; i < number; i++) {

        if (i == (number - 1)) {


            //1st button

            var button = document.createElement("input");
            button.setAttribute("type", "submit");
            button.setAttribute("value", "Append");
            button.setAttribute("class", "btn btn-primary")
            button.setAttribute("name", "append")
            container.appendChild(button);

            container.appendChild(document.createElement("hr"));

            //2nd button
            var button = document.createElement("input");
            button.setAttribute("type", "submit");
            button.setAttribute("value", "Delete");
            button.setAttribute("class", "btn btn-primary")
            button.setAttribute("name", "delete")
            container.appendChild(button);
            // Append a line break 
            container.appendChild(document.createElement("hr"));
            return;
        }

        // Append a node with a label
        var name = particular[i].textContent;

        var label = document.createElement("label");
        label.innerHTML = name;
        if (name === 'id') {
            label.innerHTML = '';
        }
        label.setAttribute("for", name);
        label.style = "text-allign:left;"
        container.appendChild(label)

        // Append a node with a particular
        //container.appendChild(document.createTextNode(name));

        // Create an <input> element, set its type and name attributes

        var input = document.createElement("input");

        input.type = "text";
        input.name = name;
        input.value = c[i].textContent;
        input.class = "form-control";
        if (name === 'id') {
            input.setAttribute('hidden','');
        }
        container.appendChild(input);

        // Append a line break 
        container.appendChild(document.createElement("br"));
        container.appendChild(document.createElement("br"));
    }


}

// block to amend or delete expenses
function editexpenses (id) {
    var x = document.getElementById(id).parentNode;

    // Container <div> where dynamic content will be placed
    var container = document.getElementById("edit-expenses");

    var number = document.getElementById(x.id).childElementCount;

    var particular = document.getElementById("expenses-particular").children;

    var c = document.getElementById(x.id).children;


    //alert(number);

    // Clear previous contents of the container
    while (container.hasChildNodes()) {
        container.removeChild(container.lastChild);
    }

    var message = document.createElement("h3");
    message.innerHTML = "Append the details or delete the entry";
    container.appendChild(message);

    container.appendChild(document.createElement("hr"));

    for (i = 3; i < number; i++) {

        if (i == (number - 1)) {


            //1st button

            var button = document.createElement("input");
            button.setAttribute("type", "submit");
            button.setAttribute("value", "append");
            button.setAttribute("class", "btn btn-primary")
            button.setAttribute("name", "append")
            container.appendChild(button);

            container.appendChild(document.createElement("hr"));

            //2nd button
            var button = document.createElement("input");
            button.setAttribute("type", "submit");
            button.setAttribute("value", "delete");
            button.setAttribute("class", "btn btn-primary")
            button.setAttribute("name", "delete")
            container.appendChild(button);
            // Append a line break 
            container.appendChild(document.createElement("hr"));
            return;
        }

        // Append a node with a label
        var name = particular[i].textContent;

        var label = document.createElement("label");
        label.innerHTML = name;
        if (name === 'id') {
            label.innerHTML = '';
        }
        label.setAttribute("for", name);
        label.style = "text-allign:left;"
        container.appendChild(label)

        // Append a node with a particular
        //container.appendChild(document.createTextNode(name));

        // Create an <input> element, set its type and name attributes

        var input = document.createElement("input");

        input.type = "text";
        input.name = name;
        input.value = c[i].textContent;
        input.class = "form-control";
        if (name === 'id') {
            input.setAttribute('hidden', '');
        }
        container.appendChild(input);

        // Append a line break 
        container.appendChild(document.createElement("br"));
        container.appendChild(document.createElement("br"));
    }


}






function setdate(d) {

    var date = new Date();
    date.setMonth(d);
    document.getElementById('from-date').valueAsDate = date;
}