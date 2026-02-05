// ============================
// KPIs
// ============================

// document.getElementById("totalDenuncias").innerText = 1125;
// document.getElementById("emAndamento").innerText = 48;
// document.getElementById("foraSla").innerText = 7;

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
    labels: ['Baixo', 'Médio', 'Alta', 'Crítica'],
    datasets: [{
      data: [150,80, 35, 13],
      backgroundColor: [
        'rgb(3, 188, 169)',
        'rgb(255, 193, 7)',
        'rgb(255, 152, 0)',
        'rgb(244, 67, 54)'
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
      borderWidth: 1,
      backgroundColor: [
        'rgb(0, 80, 200)',
        'rgb(240, 180, 0)',
        'rgb(255, 130, 0)',
        'rgb(30, 160, 60)'
      ]
    }]
  },
  options: {
    indexAxis: 'y',
    scales: {
      x: { beginAtZero: true }
    }
  }
});
