// Results page
// HTTP request to get user exercise graph
function getGraph(userId) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() { 
        if (this.readyState == 4 && this.status == 200) {
        const myData = JSON.parse(this.responseText);
        exerciseGraph(myData);
        runningSpeedGraph(myData);
        }
    };
    let url = "http://localhost:5000/api/users/" + userId + "/exercise/graphs";
    xhttp.open("GET", url, true);
    xhttp.send();
  }

// Creates total exercise graph for personal profile
function exerciseGraph(arr) {
    let ctx = document.getElementById("barChart").getContext('2d');
    let walktime = 0;
    let runtime = 0;
    for (x in arr) {
        if (arr[x].style == "Walk") {
            walktime += parseFloat(arr[x].time);
        } else if (arr[x].style == "Run") {
            runtime += parseFloat(arr[x].time);
        }
    }

    var barChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Run", "Walk"],
            datasets: [{
                data: [runtime, walktime],
                backgroundColor: ["#331E36", "#A5FFD6"],
                }]
        },
        options: {
            title: {
                display: true,
                text: "Your total exercise to-date"
            },
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Minutes'
                    },
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
        
    });
};
// Creates running speed graph for personal profile
function runningSpeedGraph(arr) {
    let ctx = document.getElementById("runningSpeed").getContext('2d');
    let dates = []
    let speeds = []
    for (x in arr) {
        if (arr[x].style == "Run") {
            dates.push(arr[x].exercise_date);
            speeds.push(arr[x].speed);
        }
    }
    dates.sort();

    var lineChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: dates,
            datasets: [{
                data: speeds,
                borderColor: "#1F7A8C",
                lineTension: 0,
                }]
        },
        options: {
            title: {
                display: true,
                text: "Your running speed over time"
            },
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Mins per kilometre'
                    },
                    ticks: {
                        beginAtZero: true
                    }
                }],
            },
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
       