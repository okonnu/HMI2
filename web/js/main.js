// document.addEventListener('contextmenu', event => event.preventDefault());

var visitData = ["", ""];

var myChart = new Chart(document.getElementById('mychart'), {
    type: 'doughnut',
    data: {
        labels: ["Efficiency", ""],
        datasets: [{
            label: 'Visitor',
            data: ["20", "80"],
            backgroundColor: [
                "#a2d6c4",
                "transparent"
            ]
        }]
    },
    options: {
        responsive: true,
        legend: false,
        animation: {
            duration: 0
        }
    }
});

function addData(data) {
    alt = 100 - data
    if (alt < 1) { alt = 0 }
    vals = [data, alt]
    myChart.data.datasets = [{
        label: 'Visitor',
        data: vals,
        backgroundColor: [
            "#a2d6c4",
            "transparent"
        ]
    }]
    document.getElementById('efficiency').innerHTML = data + '%'
    myChart.update(0);
}

function openmodal() {
    $('#passwordmodal').modal('show')
}


// setInterval(function() {
//     var data1 = (Math.floor((Math.random() * 100) + 1));
//     addData(data1)

// }, 500);



// $(window).load(function() {
//     // $('#actv').click()
//    
// });
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('actv').click()
});

function updatetarget() {
    const tgt = document.getElementById('ftarget').value
    document.getElementById('rangee').innerHTML = tgt
}

$('#submit').click(function() {

    const fclient_id = document.getElementById("fclient_id").value;
    const fteam = document.getElementById("fteam").value;
    const fcanspercase = document.getElementById("fcanspercase").value;
    const ftarget = document.getElementById("ftarget").value;

    eel.set_pyconfigs(fclient_id, fteam, fcanspercase, ftarget)
        // alert('settings saved successfully')
    document.getElementById('actv').click()
});

// retrieve settings from python, and save on js
eel.expose(set_jsconfigs);

function set_jsconfigs(client_id, team, canspercase, target, shift) {
    // client title
    document.getElementById('client_id').innerHTML = client_id.replace(/^\D+/g, '');
    //team
    document.getElementById("team").innerHTML = team
        //shift
    document.getElementById("shift").innerHTML = shift

}

eel.expose(set_eff);

function set_eff(effic) {
    // efficiency
    console.log(effic)
    addData(effic)
}

eel.expose(set_metrics);

function set_metrics(s_cans, s_cases, damages, downtime) {

    //seamed cans
    document.getElementById("s_cans").innerHTML = s_cans

    //seamed cases 
    document.getElementById("s_cases").innerHTML = s_cases

    //damaged cans
    document.getElementById("damages").innerHTML = damages

    //downtime
    document.getElementById("downtime").innerHTML = downtime

}