function toggleCard(id) {
    const details = document.getElementById(`details-${id}`);
    const seta = document.getElementById(`seta-${id}`);

    details.classList.toggle("open");

    seta.style.transform = details.classList.contains("open")
        ? "rotate(180deg)"
        : "rotate(0deg)";
}
