import { Badge, Box, Table, Text } from "@chakra-ui/react"

const fmt = (amount) =>
  `RM ${Math.abs(amount).toLocaleString("en-MY", { minimumFractionDigits: 2 })}`

const TransactionsTable = ({ transactions }) => (
  <Box
    bg="white"
    border="1px solid"
    borderColor="gray.200"
    borderRadius="lg"
    overflow="hidden"
  >
    <Box maxH="400px" overflowY="auto">
      <Table.Root size="sm">
        <Table.Header>
          <Table.Row bg="gray.50">
            <Table.ColumnHeader color="gray.500" fontWeight="medium" py={3} px={4} position="sticky" top={0} bg="gray.50" zIndex={1}>Date</Table.ColumnHeader>
            <Table.ColumnHeader color="gray.500" fontWeight="medium" py={3} px={4} position="sticky" top={0} bg="gray.50" zIndex={1}>Transaction</Table.ColumnHeader>
            <Table.ColumnHeader color="gray.500" fontWeight="medium" py={3} px={4} textAlign="right" position="sticky" top={0} bg="gray.50" zIndex={1}>Amount</Table.ColumnHeader>
            <Table.ColumnHeader color="gray.500" fontWeight="medium" py={3} px={4} position="sticky" top={0} bg="gray.50" zIndex={1}>Description</Table.ColumnHeader>
            <Table.ColumnHeader color="gray.500" fontWeight="medium" py={3} px={4} position="sticky" top={0} bg="gray.50" zIndex={1}>Category</Table.ColumnHeader>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {transactions.map((t, i) => (
            <Table.Row key={i} bg="white" _hover={{ bg: "gray.50" }}>
              <Table.Cell py={3} px={4} color="gray.500" fontSize="sm">
                {t.date}
              </Table.Cell>
              <Table.Cell py={3} px={4} fontSize="sm" maxW="280px">
                <Text color={"black"} truncate title={t.transaction}>{t.transaction}</Text>
              </Table.Cell>
              <Table.Cell py={3} px={4} textAlign="right" fontWeight="medium">
                <Text color={t.amount > 0 ? "green.600" : "red.600"} fontSize="sm">
                  {t.amount > 0 ? "+" : "-"}{fmt(t.amount)}
                </Text>
              </Table.Cell>
              <Table.Cell py={3} px={4} color="gray.600" fontSize="sm" maxW="200px">
                <Text truncate title={t.description}>{t.description}</Text>
              </Table.Cell>
              <Table.Cell py={3} px={4}>
                <Badge
                  size="sm"
                  colorPalette={t.is_direct ? "blue" : "purple"}
                  variant="solid"
                >
                  {t.is_direct ? "DIRECT" : "TOYYIBPAY"}
                </Badge>
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table.Root>
    </Box>
  </Box>
)

export default TransactionsTable

