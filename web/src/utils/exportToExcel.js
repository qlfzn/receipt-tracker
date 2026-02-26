import * as XLSX from "xlsx"

const toRows = (transactions) =>
  transactions.map((t) => ({
    Date: t.date,
    Transaction: t.transaction,
    Amount: t.amount,
    Description: t.description ?? "",
    Category: t.is_direct ? "DIRECT" : "TOYYIBPAY",
  }))

export const exportTransactionsToExcel = (transactions, filename = "transactions") => {
  const credits = transactions.filter((t) => t.amount > 0)
  const debits = transactions.filter((t) => t.amount < 0)

  const creditSheet = XLSX.utils.json_to_sheet(toRows(credits))
  const debitSheet = XLSX.utils.json_to_sheet(toRows(debits))

  const workbook = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(workbook, creditSheet, "Credit")
  XLSX.utils.book_append_sheet(workbook, debitSheet, "Debit")

  XLSX.writeFile(workbook, `${filename}.xlsx`)
}
