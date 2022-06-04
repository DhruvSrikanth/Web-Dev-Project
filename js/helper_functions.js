function filterActive() {
    var table = document.getElementById("user_table");
    var rows = table.getElementsByTagName('tr');
    
    for (var i = 1; i < rows.length; i++) {
        var status = rows[i].getElementsByTagName("TD")[3];
        console.log(status.innerHTML.toLowerCase());
        if (status.innerHTML.toLowerCase() == "inactive"){
            rows[i].style.display = "";
        }
    }
}

function filterInactive() {
    var table = document.getElementById("user_table");
    var rows = table.getElementsByTagName('tr');
    for (var i = 1; i < rows.length; i++) {
        var status = rows[i].getElementsByTagName("TD")[3];
        console.log(status.innerHTML.toLowerCase()); 
        if (status.innerHTML.toLowerCase() == "active"){
            rows[i].style.display = "";
        }
    }
}

