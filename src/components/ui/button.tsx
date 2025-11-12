import * as React from "react"
import { useState, useEffect } from "react"
import { cn } from "@/lib/utils"

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "outline" | "ghost"
  size?: "default" | "sm" | "lg"
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "default", ...props }, ref) => {
    // Theme state
    const [theme, setTheme] = useState<"light" | "dark" | "system">(() => {
      const savedTheme = localStorage.getItem("theme") as "light" | "dark" | "system" | null
      return savedTheme || "dark"
    })

    // Listen for theme changes
    useEffect(() => {
      const handleStorageChange = () => {
        const savedTheme = localStorage.getItem("theme") as "light" | "dark" | "system" | null
        if (savedTheme) {
          setTheme(savedTheme)
        }
      }
      window.addEventListener("storage", handleStorageChange)
      const interval = setInterval(() => {
        const savedTheme = localStorage.getItem("theme") as "light" | "dark" | "system" | null
        if (savedTheme && savedTheme !== theme) {
          setTheme(savedTheme)
        }
      }, 100)
      return () => {
        window.removeEventListener("storage", handleStorageChange)
        clearInterval(interval)
      }
    }, [theme])

    const getVariantClasses = () => {
      if (variant === "default") {
        return theme === "light"
          ? "bg-[#61AFEF] text-white hover:bg-[#528CC2]"
          : "bg-[#61AFEF] text-[#282C34] hover:bg-[#528CC2]"
      }
      if (variant === "outline") {
        return theme === "light"
          ? "border border-gray-300 bg-transparent hover:bg-gray-100 text-gray-800"
          : "border border-[#3E4451] bg-transparent hover:bg-[#282C34]"
      }
      if (variant === "ghost") {
        return theme === "light"
          ? "hover:bg-gray-100"
          : "hover:bg-[#282C34]"
      }
      return ""
    }

    return (
      <button
        className={cn(
          "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 cursor-pointer disabled:cursor-not-allowed disabled:opacity-50",
          getVariantClasses(),
          {
            "h-10 px-4 py-2": size === "default",
            "h-9 px-3": size === "sm",
            "h-11 px-8": size === "lg",
          },
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button }

