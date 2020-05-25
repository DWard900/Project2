// Admin View
// HTTP request to token API to get token
function adminSignIn(data) {
    const xhttp = new XMLHttpRequest();
    b64 = btoa(data);
    xhttp.onreadystatechange = function() { 
        if (this.readyState == 4 && this.status == 200) {
          responseData = JSON.parse(this.responseText);
          authToken = responseData['token'];
          getUsers(authToken);
        }
    };
    xhttp.open("POST", "http://localhost:5000/api/tokens");
    xhttp.setRequestHeader("Authorization", "Basic " + b64);
    xhttp.send(data);
}

// HTTP request to get users
function getUsers(token) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() { 
        if (this.readyState == 4 && this.status == 200) {
        const myData = JSON.parse(this.responseText);
        userTable(myData);
        }
    };
    let bearer = "Bearer " + token;
    xhttp.open("GET", "http://localhost:5000/api/users");
    xhttp.setRequestHeader("Authorization", bearer);
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
  let url = "api/users/" + userId + "/exercise";
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

// HTTP request to get exercise on user page
function getUserExercise(userId) {
  const xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() { 
      if (this.readyState == 4 && this.status == 200) {
      const myData = JSON.parse(this.responseText);
      exerciseList(myData);
      }
  };
  let url = "http://127.0.0.1:5000/api/users/" + userId + "/exercise";
  xhttp.open("GET", url, true);
  xhttp.send();
}

// Creates list of exercises for user page
function exerciseList(arr) {
  let header = "<h3>Your exercises</h3><br>";
  exerciseText = ""

  for (x in arr) {
      let exerciseId = arr[x].id;
      let style = arr[x].style;
      if (style == "Run") {
        imgURL = "<img src='/static/assets/running-small.png' id='run-small'>"
      } else {
        imgURL = "<img src='/static/assets/walk-small.png' id='walk-small'>"
      }
      let time = arr[x].time;
      let distance = arr[x].distance;
      let date = arr[x].exercise_date;
      let speed = arr[x].speed;
      let rating = arr[x].rate_exercise;
      let comment = arr[x].exercise_comments;
      let deleteURL = "http://localhost:5000/delete_post/" + exerciseId;
      
      exerciseText += '<div class="exercise-text"> \
                      <br> \
                      <p>Date: <b>' + date + '</b></p> \
                      <p><span>' + imgURL + '</span>Type of exercise: <b>' + style + '</b><span>' + imgURL + '</span></p> \
                      <p>Time: <b>' + time + '</b> minutes</p> \
                      <p>Distance: <b>' + distance + '</b> kilometres</p> \
                      <p>Speed: <b>' + speed + '</b> minutes per kilometre</p> \
                      <p>Your rating: <b>' + rating + '</b> out of 10<p> \
                      <pYour comment: <b>' + comment + '</b></p> \
                      <p><form action ="' + deleteURL + '" method="post", class="del-button" style="display: none;"> \
                        <input type="submit" value="Delete" class="btn btn-danger"></form></p> \
                      <br> \
                      </div> \
                      <br>'
   }
   html = header + exerciseText
   document.getElementById("user-exercise-list").innerHTML = html;
};


// User and Message Page - show hidden delete buttons when clicking Toggle Delete Buttons
function showDeleteButton() {
  let elements = document.getElementsByClassName('del-button')
  for ( let x of elements) {
    if (x.style.display == "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }
}

