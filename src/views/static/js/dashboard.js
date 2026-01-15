// ============================
// KPIs
// ============================

document.getElementById("totalDenuncias").innerText = 1125;
document.getElementById("emAndamento").innerText = 48;
document.getElementById("foraSla").innerText = 7;

// ============================
// GRÁFICO MENSAL
// ============================

new Chart(document.getElementById('graficoMes'), {
  type: 'bar',
  data: {
    labels: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
    datasets: [{
      label: 'Total de Denúncias',
      data: [120, 90, 150, 80, 200, 170, 50, 40, 85, 10, 24, 97],
      borderWidth: 1
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: { beginAtZero: true }
    }
  }
});

// ============================
// DENÚNCIAS POR GÊNERO
// ============================

new Chart(document.getElementById("graficoDoughnut"), {
  type: 'doughnut',
  data: {
    labels: ['Mulher', 'Homem', 'Outros'],
    datasets: [{
      data: [100, 40, 10],
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)'
      ]
    }]
  }
});

// ============================
// DENÚNCIAS POR TIPO
// ============================

new Chart(document.getElementById("graficoPizzaTipo"), {
  type: 'pie',
  data: {
    labels: ['Assédio', 'Fraude', 'Discriminação', 'Outros'],
    datasets: [{
      data: [45, 25, 20, 10],
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(153, 102, 255)',
        'rgb(201, 203, 207)'
      ]
    }]
  }
});

// ============================
// STATUS DAS DENÚNCIAS
// ============================

new Chart(document.getElementById("graficoStatus"), {
  type: 'bar',
  data: {
    labels: ['Recebidas', 'Em análise', 'Investigação', 'Encerradas'],
    datasets: [{
      label: 'Quantidade',
      data: [30, 18, 12, 65],
      borderWidth: 1
    }]
  },
  options: {
    indexAxis: 'y',
    scales: {
      x: { beginAtZero: true }
    }
  }
});
