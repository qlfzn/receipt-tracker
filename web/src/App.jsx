import { useState } from "react"
import {
  Box,
  Button,
  FileUpload,
  Heading,
  Stack,
  Text,
  Alert,
  Spinner,
} from "@chakra-ui/react"
import StatsBar from "./components/StatsBar"
import TransactionsTable from "./components/TransactionsTable"

const API_URL = "http://localhost:8000/api/v1/files/upload"

const App = () => {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [data, setData] = useState(null)

  const handleFileChange = (details) => {
    setFile(details.acceptedFiles[0] ?? null)
    setError(null)
    setData(null)
  }

  const handleExtract = async () => {
    if (!file) return
    const formData = new FormData()
    formData.append("file", file)
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(API_URL, { method: "POST", body: formData })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail ?? "Something went wrong")
      }
      setData(await res.json())
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setFile(null)
    setData(null)
    setError(null)
  }

  return (
    <Box minH="100vh" bg="gray.50" px={4} py={10}>
      <Box w="full" maxW={data ? "1500px" : "480px"} mx="auto">
        <Stack gap={6}>
          {/* Upload card — full when no data, compact bar when data loaded */}
          {!data ? (
            <Box
              bg="white"
              w="full"
              borderRadius="lg"
              border="1px solid"
              borderColor="gray.200"
              p={8}
            >
              <Stack gap={6}>
                <Stack gap={1}>
                  <Heading size="md" fontWeight="semibold" color="gray.900">
                    Bank Statement Reader
                  </Heading>
                  <Text fontSize="sm" color="gray.500">
                    Upload your monthly PDF statement to extract and export
                    cashflow data.
                  </Text>
                </Stack>

                <FileUpload.Root
                  w="full"
                  maxFiles={1}
                  accept={{ "application/pdf": [".pdf"] }}
                  onFileChange={handleFileChange}
                >
                  <FileUpload.HiddenInput />
                  <FileUpload.Dropzone
                    w="full"
                    border="1.5px dashed"
                    borderColor="gray.300"
                    borderRadius="md"
                    bg="white"
                    p={8}
                    cursor="pointer"
                    display="flex"
                    alignItems="center"
                    justifyContent="center"
                    _hover={{ borderColor: "gray.400", bg: "gray.50" }}
                    transition="border-color 0.15s, background 0.15s"
                  >
                    <Stack gap={3} align="center">
                      <Stack gap={1} align="center">
                        <Text fontSize="sm" fontWeight="medium" color="gray.700">
                          Drag and drop your statement here
                        </Text>
                        <Text fontSize="xs" color="gray.400">
                          PDF format only
                        </Text>
                      </Stack>
                      <Text fontSize="xs" color="gray.400">
                        or
                      </Text>
                      <FileUpload.Trigger asChild>
                        <Button size="sm" variant="surface" colorPalette="black">
                          Browse file
                        </Button>
                      </FileUpload.Trigger>
                    </Stack>
                  </FileUpload.Dropzone>
                  <FileUpload.List mt={3} />
                </FileUpload.Root>

                {error && (
                  <Alert.Root status="error" borderRadius="md">
                    <Alert.Indicator />
                    <Alert.Description>{error}</Alert.Description>
                  </Alert.Root>
                )}

                <Button
                  disabled={!file || loading}
                  colorPalette="gray"
                  variant="surface"
                  onClick={handleExtract}
                >
                  {loading ? <Spinner size="sm" /> : "Extract Data"}
                </Button>
              </Stack>
            </Box>
          ) : (
            <Box
              bg="white"
              w="full"
              borderRadius="lg"
              border="1px solid"
              borderColor="gray.200"
              px={5}
              py={3}
              display="flex"
              alignItems="center"
              gap={4}
            >
              <Text fontSize="sm" color="gray.500" flex="1" truncate>
                <Text as="span" fontWeight="medium" color="gray.800">
                  {file?.name ?? "Statement"}
                </Text>
              </Text>
              {error && (
                <Text fontSize="sm" color="red.500">{error}</Text>
              )}
              <Button
                size="sm"
                variant="outline"
                color={"black"}
                onClick={handleReset}
                flexShrink={0}
                _hover={{ color: "white" }}
              >
                Upload New File
              </Button>
            </Box>
          )}

          {/* Results */}
          {data && (
            <Stack gap={4}>
              <StatsBar transactions={data.transactions} />
              <TransactionsTable transactions={data.transactions} />
            </Stack>
          )}
        </Stack>
      </Box>
    </Box>
  )
}

export default App