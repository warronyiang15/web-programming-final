import { Monitor } from "lucide-react"

export function FullPageWebPreviewPage() {
  return (
    <div className="h-screen w-screen bg-[#111620] flex items-center justify-center">
      <div className="w-full h-full flex items-center justify-center">
        <div className="text-center">
          <Monitor className="w-16 h-16 mx-auto text-[#5C6370] mb-4" />
          <p className="text-[#5C6370] text-lg">
            Full Page Web Preview
          </p>
          <p className="text-[#5C6370] text-sm mt-2">
            This is a full-page preview of your website layout
          </p>
        </div>
      </div>
    </div>
  )
}

