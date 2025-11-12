import { ChevronDown, ChevronLeft, ChevronFirst, ChevronLast, Monitor, ExternalLink } from "lucide-react"

interface WebPreviewProps {
  onToggleChat: () => void
  onHidePreview?: () => void
  onShowChat?: () => void
  isChatHidden: boolean
  isSwapped?: boolean
}

export function WebPreview({ onToggleChat, onHidePreview, onShowChat, isChatHidden, isSwapped = false }: WebPreviewProps) {
  const handleOpenInNewTab = () => {
    // Hide the preview panel in the current tab
    if (onHidePreview) {
      onHidePreview()
    }
    // Show the chat section if it's hidden
    if (isChatHidden && onShowChat) {
      onShowChat()
    }
    // Open the full page preview in a new tab
    window.open("/web-preview", "_blank")
  }

  return (
    <div className="h-screen bg-[#1E2025] flex flex-col">
      {/* Fixed Header Section */}
      <div className="flex-shrink-0 p-6 pb-0">
        <div className="mb-6">
          <div className="flex items-center justify-between gap-2 mb-4">
            <div className="flex items-center gap-2">
              {!isSwapped && (
                <button
                  onClick={onToggleChat}
                  className="hover:bg-[#3E4451] rounded p-1 transition-colors"
                  aria-label="Toggle chat section"
                >
                  {isChatHidden ? (
                    <ChevronLast className="w-5 h-5 text-[#5B6B83] cursor-pointer" />
                  ) : (
                    <ChevronFirst className="w-5 h-5 text-[#5B6B83] cursor-pointer" />
                  )}
                </button>
              )}
              <h2 className="text-sm font-semibold text-[#5B6B83] uppercase tracking-[0.4rem]">
                Web Preview
              </h2>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={handleOpenInNewTab}
                className="hover:bg-[#3E4451] rounded p-1 transition-colors"
                aria-label="Open in new tab"
                title="Open in new tab"
              >
                <ExternalLink className="w-5 h-5 text-[#5B6B83] cursor-pointer" />
              </button>
              {isSwapped && (
                <button
                  onClick={onToggleChat}
                  className="hover:bg-[#3E4451] rounded p-1 transition-colors"
                  aria-label="Toggle chat section"
                >
                  {isChatHidden ? (
                    <ChevronFirst className="w-5 h-5 text-[#5B6B83] cursor-pointer" />
                  ) : (
                    <ChevronLast className="w-5 h-5 text-[#5B6B83] cursor-pointer" />
                  )}
                </button>
              )}
            </div>
          </div>
        </div>

        <div className="w-full h-px bg-[#3E4451] mb-6"></div>
      </div>

      {/* Scrollable Content Section */}
      <div className="flex-1 overflow-y-auto p-6 pt-0">
        <div className="w-full h-full min-h-[400px] bg-[#111620] border border-[#3E4451] rounded-lg overflow-hidden">
          <div className="h-full flex items-center justify-center">
            <div className="text-center">
              <Monitor className="w-16 h-16 mx-auto text-[#5C6370] mb-4" />
              <p className="text-[#5C6370] text-lg">
                Web preview will appear here
              </p>
              <p className="text-[#5C6370] text-sm mt-2">
                As you modify the layout, the preview will update in real-time
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

