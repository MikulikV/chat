// Returns current date and time
export function getTimeStamp() {
  const currentDate = new Date();
  const MM = String(currentDate.getMonth() + 1).padStart(2, "0");
  const DD = String(currentDate.getDate()).padStart(2, "0");
  const HH = currentDate.getHours();
  const ampm = HH >= 12 ? "PM" : "AM";
  const H =
    HH > 12 ? String(HH - 12).padStart(2, "0") : String(HH).padStart(2, "0");
  const M = String(currentDate.getMinutes()).padStart(2, "0");
  return `${MM}/${DD} ${H}:${M} ${ampm}`;
}
