import * as React from "react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  onConfirm: () => void
  title?: string
  message: string
  confirmText?: string
  cancelText?: string
}

export function Modal({
  isOpen,
  onClose,
  onConfirm,
  title = "Confirm Action",
  message,
  confirmText = "Confirm",
  cancelText = "Cancel",
}: ModalProps) {
  if (!isOpen) return null

  const handleBackdropClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget) {
      onClose()
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      onClick={handleBackdropClick}
    >
      <div
        className={cn(
          "bg-[#282C34] border border-[#3E4451] rounded-lg shadow-lg p-6 max-w-md w-full mx-4",
          "transition-all duration-200"
        )}
        onClick={(e) => e.stopPropagation()}
      >
        {title && (
          <h2 className="text-xl font-semibold text-[#E0E0E0] mb-4">{title}</h2>
        )}
        <p className="text-sm text-[#ABB2BF] mb-6">{message}</p>
        <div className="flex gap-3 justify-end">
          <Button
            variant="outline"
            onClick={onClose}
            className="cursor-pointer"
          >
            {cancelText}
          </Button>
          <Button
            variant="default"
            onClick={onConfirm}
            className="cursor-pointer"
          >
            {confirmText}
          </Button>
        </div>
      </div>
    </div>
  )
}

