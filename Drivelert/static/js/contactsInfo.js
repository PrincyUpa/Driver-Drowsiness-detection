//Function to add contact
function add(name, mobile) {
    //contacts[name] = mobile;
    localStorage.setItem(name, mobile);
    show();
    alert("Contact added sucessfully!!!");
    return;
}

//Function to search contact
function search(name, mobile) {
    let temp = "";
    let flag = 0;
    if (name == "" && mobile == "") {
        alert("Please provide Name or Mobile No.");
        return;
    }
    if (name != "" || name != undefined) {
        Object.keys(localStorage).forEach((key) => {
            if (key == name) {
                temp = "<br><h4>Name : " + key + "<br>Mobile No. : " + localStorage.getItem(key) + "</h4>";
                alert(key + "   " + localStorage.getItem(key));
                flag = 1;
            }
        });
    }
    if (mobile != "" || mobile != undefined) {
        Object.keys(localStorage).forEach((key) => {
            if (localStorage.getItem(key) == mobile) {
                temp = "<br><h4>Name : " + key + "<br>Mobile No. : " + localStorage.getItem(key) + "</h4>";
                alert(key + "   " + localStorage.getItem(key));
                flag = 1;
            }
        });
    }
    if (flag == 0) {
        alert("Contact not found");
        return;
    }
    document.getElementById("searchPrint").innerHTML = temp;
    show();
    return;
}

//Function to delete contact
function del(name, mobile) {
    let flag = 0;
    console.log("delete");
    if (name == "" && mobile == "") {
        alert("Please provide Name or Mobile No.");
        return;
    }
    if (name != "" || name != undefined) {
        Object.keys(localStorage).forEach((key) => {
            if (key == name) {
                localStorage.removeItem(key);
                alert("Contact deleted successfully!!!");
                flag = 1;
            }
        });
    }
    if (mobile != "" || mobile != undefined) {
        Object.keys(localStorage).forEach((key) => {
            if (localStorage.getItem(key) == mobile) {
                localStorage.removeItem(key);
                alert("Contact deleted successfully!!!");
                flag = 1;
            }
        });
    }
    if (flag == 0) {
        alert("Contact not found");
        return;
    }
    show();
    return;
}

//Function to show contacts
function show() {
    let temp = "";
    if (localStorage.length == 0) {
        document.getElementById("showPrint").innerHTML = "No Contacts";
        return;
    }
    Object.keys(localStorage).forEach((key) => {
        temp += "<h3>" + key + " : " + localStorage.getItem(key) + "</h3><br>";
    });
    document.getElementById("showPrint").innerHTML = temp;
    return;
}