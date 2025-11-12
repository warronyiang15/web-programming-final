import { useState, useEffect, useRef } from "react"
import { useNavigate } from "react-router-dom"
import { User, LogOut, LayoutDashboard, Settings, HelpCircle } from "lucide-react"
import type { Project } from "@/types"

// Mock projects data
const mockProjects: Project[] = [
  {
    id: "project-1713175800000",
    name: "AI-Powered Course Design with React & Next.js",
    updatedAt: new Date("2024-04-15T10:30:00"),
    currentStep: "3",
  },
  {
    id: "project-1713088800000",
    name: "Introduction to Web Development",
    updatedAt: new Date("2024-04-14T15:20:00"),
    currentStep: "2",
  },
  {
    id: "project-1713002100000",
    name: "Advanced TypeScript Patterns",
    updatedAt: new Date("2024-04-13T09:15:00"),
    currentStep: "1",
  },
  {
    id: "project-1712916300000",
    name: "Full-Stack JavaScript Mastery",
    updatedAt: new Date("2024-04-12T14:45:00"),
    currentStep: "2",
  },
  {
    id: "project-1712830200000",
    name: "Machine Learning Fundamentals",
    updatedAt: new Date("2024-04-11T11:00:00"),
    currentStep: "1",
  },
  {
    id: "project-1712743800000",
    name: "UI/UX Design Principles",
    updatedAt: new Date("2024-04-10T16:30:00"),
    currentStep: "3",
  },
]

