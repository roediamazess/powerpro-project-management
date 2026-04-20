/**
 * The PowerPro Data Export Utility (v2.3)
 * Handles CSV and Specialized PDF Printing
 */

export const exportToCSV = (data: any[], filename: string) => {
  if (data.length === 0) return

  // 1. Get headers from the first object
  const headers = Object.keys(data[0])
  const csvRows = []

  // 2. Add header row
  csvRows.push(headers.join(','))

  // 3. Add data rows
  for (const row of data) {
    const values = headers.map(header => {
      const val = row[header]
      const escaped = ('' + val).replace(/"/g, '""')
      return `"${escaped}"`
    })
    csvRows.push(values.join(','))
  }

  // 4. Create Blob and Download
  const csvString = csvRows.join('\n')
  const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  
  link.setAttribute('href', url)
  link.setAttribute('download', `${filename}.csv`)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

export const printToPDF = () => {
  /**
   * Leverages browser's print engine.
   * In conjunction with @media print CSS rules in main.css
   */
  window.print()
}
