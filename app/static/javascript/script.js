// Admin View
// HTTP request to get users
function getUsers() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() { 
        if (this.readyState == 4 && this.status == 200) {
        const myData = JSON.parse(this.responseText);
        userTable(myData);
        }
    };
    xhttp.open("GET", "http://localhost:5000/api/users", true);
    xhttp.send();
}

// Creates header, searchbar, table
function userTable(arr) {
    let searchbar = '<input type="text" id="searchBar" onkeyup="searchFunction()" placeholder="Search by name..."><br>';

    let table = "<br><table id='data-table'><tr><th>User ID</th><th>Username</th><th>Last seen</th><th>Exercise</th></tr>";

    for (x in arr) {
        let userId = arr[x].id;
        let username = arr[x].username;
        let lastSeen = arr[x].last_seen;
        table += "<tr><td>" + userId + "</td><td>" + username + "</td><td>" + lastSeen + "</td><td><button onclick='getExercise(" + userId + ")'>See Exercise</button></td></tr>";
     }
     table += "</table><br>"
     html = searchbar + table
     document.getElementById("user-table").innerHTML = html;
}; 

// Creates search function
function searchFunction() {
    let input = document.getElementById("searchBar");
    let filter = input.value.toUpperCase();
    let dataTable = document.getElementById("data-table");
    tr = dataTable.getElementsByTagName("tr");

    // Loops through all table rows, and hides those that don't match search query
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[1];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

// HTTP request to get user exercise
function getExercise(userId) {
  const xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() { 
      if (this.readyState == 4 && this.status == 200) {
      const myData = JSON.parse(this.responseText);
      exerciseTable(myData);
      }
  };
  let url = "http://localhost:5000/api/users/" + userId + "/exercise";
  xhttp.open("GET", url, true);
  xhttp.send();
}

// Creates header, table
function exerciseTable(arr) {
  let header = "<h3>User exercise</h3><br>";

  let table = "<br><table><tr><th>Exercise ID</th><th>Type</th><th>Time</th><th>Timestamp</th></tr>";

  for (x in arr) {
      let exerciseId = arr[x].id;
      let style = arr[x].style;
      let time = arr[x].time;
      let timestamp = arr[x].timestamp
      table += "<tr><td>" + exerciseId + "</td><td>" + style + "</td><td>" + time + "</td><td>" + timestamp + "</td></tr>";
   }
   table += "</table><br>"
   html = header + table
   document.getElementById("exercise-table").innerHTML = html;
};

// User Page - show buttons
function showDeleteButton() {
  let elements = document.getElementsByClassName('test')
  console.log(elements)
  for (x in elements) {
    if (x.style.display == "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }
}