const chartEl = document.getElementById("vibration-chart");


const createChart = (chartEl, vibrationValues, relayValues) => {
  const xValues = [...Array(vibrationValues.length)].map((_, i) => i);

  const chart = new Chart(chartEl, {
    type: "line",
    data: {
      labels: xValues,
      datasets: [
        {
          label: "Вибрация",
          data: vibrationValues,
        },
        {
          label: "Распыление",
          data: relayValues,
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

  return chart
};

const initialValues = [...Array(120)].map((_) => 0);
const chart = createChart(chartEl,
  window.__HISTORIC_DATA ? window.__HISTORIC_DATA.vibration : initialValues,
  window.__HISTORIC_DATA ? window.__HISTORIC_DATA.relay : initialValues,
);

const updateChartData = (chart, newVibration, newRelay) => {
  const labels = chart.data.labels;
  labels.push(chart.data.labels[chart.data.labels.length - 1] + 1);
  labels.shift();

  const vibrationData = chart.data.datasets[0].data;
  vibrationData.push(newVibration);
  vibrationData.shift();

  const relayData = chart.data.datasets[1].data;
  relayData.push(newRelay);
  relayData.shift();

  chart.update();
}

document.addEventListener("dataUpdated", (ev) => {
  const vibrationValue = Number(ev.detail["has_vibration"]);
  const isRelayActivated = Number(ev.detail["is_relay_activated"]);
  updateChartData(chart, vibrationValue, isRelayActivated);
});
