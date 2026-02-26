import { useMemo, useState } from "react"
import { Badge, Button, Box, Grid, Input, NativeSelect, Table, Text } from "@chakra-ui/react"
import { exportTransactionsToExcel } from "../utils/exportToExcel"

const fmt = (amount) =>
  `RM ${Math.abs(amount).toLocaleString("en-MY", { minimumFractionDigits: 2 })}`

const COLUMNS = [
  { key: "date", label: "Date" },
  { key: "transaction", label: "Transaction" },
  { key: "amount", label: "Amount", align: "right" },
  { key: "description", label: "Description" },
  { key: "category", label: "Category" },
]

const sortRows = (rows, key, dir) => {
  if (!key) return rows
  return [...rows].sort((a, b) => {
    let av = a[key] ?? ""
    let bv = b[key] ?? ""
    if (key === "amount") return dir === "asc" ? av - bv : bv - av
    if (key === "category") {
      av = a.is_direct ? "DIRECT" : "TOYYIBPAY"
      bv = b.is_direct ? "DIRECT" : "TOYYIBPAY"
    }
    return dir === "asc"
      ? String(av).localeCompare(String(bv))
      : String(bv).localeCompare(String(av))
  })
}

const SortIcon = ({ active, dir }) => (
  <Text as="span" ml={1} color={active ? "gray.700" : "gray.300"} fontSize="10px">
    {active ? (dir === "asc" ? "▲" : "▼") : "▲▼"}
  </Text>
)

const TransactionSubTable = ({ transactions, title, colorScheme }) => {
  const [sortKey, setSortKey] = useState("date")
  const [sortDir, setSortDir] = useState("asc")

  const handleSort = (key) => {
    if (key === sortKey) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"))
    } else {
      setSortKey(key)
      setSortDir("asc")
    }
  }

  const sorted = useMemo(() => sortRows(transactions, sortKey, sortDir), [transactions, sortKey, sortDir])

  const total = transactions.reduce((sum, t) => sum + Math.abs(t.amount), 0) 

  return (
  <Box
    bg="white"
    border="1px solid"
    borderColor="gray.200"
    borderRadius="lg"
    overflow="hidden"
    minW={0}
  >
    <Box px={4} py={2} borderBottom="1px solid" borderColor="gray.100" display="flex" justifyContent="space-between" alignItems="baseline">
      <Text fontWeight="semibold" fontSize="sm" color={colorScheme === "green" ? "green.600" : "red.600"}>
        {title} <Text as="span" color="gray.400" fontWeight="normal">({transactions.length} rows)</Text>
      </Text>
      <Text fontSize="xs" color="gray.500">
        Total: <Text as="span" fontWeight="medium" color="gray.700">{fmt(total)}</Text>
      </Text>
    </Box>

    <Box maxH="60vh" overflowY="auto" overflowX="auto">
      <Table.Root size="sm">
        <Table.Header>
          <Table.Row bg="gray.50">
            {COLUMNS.map((col) => (
              <Table.ColumnHeader
                key={col.key}
                color="gray.500"
                fontWeight="medium"
                py={3}
                px={3}
                position="sticky"
                top={0}
                bg="gray.50"
                zIndex={1}
                whiteSpace="nowrap"
                textAlign={col.align ?? "left"}
                cursor="pointer"
                userSelect="none"
                _hover={{ color: "gray.700" }}
                onClick={() => handleSort(col.key)}
              >
                {col.label}
                <SortIcon active={sortKey === col.key} dir={sortDir} />
              </Table.ColumnHeader>
            ))}
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {sorted.length === 0 ? (
            <Table.Row>
              <Table.Cell colSpan={5} py={6} textAlign="center" color="fg.disabled" fontSize="sm">
                No transactions found
              </Table.Cell>
            </Table.Row>
          ) : (
            sorted.map((t, i) => (
              <Table.Row key={i} bg="white" _hover={{ bg: "gray.50" }}>
                <Table.Cell py={3} px={3} color="gray.500" fontSize="sm" whiteSpace="nowrap">{t.date}</Table.Cell>
                <Table.Cell py={3} px={3} fontSize="sm" maxW="180px">
                  <Text color="gray.900" truncate title={t.transaction}>{t.transaction}</Text>
                </Table.Cell>
                <Table.Cell py={3} px={3} textAlign="right" fontWeight="medium" whiteSpace="nowrap">
                  <Text color={t.amount > 0 ? "green.600" : "red.600"} fontSize="sm">
                    {t.amount > 0 ? "+" : "-"}{fmt(t.amount)}
                  </Text>
                </Table.Cell>
                <Table.Cell py={3} px={3} color="gray.600" fontSize="sm" maxW="200px">
                  <Text truncate title={t.description}>{t.description ?? "—"}</Text>
                </Table.Cell>
                <Table.Cell py={3} px={3}>
                  <Badge size="sm" colorPalette={t.is_direct ? "blue" : "yellow"} variant="solid">
                    {t.is_direct ? "DIRECT" : "TOYYIBPAY"}
                  </Badge>
                </Table.Cell>
              </Table.Row>
            ))
          )}
        </Table.Body>
      </Table.Root>
    </Box>
  </Box>
  )
}

const TransactionsTable = ({ transactions }) => {
  const [search, setSearch] = useState("")
  const [category, setCategory] = useState("all")

  const filtered = useMemo(() => {
    const q = search.toLowerCase()
    return transactions.filter((t) => {
      const matchesSearch =
        !q ||
        t.transaction.toLowerCase().includes(q) ||
        (t.description ?? "").toLowerCase().includes(q)
      const matchesCategory =
        category === "all" ||
        (category === "direct" && t.is_direct) ||
        (category === "toyyibpay" && !t.is_direct)
      return matchesSearch && matchesCategory
    })
  }, [transactions, search, category])

  const credits = filtered.filter((t) => t.amount > 0)
  const debits = filtered.filter((t) => t.amount < 0)

  return (
    <Box display="flex" flexDirection="column" gap={4}>
      {/* Controls */}
      <Box display="flex" gap={3} alignItems="center">
        <Input
          placeholder="Search transactions..."
          size="sm"
          bg="white"
          flex="1"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <NativeSelect.Root size="sm" w="160px" bg="white">
          <NativeSelect.Field value={category} onChange={(e) => setCategory(e.target.value)}>
            <option value="all">All Categories</option>
            <option value="direct">Direct</option>
            <option value="toyyibpay">ToyyibPay</option>
          </NativeSelect.Field>
          <NativeSelect.Indicator />
        </NativeSelect.Root>
        <Button
          size="sm"
          colorPalette="green"
          variant="solid"
          flexShrink={0}
          onClick={() => exportTransactionsToExcel(filtered, "transactions")}
        >
          Export to Excel
        </Button>
      </Box>

      {/* Tables side by side */}
      <Grid templateColumns="1fr 1fr" gap={4}>
        <TransactionSubTable transactions={credits} title="Credit" colorScheme="green" />
        <TransactionSubTable transactions={debits} title="Debit" colorScheme="red" />
      </Grid>
    </Box>
  )
}

export default TransactionsTable