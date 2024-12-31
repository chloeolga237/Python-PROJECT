import { jsPDF } from "jspdf";
import html2canvas from "html2canvas";

export function exportBracket() {
  const bracketElement = document.querySelector(".bracket");
  html2canvas(bracketElement).then((canvas) => {
    const pdf = new jsPDF();
    const imgData = canvas.toDataURL("image/png");
    pdf.addImage(imgData, "PNG", 10, 10, 180, 160);
    pdf.save("bracket.pdf");
  });
}
