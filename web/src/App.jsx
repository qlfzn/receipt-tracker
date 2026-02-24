import { useState } from "react"
import {
  Box,
  Button,
  FileUpload,
  Heading,
  Stack,
  Text,
} from "@chakra-ui/react"

const App = () => {
  const [hasFile, setHasFile] = useState(false)

  return (
    <Box
      minH="100vh"
      bg="gray.50"
      display="flex"
      alignItems="center"
      justifyContent="center"
      px={4}
    >
      <Box
        bg="white"
        w="full"
        maxW="480px"
        borderRadius="lg"
        border="1px solid"
        borderColor="gray.200"
        p={8}
      >
        <Stack gap={6}>
          {/* Header */}
          <Stack gap={1}>
            <Heading size="md" fontWeight="semibold" color="gray.900">
              Bank Statement Reader
            </Heading>
            <Text fontSize="sm" color="gray.500">
              Upload your monthly PDF statement to extract and export cashflow
              data.
            </Text>
          </Stack>

          {/* Upload area */}
          <FileUpload.Root
            w="full"
            maxFiles={1}
            accept={{ "application/pdf": [".pdf"] }}
            onFileChange={(details) =>
              setHasFile(details.acceptedFiles.length > 0)
            }
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
                  <Button size="sm" variant="outline" colorPalette="gray">
                    Browse file
                  </Button>
                </FileUpload.Trigger>
              </Stack>
            </FileUpload.Dropzone>

            <FileUpload.List mt={3} />
          </FileUpload.Root>

          {/* Action button */}
          <Button
            w="full"
            disabled={!hasFile}
            colorPalette="gray"
            variant="solid"
          >
            Extract Data
          </Button>
        </Stack>
      </Box>
    </Box>
  )
}

export default App