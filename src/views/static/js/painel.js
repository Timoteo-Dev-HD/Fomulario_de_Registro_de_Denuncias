function toggleCard(id) {
    const details = document.getElementById(`details-${id}`);
    const seta = document.getElementById(`seta-${id}`);

    details.classList.toggle("open");

    seta.style.transform = details.classList.contains("open")
        ? "rotate(180deg)"
        : "rotate(0deg)";
}

function salvarDenuncia(btn) {
    const denunciaId = btn.getAttribute("data-id");

    const form = btn.closest(".form-analise");

    const status = form.querySelector("[name='status']").value;

    const depoimentoVitima = form.querySelector("[name='depoimento_vitima']").value;
    const depoimentoAcusado = form.querySelector("[name='depoimento_acusado']").value;
    const depoimentoTestemunha = form.querySelector("[name='depoimento_testemunha']").value;
    const depoimentoAdmin = form.querySelector("[name='depoimento_admin']").value;

    const dados = {
        status: status,
        depoimento_vitima: depoimentoVitima,
        depoimento_acusado: depoimentoAcusado,
        depoimento_testemunha: depoimentoTestemunha,
        depoimento_admin: depoimentoAdmin
    };

    fetch(`/admin/denuncia/${denunciaId}/atualizar`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content
        },
        body: JSON.stringify(dados)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);

        if (data.sucesso) {
            alert("Denúncia atualizada com sucesso!");
            window.location.reload();
        } else {
            alert(data.mensagem || "Erro ao atualizar denúncia.");
        }
    })
    .catch(error => {
        console.error("Erro:", error);
        alert("Erro ao atualizar denúncia. Veja o console.");
    });
}