document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.getElementById("menu-toggle");
  const closeBtn = document.getElementById("close-btn");

  // التعامل مع قائمة التنقل
  menuToggle.addEventListener("click", () => {
    document.querySelector(".navbar").classList.toggle("active");
  });

  // تخزين البيانات في الأرشيف
  function addDataToArchive(predictedInfo, value) {
    const currentDate = new Date().toLocaleString();
    const archiveData = JSON.parse(localStorage.getItem("dataArchive")) || [];
    archiveData.push({ predictedInfo, value, date: currentDate });
    localStorage.setItem("dataArchive", JSON.stringify(archiveData));
  }

  // عرض البيانات
  function displayData() {
    const archiveData = JSON.parse(localStorage.getItem("dataArchive")) || [];
    const tableBody = document.getElementById("data-table-body");
    tableBody.innerHTML = "";

    archiveData.forEach((data) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${data.predictedInfo}</td>
        <td>${data.value}</td>
        <td>${data.date}</td>
      `;
      tableBody.appendChild(row);
    });
  }

  displayData();
});
