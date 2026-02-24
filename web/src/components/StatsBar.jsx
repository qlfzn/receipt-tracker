import { Box, Grid, Stack, Text } from "@chakra-ui/react"

const StatCard = ({ label, value }) => (
  <Box
    bg="white"
    border="1px solid"
    borderColor="gray.200"
    borderRadius="lg"
    p={5}
  >
    <Stack gap={1}>
      <Text fontSize="xs" color="gray.500" fontWeight="medium">
        {label}
      </Text>
      <Text fontSize="xl" fontWeight="semibold" color="gray.900">
        {value}
      </Text>
    </Stack>
  </Box>
)

const fmt = (amount) =>
  `RM ${Math.abs(amount).toLocaleString("en-MY", { minimumFractionDigits: 2 })}`

const StatsBar = ({ transactions }) => {
  const totalCredits = transactions
    .filter((t) => t.amount > 0)
    .reduce((sum, t) => sum + t.amount, 0)

  const totalDebits = transactions
    .filter((t) => t.amount < 0)
    .reduce((sum, t) => sum + t.amount, 0)

  return (
    <Grid templateColumns="repeat(3, 1fr)" gap={4}>
      <StatCard label="Total Transactions" value={transactions.length} />
      <StatCard label="Total Credits" value={fmt(totalCredits)} />
      <StatCard label="Total Debits" value={fmt(totalDebits)} />
    </Grid>
  )
}

export default StatsBar
