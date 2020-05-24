// Results page
// HTTP request to get user exercise graph
function getGraph(userId) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() { 
        if (this.readyState == 4 && this.status == 200) {
        const myData = JSON.parse(this.responseText);
        exerciseGraph(myData);
        }
    };
    let url = "http://localhost:5000/api/users/" + userId + "/exercise/time_graph";
    xhttp.open("GET", url, true);
    xhttp.send();
  }

// Creates graph for personal profile
function exerciseGraph(arr) {
    let ctx = document.getElementById("barChart").getContext('2d');
    let style = [];
    let time = [];
    for (x in arr) {
        style.push(arr[x].style);
        time.push(arr[x].time);
    }

    var barChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: style,
            datasets: [{
                label: "Time",
                data: time,
                backgroundColor: [
                    "#331E36",
                    "#A5FFD6"
                ],
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
        
    });
};

// Creates graph for groups page
// 

function getGroupGraph() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() { 
        if (this.readyState == 4 && this.status == 200) {
        const myData = JSON.parse(this.responseText);
        exerciseGroupGraph(myData);
        }
    };
    let url = "http://localhost:5000//api/users/all/exercise";
    xhttp.open("GET", url, true);
    xhttp.send();
  }


function exerciseGroupGraph(arr) {
    let ctx = document.getElementById("chart").getContext('2d');
    let user = [];
    for (x in arr) {
        user.push(arr[x].username);
    }

    ///Creates a unique array of users
    var uniqueusers = [];
    var count = 0;
    var found = false;

    for (i=0;i<user.length;i++){
        for (y = 0; y<uniqueusers.length; y++){
            if(user[i] == uniqueusers[y]){
                found = true;
            }
        }
        count++;
        if(count == 1 && found ==false){
            uniqueusers.push(user[i]);
        }
        count=0;
        found = false;
    }
    
    ///Creates array counts with the number of times the user has exercised
    var counts = [];
    for (i=0;i<uniqueusers.length;i++){
        tally = 0
        for (y = 0; y<user.length; y++){
            if (uniqueusers[i] == user[y]){
                tally++;
            }
        }
        counts.push(tally)
    }

    var barChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: uniqueusers,
            datasets: [{
                label: "Number of Exercises",
                data: counts,
                backgroundColor: [
                    "#331E36",
                    "#A5FFD6",
                    "#331E36",
                    "#A5FFD6"
                ],
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
        
    });

};


function fastestRunData() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() { 
        if (this.readyState == 4 && this.status == 200) {
        const myData = JSON.parse(this.responseText);
        fastestRunGraph(myData);
        }
    };
    let url = "http://localhost:5000//api/users/all/exercise";
    xhttp.open("GET", url, true);
    xhttp.send();
  }

function fastestRunGraph(arr) {
    let ctx = document.getElementById("chart2").getContext('2d');
    let user = [];
    let time = [];
    let distance = [];
    let speed = [];

    for (x in arr) {
        user.push(arr[x].username);
        time.push(parseFloat(arr[x].time));
        distance.push(parseFloat(arr[x].distance));
    }
    for (i=0;i<user.length;i++){
        speed.push(time[i]/distance[i])
    }

    ///Creates a unique array of users
    var uniqueusers = [];
    var count = 0;
    var found = false;

    for (i=0;i<user.length;i++){
        for (y = 0; y<uniqueusers.length; y++){
            if(user[i] == uniqueusers[y]){
                found = true;
            }
        }
        count++;
        if(count == 1 && found ==false){
            uniqueusers.push(user[i]);
        }
        count=0;
        found = false;
    }

    
    

    var barChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: user,
            datasets: [{
                label: "Mintues per KM",
                data: speed,
                backgroundColor: [
                    "#331E36",
                    "#A5FFD6",
                    "#331E36",
                    "#A5FFD6"
                ],
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
        
    });

};
       