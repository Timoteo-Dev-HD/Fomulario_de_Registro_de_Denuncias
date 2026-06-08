async function carregarDashboard() {
  try {
    const response = await fetch(`/admin/meses-denuncias`);
    const dados = await response.json()    

    const dadosMes = [
      dados.Jan, dados.Fev, dados.Mar, dados.Abr,
      dados.Mai, dados.Jun, dados.Jul, dados.Ago,
      dados.Set, dados.Out, dados.Nov, dados.Dez
    ];

    // GRÁFICO MENSAL
    new Chart(document.getElementById("graficoMes"), {
        type: "bar",
        data: {
        labels: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
                "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
        datasets: [{
        label: "Total de Denúncias",
        data: dadosMes,
        borderWidth: 1
              }]
        },
        options: {
        responsive: true,
        scales: { y: { beginAtZero: true } }
        }
    });

    const response1 = await fetch(`/admin/filter/quantidade_status`);
    const dados1 = await response1.json()

    const dadosStatus = [
      dados1.pendente, dados1.em_analise,
      dados1.suspenso, dados1.encerrada
    ]

    // ============================
    // STATUS DAS DENÚNCIAS
    // ============================

    new Chart(document.getElementById("graficoStatus"), {
      type: 'bar',
      data: {
        labels: ['Pendente', 'Em análise', 'Suspenso', 'Encerradas'],
        datasets: [{
          label: 'Quantidade',
          data: dadosStatus,
          borderWidth: 1,
          backgroundColor: [
            'rgb(240, 180, 0)',
            'rgb(0, 80, 200)',
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



  } catch (error) {
    console.error("Erro ao carregar dashboard:", error);
  }

}

carregarDashboard();

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

// // ============================
// // DENÚNCIAS POR TIPO
// // ============================

// new Chart(document.getElementById("graficoPizzaTipo"), {
//   type: 'pie',
//   data: {
//     labels: ['Assédio', 'Fraude', 'Discriminação', 'Outros'],
//     datasets: [{
//       data: [45, 25, 20, 10],
//       backgroundColor: [
//         'rgb(255, 99, 132)',
//         'rgb(54, 162, 235)',
//         'rgb(153, 102, 255)',
//         'rgb(201, 203, 207)'
//       ]
//     }]
//   }
// });

