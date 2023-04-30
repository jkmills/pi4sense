// Connect to the Socket.IO server
var socket = io();

// Update the sensor data table with a new value
function updateTable(selector, value, units = '') {
    $(selector).fadeOut(200, function() {
        $(this).html(value + units);
        $(this).fadeIn(200);
    });
}

// Update the orientation indicators with a new roll, pitch, or yaw value
function drawRollIndicator(roll) {
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    var centerX = canvas.width / 2;
    var centerY = canvas.height / 2;
    var radius = 50;
    var startAngle = -Math.PI / 2;
    var endAngle = startAngle + (roll / 180) * Math.PI;

    // Clear the canvas
    context.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the background circle
    context.beginPath();
    context.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
    context.lineWidth = 10;
    context.strokeStyle = '#ccc';
    context.stroke();

    // Draw the indicator arc
    context.beginPath();
    context.arc(centerX, centerY, radius, startAngle, endAngle, false);
    context.lineWidth = 10;
    context.strokeStyle = '#f00';
    context.stroke();
}

function drawPitchIndicator(pitch) {
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    var centerX = canvas.width / 2;
    var centerY = canvas.height / 2;
    var radius = 50;
    var startAngle = Math.PI / 2;
    var endAngle = startAngle + (pitch / 180) * Math.PI;

    // Draw the indicator arc
    context.beginPath();
    context.arc(centerX, centerY, radius, startAngle, endAngle, false);
    context.lineWidth = 10;
    context.strokeStyle = '#0f0';
    context.stroke();
}

function drawYawIndicator(yaw) {
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    var centerX = canvas.width / 2;
    var centerY = canvas.height / 2;
    var radius = 50;
    var startAngle = 0;
    var endAngle = startAngle + (yaw / 180) * Math.PI;

    // Draw the indicator arc
    context.beginPath();
    context.arc(centerX, centerY, radius, startAngle, endAngle, false);
    context.lineWidth = 10;
    context.strokeStyle = '#00f';
    context.stroke();
}

// Listen for the 'sensor-data' event
socket.on('sensor-data', function(data) {
    // Update the sensor data table
    updateTable('#temperature', data.temperature, '°C');
    updateTable('#humidity', data.humidity, '%');
    updateTable('#pressure', data.pressure, 'hPa');
    updateTable('#datetime', data.datetime);

    // Update the orientation indicators
    drawRollIndicator(data.roll);
    drawPitchIndicator(data.pitch);
    drawYawIndicator(data.yaw);
});

// Listen for the 'orientation-data' event
socket.on('orientation-data', function(data) {
    // Update the orientation table
    updateTable('#roll', data.roll, '°');
    updateTable('#pitch', data.pitch, '°');
    updateTable('#yaw', data.yaw, '°');
});
