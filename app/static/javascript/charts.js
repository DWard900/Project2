// Results page
// HTTP request to get user exercise graph
function getGraph(userId) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() { 
        if (this.readyState == 4 && this.status == 200) {
        const myData = JSON.parse(this.responseText);
        exerciseGraph(myData);
        runningSpeedGraph(myData);
        distanceGraph(myData);
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
                fill: false
                }]
        },
        options: {
            title: {
                display: true,
                text: "Minutes per kilometre for runs over time"
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

// Creates total distance graph for personal profile
function distanceGraph(arr) {
    let ctx = document.getElementById("distance").getContext('2d');
    let distanceList = [];
    for (x in arr) {
        date = arr[x].exercise_date;
        if (date in distanceList) {
            oldDistance = distanceList[date];
            newDistance = oldDistance + parseFloat(arr[x].distance);
            distanceList[date] = newDistance;
        } else {
            let distance = parseFloat(arr[x].distance)
            distanceList[date] = distance;
        }
    }

    let entries = Object.entries(distanceList);
    entries.sort();
    let dateList = [];
    let distances = [];
    let total_dist = 0;
    for (i=0; i < entries.length; i++) {
        dateList.push(entries[i][0]);
        total_dist += entries[i][1];
        distances.push(total_dist);
    }

    var lineChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: dateList,
            datasets: [{
                data: distances,
                borderColor: "#331E36",
                lineTension: 0,
                }]
        },
        options: {
            title: {
                display: true,
                text: "Total cumulative distance of exercises"
            },
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Distance in km'
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

    var backgroundColors = [];
    for (i=0;i<uniqueusers.length;i++){
        if (i % 2 === 0) {
            backgroundColors.push("#331E36")
        } else {
            backgroundColors.push("#A5FFD6")
        }
    }

    var barChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: uniqueusers,
            datasets: [{
                label: "Number of Exercises",
                data: counts,
                backgroundColor: backgroundColors
            }]
        },
        options: {
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Number of exercises'
                    },
                    ticks: {
                        beginAtZero: true,
                        callback: function(value) {if (value % 1 === 0) {return value;}}
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

    fastestruns=[]

    ////select fastest
    for (y = 0; y<uniqueusers.length; y++){
        fastest = 100000 
        for (i=0;i<user.length;i++){
            if ( uniqueusers[y] == user[i]){
                if ( speed[i] < fastest){
                    fastest = speed[i]
                }
            }

        }
        fastestruns.push(fastest)
    }


    var barChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: uniqueusers,
            datasets: [{
                label: "Minutes per km",
                data: fastestruns,
                backgroundColor: [
                    "#331E36",
                    "#A5FFD6",
                    "#331E36",
                    "#A5FFD6"
                ],
            }]
        },
        options: {
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
                }]
            }
        }
        
    });

};


function exerciseTime() {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() { 
        if (this.readyState == 4 && this.status == 200) {
        const myData = JSON.parse(this.responseText);
        exerciseTimeGraph(myData);
        }
    };
    let url = "http://localhost:5000//api/users/all/exercise";
    xhttp.open("GET", url, true);
    xhttp.send();
  }

function exerciseTimeGraph(arr) {
    let ctx = document.getElementById("chart3").getContext('2d');
    let user = [];
    let speed = [];

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
     data = []
     dates=[]
    
    for (i=0;i<uniqueusers.length;i++){
        userdata = []
        userdata.push(uniqueusers[i]);
        for (b=0;b<arr.length;b++){
            if (uniqueusers[i] == arr[b].username ){
                temp = []
                temp.push(arr[b].date)
                dates.push(arr[b].date)
                temp.push(arr[b].distance)
                userdata.push(temp)
                }
            }
        data.push(userdata)
        }
        dates.sort()


        var uniquedates = [];
        
        ///Create Unique Dates from list
        for (i=0;i<dates.length;i++){
            for (y = 0; y<uniquedates.length; y++){
                if(dates[i] == uniquedates[y]){
                    found = true;
                }
            }
            count++;
            if(count == 1 && found ==false){
                uniquedates.push(dates[i]);
            }
            count=0;
            found = false;
        }

  

        DistanceData = []

        for (i=0;i<uniqueusers.length;i++){
            console.log(uniqueusers[i])
            counter=0
            userDisArray = [] 
            for (a=0;a<uniquedates.length;a++){
                for (b=0;b<arr.length;b++){
                    if (uniquedates[a] == arr[b].date && uniqueusers[i] == arr[b].username ) {
                        counter += parseFloat(arr[b].distance)
                    }
                }
                userDisArray.push(counter)
            }
            DistanceData.push(userDisArray)
        }
        console.log(DistanceData)
        
        colours = ["red","green","yellow","blue","white"];

        
        datasets = []

        for (i=0;i<uniqueusers.length;i++){
            dic = {
                label: uniqueusers[i], 
                data: DistanceData[i], 
                borderColor: colours[i],
                fill: false,
                lineTension: 0,
            }
        datasets.push(dic)
        }


    var barChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: uniquedates,
            datasets: datasets
        },
        options: {
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Distance in km'
                    },
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
        
    });

};
       