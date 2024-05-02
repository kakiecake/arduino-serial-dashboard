const ctx = document.getElementById("chart");
let chart = null;

const createChart = (yValues) => {
    const xValues = [...Array(yValues.length)].map((_, i) => i);

    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: xValues,
            datasets: [
                {
                    label: "vibration",
                    data: yValues,
                },
            ],
        },
        options: {
            scales: {
                y: {
                    min: 0,
                    max: 1,
                },
            },
        },
    });
};

createChart([...Array(120)].map((_) => 0));

document.addEventListener("dataUpdated", (ev) => {
    const vibrationValue = Number(ev.detail["has_vibration"]);
    const labels = chart.data.labels;
    const chartData = chart.data.datasets[0].data;
    labels.push(chart.data.labels[chart.data.labels.length - 1] + 1);
    chartData.push(vibrationValue);
    labels.shift();
    chartData.shift();
    chart.update();
});
