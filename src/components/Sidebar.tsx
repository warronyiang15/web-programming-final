import { useState, useEffect, useRef } from "react"
import { Menu, X, User, CheckCircle2, Circle, LogOut, LayoutDashboard } from "lucide-react"

export function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(false)
  const [showUserMenu, setShowUserMenu] = useState(false)
  const userMenuRef = useRef<HTMLDivElement>(null)

  const toggleSidebar = () => {
    setIsCollapsed(!isCollapsed)
  }

  const handleUserClick = () => {
    // If sidebar is collapsed, expand it first
    if (isCollapsed) {
      setIsCollapsed(false)
      // Show menu after sidebar expands
      setTimeout(() => {
        setShowUserMenu(true)
      }, 100)
    } else {
      setShowUserMenu(!showUserMenu)
    }
  }

  const handleDashboard = () => {
    // Dummy dashboard function
    console.log("Dashboard clicked")
    setShowUserMenu(false)
  }

  const handleLogout = () => {
    // Dummy logout function
    console.log("Logout clicked")
    setShowUserMenu(false)
  }

  const handleStep1Click = () => {
    // Dummy function for first step
    console.log("Upload files clicked")
  }

  const handleStep2Click = () => {
    // Dummy function for second step
    console.log("Modify course outline clicked")
  }

  // Close user menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (userMenuRef.current && !userMenuRef.current.contains(event.target as Node)) {
        setShowUserMenu(false)
      }
    }

    if (showUserMenu) {
      document.addEventListener("mousedown", handleClickOutside)
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside)
    }
  }, [showUserMenu])

  return (
    <div
      className={`h-screen bg-[#1E2025] border-r border-[#3E4451] flex flex-col transition-all duration-300 ${isCollapsed ? "w-16" : "w-64"
        }`}
    >
      {/* Hamburger Menu */}
      <div className="relative p-4">
        <button
          onClick={toggleSidebar}
          className="absolute top-4 left-3 w-10 h-10 flex items-center justify-center p-2 rounded-md hover:bg-[#282C34] transition-colors flex-shrink-0"
          aria-label="Toggle sidebar"
        >
          {isCollapsed ? (
            <Menu className="w-5 h-5 text-[#E0E0E0]" />
          ) : (
            <X className="w-5 h-5 text-[#E0E0E0]" />
          )}
        </button>
      </div>

      {/* Steps Indicator */}
      {!isCollapsed && (
        <div className="flex-1 flex flex-col items-start justify-center py-8 gap-4 px-4">
          {/* Step 1 - Completed */}
          <button
            onClick={handleStep1Click}
            className="w-full flex items-center gap-3 hover:bg-[#282C34] rounded-md p-2 transition-colors"
            aria-label="Upload files"
          >
            <CheckCircle2 className="w-8 h-8 text-[#8DB472] flex-shrink-0" />
            <span className="text-xs text-[#5C6370] opacity-0 animate-[fadeIn_0.3s_ease-in-out_0.1s_forwards] whitespace-nowrap">Upload files</span>
          </button>

          {/* Connector Line */}
          <div className="w-px h-8 bg-[#3E4451] ml-[1.5rem]" />

          {/* Step 2 - Current */}
          <button
            onClick={handleStep2Click}
            className="w-full flex items-center gap-3 hover:bg-[#282C34] rounded-md p-2 transition-colors"
            aria-label="Modify course outline"
          >
            <Circle className="w-8 h-8 text-[#61AFEF] fill-[#61AFEF] flex-shrink-0" />
            <span className="text-xs text-[#E0E0E0] font-semibold opacity-0 animate-[fadeIn_0.3s_ease-in-out_0.2s_forwards] whitespace-nowrap">Modify course outline</span>
          </button>

          {/* Connector Line */}
          <div className="w-px h-8 bg-[#3E4451] ml-[1.5rem]" />

          {/* Step 3 - Upcoming */}
          <button className="w-full flex items-center gap-3 hover:bg-[#282C34] rounded-md p-2 transition-colors">
            <Circle className="w-8 h-8 text-[#5C6370] flex-shrink-0" />
            <span className="text-xs text-[#5C6370] opacity-0 animate-[fadeIn_0.3s_ease-in-out_0.3s_forwards] whitespace-nowrap">Modify website interface</span>
          </button>
        </div>
      )}

      {/* Collapsed Steps Indicator */}
      {isCollapsed && (
        <div className="flex-1 flex flex-col items-center justify-center py-8 gap-4">
          <button
            onClick={handleStep1Click}
            className="hover:bg-[#282C34] rounded-md p-1 transition-colors"
            aria-label="Upload files"
          >
            <CheckCircle2 className="w-5 h-5 text-[#8DB472]" />
          </button>
          <div className="w-px h-6 bg-[#3E4451]" />
          <button
            onClick={handleStep2Click}
            className="hover:bg-[#282C34] rounded-md p-1 transition-colors"
            aria-label="Modify course outline"
          >
            <Circle className="w-5 h-5 text-[#61AFEF] fill-[#61AFEF]" />
          </button>
          <div className="w-px h-6 bg-[#3E4451]" />
          <Circle className="w-5 h-5 text-[#5C6370]" />
        </div>
      )}

      {/* Avatar and Username */}
      <div ref={userMenuRef} className={`p-4 ${isCollapsed ? "flex items-center justify-center" : ""} relative`}>
        {isCollapsed ? (
          <button
            onClick={handleUserClick}
            className="w-10 h-10 rounded-full bg-[#282C34] flex items-center justify-center border border-[#3E4451] hover:bg-[#3E4451] transition-colors flex-shrink-0"
            aria-label="User menu"
          >
            <User className="w-5 h-5 text-[#E0E0E0]" />
          </button>
        ) : (
          <button
            onClick={handleUserClick}
            className="w-full flex items-center gap-3 hover:bg-[#282C34] rounded-md p-2 transition-colors"
            aria-label="User menu"
          >
            <div className="w-10 h-10 rounded-full bg-[#282C34] flex items-center justify-center border border-[#3E4451] flex-shrink-0">
              <User className="w-5 h-5 text-[#E0E0E0]" />
            </div>
            <span className="text-sm text-[#E0E0E0] font-medium">Guest</span>
          </button>
        )}

        {/* User Menu */}
        {showUserMenu && (
          <div className={`absolute bottom-full mb-2 ${isCollapsed ? "left-0 right-0" : "left-4 right-4"}`}>
            <div className="bg-[#282C34] border border-[#3E4451] rounded-md shadow-lg overflow-hidden flex flex-col gap-0">
              {/* Dashboard Button */}
              <button
                onClick={handleDashboard}
                className={`w-full flex items-center gap-3 px-4 py-2 hover:bg-[#3E4451] transition-colors text-sm text-[#E0E0E0] ${isCollapsed ? "justify-center" : ""}`}
              >
                <LayoutDashboard className="w-4 h-4 text-[#E0E0E0]" />
                {!isCollapsed && <span>Dashboard</span>}
              </button>

              {/* Divider */}
              <div className="h-px bg-[#3E4451]" />

              {/* Logout Button */}
              <button
                onClick={handleLogout}
                className={`w-full flex items-center gap-3 px-4 py-2 hover:bg-[#3E4451] transition-colors text-sm text-red-400 ${isCollapsed ? "justify-center" : ""}`}
              >
                <LogOut className="w-4 h-4 text-red-400" />
                {!isCollapsed && <span>Logout</span>}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

