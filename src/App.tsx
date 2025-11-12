import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom"
import { DashboardPage } from "@/pages/DashboardPage"
import { HomePage } from "@/pages/HomePage"
import { OutlinePage } from "@/pages/OutlinePage"
import { UploadPage } from "@/pages/UploadPage"
import { WebDesignPage } from "@/pages/WebDesignPage"
import { FullPageWebPreviewPage } from "@/pages/FullPageWebPreviewPage"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/outline" element={<OutlinePage />} />
        <Route path="/web-design" element={<WebDesignPage />} />
        <Route path="/web-preview" element={<FullPageWebPreviewPage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
