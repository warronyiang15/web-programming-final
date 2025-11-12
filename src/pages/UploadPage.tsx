import { useRef, useState } from "react"
import type { ChangeEvent, DragEvent } from "react"
import { useNavigate } from "react-router-dom"
import "@/App.css"
import { Sidebar } from "@/components/Sidebar"

export function UploadPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const navigate = useNavigate()

  const validateFile = (file: File | null) => {
    if (!file) return false

    const isPdf =
      file.type === "application/pdf" ||
      file.name.toLowerCase().endsWith(".pdf")

    if (!isPdf) {
      setError("Please upload a PDF file.")
      setSelectedFile(null)
      return false
    }

    setError(null)
    setSelectedFile(file)
    return true
  }

  const handleDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    event.stopPropagation()
    setIsDragging(false)

    const file = event.dataTransfer.files?.[0]
    if (!file) return

    validateFile(file)
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
    const file = event.target.files?.[0] ?? null
    if (!file) return

    validateFile(file)
  }

  const handleBrowseClick = () => {
    fileInputRef.current?.click()
  }

  const handleRemoveFile = () => {
    setSelectedFile(null)
    setError(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
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
      <Sidebar currentStep={1} onStepSelect={(step) => step === 1 && navigate("/outline")} />

      <main className="flex-1 flex flex-col items-center justify-center p-10 overflow-auto">
        <div className="w-full max-w-2xl">
          <header className="mb-8">
            <h1 className="text-3xl font-semibold mb-3">Upload your course materials</h1>
            <p className="text-sm text-[#9DA5B4]">
              Upload a single PDF to kick-start outline generation. Your document remains private and is only used for this session.
            </p>
          </header>

          <section
            className={`border-2 border-dashed rounded-2xl bg-[#1E2025] transition-colors duration-200 ${
              isDragging ? "border-[#61AFEF] bg-[#2C313C]" : "border-[#3E4451]"
            }`}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
          >
            <div className="flex flex-col items-center text-center gap-4 px-10 py-14">
              <div className="flex flex-col gap-1">
                <span className="text-lg font-medium">Drag &amp; drop your PDF here</span>
                <span className="text-sm text-[#9DA5B4]">Only PDF files are supported at the moment</span>
              </div>

              <button
                type="button"
                onClick={handleBrowseClick}
                className="px-6 py-2 rounded-md bg-[#61AFEF] text-[#1E2025] font-medium hover:bg-[#82C6FF] transition-colors cursor-pointer"
              >
                Browse files
              </button>

              <input
                ref={fileInputRef}
                type="file"
                accept="application/pdf,.pdf"
                onChange={handleFileInput}
                className="hidden"
              />
            </div>
          </section>

          {selectedFile && !error && (
            <div className="mt-6 flex items-center justify-between bg-[#1E2025] border border-[#3E4451] rounded-xl px-5 py-4">
              <div className="flex flex-col text-left">
                <span className="text-sm font-medium">{selectedFile.name}</span>
                <span className="text-xs text-[#9DA5B4]">{formatFileSize(selectedFile.size)}</span>
              </div>
              <button
                type="button"
                onClick={handleRemoveFile}
                className="text-sm text-[#FF6B6B] hover:text-[#FF8A8A] transition-colors"
              >
                Remove
              </button>
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


