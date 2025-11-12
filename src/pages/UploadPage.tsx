import { useRef, useState } from "react"
import type { ChangeEvent, DragEvent } from "react"
import { useNavigate, useParams } from "react-router-dom"
import "@/App.css"
import { Sidebar } from "@/components/Sidebar"

const MAX_FILES = 10

export function UploadPage() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([])
  const [error, setError] = useState<string | null>(null)
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const navigate = useNavigate()
  const { id } = useParams<{ id: string }>()

  const validateFiles = (files: File[], currentFileCount: number) => {
    const validFiles: File[] = []
    let validationError: string | null = null

    for (const file of files) {
      const isPdf =
        file.type === "application/pdf" ||
        file.name.toLowerCase().endsWith(".pdf")

      if (!isPdf) {
        validationError = "Please upload only PDF files."
        continue
      }

      validFiles.push(file)
    }

    if (validFiles.length === 0 && files.length > 0) {
      setError(validationError || "Please upload PDF files.")
      return []
    }

    const newCount = currentFileCount + validFiles.length

    if (newCount > MAX_FILES) {
      const allowedCount = MAX_FILES - currentFileCount
      if (allowedCount > 0) {
        setError(`You can only upload up to ${MAX_FILES} files. Only the first ${allowedCount} file(s) will be added.`)
        return validFiles.slice(0, allowedCount)
      } else {
        setError(`You can only upload up to ${MAX_FILES} files. Please remove some files first.`)
        return []
      }
    }

    setError(null)
    return validFiles
  }

  const addFiles = (newFiles: File[]) => {
    setSelectedFiles((prev) => {
      const validFiles = validateFiles(newFiles, prev.length)
      if (validFiles.length > 0) {
        return [...prev, ...validFiles]
      }
      return prev
    })
  }

  const handleDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    event.stopPropagation()
    setIsDragging(false)

    const files = Array.from(event.dataTransfer.files || [])
    if (files.length === 0) return

    addFiles(files)
  }

  const handleDragOver = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    event.stopPropagation()
    setIsDragging(true)
  }

  const handleDragLeave = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    event.stopPropagation()
    setIsDragging(false)
  }

  const handleFileInput = (event: ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || [])
    if (files.length === 0) return

    addFiles(files)
    
    // Reset input to allow selecting the same file again
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  const handleBrowseClick = () => {
    fileInputRef.current?.click()
  }

  const handleRemoveFile = (index: number) => {
    setSelectedFiles((prev) => prev.filter((_, i) => i !== index))
    setError(null)
  }

  const formatFileSize = (sizeInBytes: number) => {
    const sizeInMegabytes = sizeInBytes / (1024 * 1024)
    if (sizeInMegabytes < 0.1) {
      const sizeInKilobytes = sizeInBytes / 1024
      return `${sizeInKilobytes.toFixed(1)} KB`
    }

    return `${sizeInMegabytes.toFixed(1)} MB`
  }

  return (
    <div className="flex h-screen bg-[#21252B] overflow-hidden text-[#E0E0E0]">
      <Sidebar currentStep={1} onStepSelect={(step) => step === 1 && id && navigate(`/${id}/outline`)} />

      <main className="flex-1 flex flex-col items-center justify-center p-10 overflow-auto">
        <div className="w-full max-w-2xl">
          <header className="mb-8">
            <h1 className="text-3xl font-semibold mb-3">Upload your course materials</h1>
            <p className="text-sm text-[#9DA5B4]">
              Upload up to {MAX_FILES} PDF files to kick-start outline generation. Your documents remain private and are only used for this session.
            </p>
          </header>

          <section
            className={`border-2 border-dashed rounded-2xl bg-[#1E2025] transition-colors duration-200 ${
              isDragging ? "border-[#61AFEF] bg-[#2C313C]" : "border-[#3E4451]"
            } ${selectedFiles.length >= MAX_FILES ? "opacity-50 cursor-not-allowed" : ""}`}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
          >
            <div className="flex flex-col items-center text-center gap-4 px-10 py-14">
              <div className="flex flex-col gap-1">
                <span className="text-lg font-medium">Drag &amp; drop your PDF files here</span>
                <span className="text-sm text-[#9DA5B4]">
                  Only PDF files are supported at the moment
                  {selectedFiles.length > 0 && ` (${selectedFiles.length}/${MAX_FILES} files selected)`}
                </span>
              </div>

              <button
                type="button"
                onClick={handleBrowseClick}
                disabled={selectedFiles.length >= MAX_FILES}
                className="px-6 py-2 rounded-md bg-[#61AFEF] text-[#1E2025] font-medium hover:bg-[#82C6FF] transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Browse files
              </button>

              <input
                ref={fileInputRef}
                type="file"
                accept="application/pdf,.pdf"
                multiple
                onChange={handleFileInput}
                className="hidden"
              />
            </div>
          </section>

          {selectedFiles.length > 0 && (
            <div className="mt-6 space-y-3">
              {selectedFiles.map((file, index) => (
                <div
                  key={`${file.name}-${index}`}
                  className="flex items-center justify-between bg-[#1E2025] border border-[#3E4451] rounded-xl px-5 py-4"
                >
                  <div className="flex flex-col text-left flex-1 min-w-0">
                    <span className="text-sm font-medium truncate">{file.name}</span>
                    <span className="text-xs text-[#9DA5B4]">{formatFileSize(file.size)}</span>
                  </div>
                  <button
                    type="button"
                    onClick={() => handleRemoveFile(index)}
                    className="text-sm text-[#FF6B6B] hover:text-[#FF8A8A] transition-colors ml-4 flex-shrink-0"
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
          )}

          {error && (
            <div className="mt-6 rounded-xl border border-[#FF6B6B] bg-[#2B1F23] px-5 py-3 text-sm text-[#FF8A8A]">
              {error}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}