export function DashboardPage() {
  const navigate = useNavigate()
  const [showUserMenu, setShowUserMenu] = useState(false)
  const [activeTab, setActiveTab] = useState<"dashboard" | "settings" | "help-center">("dashboard")
  const userMenuRef = useRef<HTMLDivElement>(null)

  // Calculate statistics
  const totalProjects = mockProjects.length
  const step1Count = mockProjects.filter((p) => p.currentStep === "1").length
  const step2Count = mockProjects.filter((p) => p.currentStep === "2").length
  const step3Count = mockProjects.filter((p) => p.currentStep === "3").length
  const step4Count = mockProjects.filter((p) => p.currentStep === "4").length

  // Group projects by step and sort by updated date (newest first)
  const step1Projects = mockProjects
    .filter((p) => p.currentStep === "1")
    .sort((a, b) => b.updatedAt.getTime() - a.updatedAt.getTime())

  const step2Projects = mockProjects
    .filter((p) => p.currentStep === "2")
    .sort((a, b) => b.updatedAt.getTime() - a.updatedAt.getTime())

  const step3Projects = mockProjects
    .filter((p) => p.currentStep === "3")
    .sort((a, b) => b.updatedAt.getTime() - a.updatedAt.getTime())

  const step4Projects = mockProjects
    .filter((p) => p.currentStep === "4")
    .sort((a, b) => b.updatedAt.getTime() - a.updatedAt.getTime())

  const formatDate = (date: Date) => {
    return new Intl.DateTimeFormat("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "numeric",
      minute: "2-digit",
    }).format(date)
  }

  const generateUniqueProjectId = (existingProjects: Project[]): string => {
    let newId: string
    let attempts = 0
    const maxAttempts = 100

    do {
      newId = `project-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`
      attempts++
    } while (existingProjects.some((p) => p.id === newId) && attempts < maxAttempts)

    return newId
  }

  const handleCreateNewCourse = () => {
    // Generate a unique project ID that doesn't conflict with existing projects
    const newProjectId = generateUniqueProjectId(mockProjects)
    navigate(`/${newProjectId}/upload`)
  }

  const handleProjectClick = (project: Project) => {
    // Navigate based on the project's current step
    if (project.currentStep === "1") {
      navigate(`/${project.id}/upload`)
    } else if (project.currentStep === "2") {
      navigate(`/${project.id}/outline`)
    } else if (project.currentStep === "3") {
      navigate(`/${project.id}/web-design`)
    }
    // Step 4 (Deployed) projects are not clickable
  }

  const handleUserClick = () => {
    setShowUserMenu(!showUserMenu)
  }

  const handleLogout = () => {
    setShowUserMenu(false)
    console.log("Logout clicked")
    // Add logout logic here
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

  const getStepColor = (step: string) => {
    switch (step) {
      case "Step 1: Upload":
        return "#61AFEF"
      case "Step 2: Outline":
        return "#E5C07B"
      case "Step 3: Design":
        return "#56B6C2"
      case "Step 4: Deployed":
        return "#8DB472"
      default:
        return "#9DA5B4"
    }
  }

  const renderProjectSection = (title: string, projects: Project[]) => {
    if (projects.length === 0) return null

    const stepColor = getStepColor(title)
    const isDeployed = title === "Step 4: Deployed"

    return (
      <div>
        <h3 className="text-sm font-semibold text-[#E0E0E0] mb-3 flex items-center gap-2">
          <span className="w-2 h-2 rounded-full" style={{ backgroundColor: stepColor }} />
          {title}
        </h3>
        <div className="space-y-3">
          {projects.map((project) => (
            <div
              key={project.id}
              onClick={() => !isDeployed && handleProjectClick(project)}
              className={`flex items-center justify-between rounded-xl border border-[#3E4451] bg-[#282C34] px-4 py-3 transition-colors ${isDeployed
                ? ""
                : "hover:bg-[#2C313C] cursor-pointer"
                }`}
            >
              <span className="text-sm font-medium text-[#E0E0E0]">{project.name}</span>
              <span className="text-xs text-[#9DA5B4]">{formatDate(project.updatedAt)}</span>
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-screen bg-[#21252B] text-[#E0E0E0] overflow-hidden">
      {/* Header */}
      <header className="border-b border-[#3E4451] px-8 py-6 flex-shrink-0">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <div>
            <p className="text-sm uppercase tracking-wide text-[#9DA5B4]">Control Center</p>
            <h1 className="mt-2 text-3xl font-semibold text-[#E0E0E0]">Dashboard</h1>
          </div>
          <div ref={userMenuRef} className="relative">
            <button
              onClick={handleUserClick}
              className="flex items-center gap-3 hover:bg-[#282C34] rounded-lg px-4 py-3 transition-colors cursor-pointer"
              aria-label="User menu"
            >
              <div className="w-8 h-8 rounded-full bg-[#282C34] flex items-center justify-center border border-[#3E4451] flex-shrink-0">
                <User className="w-5 h-5 text-[#E0E0E0]" />
              </div>
              <span className="text-sm text-[#E0E0E0] font-medium">Guest</span>
            </button>

            {/* User Menu */}
            {showUserMenu && (
              <div className="absolute right-0 top-full mt-2">
                <div className="bg-[#282C34] border border-[#3E4451] rounded-md shadow-lg overflow-hidden flex flex-col gap-0 min-w-[160px]">
                  {/* Logout Button */}
                  <button
                    onClick={handleLogout}
                    className="w-full flex items-center gap-3 px-4 py-2 hover:bg-[#3E4451] transition-colors text-sm text-red-400 cursor-pointer"
                  >
                    <LogOut className="w-4 h-4 text-red-400" />
                    <span>Logout</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content Area with Side Panel */}
      <main className="flex-1 overflow-auto">
        <div className="mx-auto flex max-w-7xl">
          <div className="flex h-full">
            {/* Left Panel - No box, no border */}
            <div className="w-64 flex flex-col gap-1 p-2 pt-10">
              <button
                onClick={() => setActiveTab("dashboard")}
                className={`flex items-center gap-3 px-4 py-3 rounded-md transition-colors ${activeTab === "dashboard"
                  ? "bg-[#282C34] text-[#E0E0E0]"
                  : "text-[#9DA5B4] hover:bg-[#282C34] hover:text-[#E0E0E0]"
                  }`}
              >
                <LayoutDashboard className="w-5 h-5" />
                <span className={`text-sm ${activeTab === "dashboard" ? "font-semibold" : "font-medium"}`}>Dashboard</span>
              </button>
              <button
                onClick={() => setActiveTab("settings")}
                className={`flex items-center gap-3 px-4 py-3 rounded-md transition-colors ${activeTab === "settings"
                  ? "bg-[#282C34] text-[#E0E0E0]"
                  : "text-[#9DA5B4] hover:bg-[#282C34] hover:text-[#E0E0E0]"
                  }`}
              >
                <Settings className="w-5 h-5" />
                <span className={`text-sm ${activeTab === "settings" ? "font-semibold" : "font-medium"}`}>Settings</span>
              </button>
              <button
                onClick={() => setActiveTab("help-center")}
                className={`flex items-center gap-3 px-4 py-3 rounded-md transition-colors ${activeTab === "help-center"
                  ? "bg-[#282C34] text-[#E0E0E0]"
                  : "text-[#9DA5B4] hover:bg-[#282C34] hover:text-[#E0E0E0]"
                  }`}
              >
                <HelpCircle className="w-5 h-5" />
                <span className={`text-sm ${activeTab === "help-center" ? "font-semibold" : "font-medium"}`}>Help Center</span>
              </button>
            </div>

            {/* Dashboard Content */}
            <div className="flex-1">
              <div className="mx-auto flex max-w-7xl flex-col gap-8 px-8 py-10">
                {/* Statistics Section */}
                <section className="flex flex-wrap gap-6">
                  <div className="rounded-2xl border-2 border-[#C678DD] bg-[#1E2025] p-6 w-full md:w-full xl:w-auto xl:flex-1 xl:min-w-0">
                    <p className="text-sm text-[#9DA5B4]">Total Projects</p>
                    <p className="mt-4 text-4xl font-semibold text-[#C678DD]">{totalProjects}</p>
                  </div>
                  <div className="w-px bg-[#3E4451] self-stretch hidden xl:block" />
                  <div className="rounded-2xl border-2 border-[#61AFEF] bg-[#1E2025] p-6 flex-1 min-w-[calc(50%-12px)] md:flex-1 md:min-w-0 xl:flex-1 xl:min-w-0">
                    <p className="text-sm text-[#9DA5B4]">Step 1: Upload</p>
                    <p className="mt-4 text-4xl font-semibold text-[#61AFEF]">{step1Count}</p>
                  </div>
                  <div className="rounded-2xl border-2 border-[#E5C07B] bg-[#1E2025] p-6 flex-1 min-w-[calc(50%-12px)] md:flex-1 md:min-w-0 xl:flex-1 xl:min-w-0">
                    <p className="text-sm text-[#9DA5B4]">Step 2: Outline</p>
                    <p className="mt-4 text-4xl font-semibold text-[#E5C07B]">{step2Count}</p>
                  </div>
                  <div className="rounded-2xl border-2 border-[#56B6C2] bg-[#1E2025] p-6 flex-1 min-w-[calc(50%-12px)] md:flex-1 md:min-w-0 xl:flex-1 xl:min-w-0">
                    <p className="text-sm text-[#9DA5B4]">Step 3: Design</p>
                    <p className="mt-4 text-4xl font-semibold text-[#56B6C2]">{step3Count}</p>
                  </div>
                  <div className="rounded-2xl border-2 border-[#8DB472] bg-[#1E2025] p-6 flex-1 min-w-[calc(50%-12px)] md:flex-1 md:min-w-0 xl:flex-1 xl:min-w-0">
                    <p className="text-sm text-[#9DA5B4]">Step 4: Deployed</p>
                    <p className="mt-4 text-4xl font-semibold text-[#8DB472]">{step4Count}</p>
                  </div>
                </section>

                {/* Projects List Section */}
                <section className="rounded-2xl border border-[#3E4451] bg-[#1E2025] p-6">
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-lg font-medium text-[#E0E0E0]">Current Projects</h2>
                    <button
                      onClick={handleCreateNewCourse}
                      className="rounded-md bg-[#61AFEF] px-4 py-2 text-sm font-medium text-[#1E2025] transition hover:bg-[#82C6FF]"
                    >
                      Create New Course
                    </button>
                  </div>
                  <div className="space-y-6">
                    {renderProjectSection("Step 1: Upload", step1Projects)}
                    {step1Projects.length > 0 && (step2Projects.length > 0 || step3Projects.length > 0 || step4Projects.length > 0) && (
                      <div className="border-t border-[#3E4451]" />
                    )}
                    {renderProjectSection("Step 2: Outline", step2Projects)}
                    {step2Projects.length > 0 && (step3Projects.length > 0 || step4Projects.length > 0) && (
                      <div className="border-t border-[#3E4451]" />
                    )}
                    {renderProjectSection("Step 3: Design", step3Projects)}
                    {step3Projects.length > 0 && step4Projects.length > 0 && (
                      <div className="border-t border-[#3E4451]" />
                    )}
                    {renderProjectSection("Step 4: Deployed", step4Projects)}
                  </div>
                </section>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

