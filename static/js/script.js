function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function allowDrop(ev) {
    ev.preventDefault();
}

function drop(ev) {
    ev.preventDefault();
    let data = ev.dataTransfer.getData("text");
    ev.currentTarget.appendChild(document.getElementById(data));
}

function createTask() {
    let x = document.getElementById("inprogress");
    let y = document.getElementById("done");
    let z = document.getElementById("create-new-task-block");
    if (x.style.display === "none") {
        x.style.display = "block";
        y.style.display = "block";
        z.style.display = "none";
    } else {
        x.style.display = "none";
        y.style.display = "none";
        z.style.display = "flex";
    }
}

function saveTask() {
    let taskName = document.getElementById("name").value;
    let taskDescription = document.getElementById("description").value;
    let taskStatus = document.getElementById("status").value;

    // Send data to Django view using AJAX
    let xhr = new XMLHttpRequest();
    xhr.open("POST", `/projects/${projectId}/save_task/`, true);  // Update the URL to match your Django URL pattern
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                // Handle successful response
                console.log("Task saved successfully!");
            } else {
                // Handle error response
                console.error("Error saving task:", xhr.responseText);
            }
        }
    };
    let data = JSON.stringify({
        name: taskName,
        description: taskDescription,
        status: taskStatus
    });
    xhr.send(data);
}


function editTask() {
    let saveButton = document.getElementById("save-button");
    let editButton = document.getElementById("edit-button");
    if (saveButton.style.display === "none") {
        saveButton.style.display = "block";
        editButton.style.display = "none";
    } else {
        saveButton.style.display = "none";
        editButton.style.display = "block";
    }
}
        