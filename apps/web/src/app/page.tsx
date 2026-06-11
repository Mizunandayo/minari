import { LandingNav } from "@/components/landing/LandingNav";
import { Hero } from "@/components/landing/Hero";
import { Problem } from "@/components/landing/Problem";
import { Workflow } from "@/components/landing/Workflow";
import { Demo } from "@/components/landing/Demo";
import { Architecture } from "@/components/landing/Architecture";
import { GeminiLayer } from "@/components/landing/GeminiLayer";
import { Features } from "@/components/landing/Features";
import { TechStack } from "@/components/landing/TechStack";
import { WhyMinari } from "@/components/landing/WhyMinari";
import { Market } from "@/components/landing/Market";
import { Revenue } from "@/components/landing/Revenue";
import { Roadmap } from "@/components/landing/Roadmap";
import { CTA } from "@/components/landing/CTA";

// Marketing landing — composed from focused section components (each isolated and
// independently editable). The page stays a server component; interactive leaves
// (nav scroll-spy, starfield, animated pipeline, scroll-reveal) opt into "use client".
//
// Section order tells the hackathon story: hook → problem → how it works →
// proof (demo) → technical depth (GitLab MCP + Gemini) → differentiation →
// business case → roadmap → call to action.
export default function Home() {
  return (
    <>
      <LandingNav />
      <main>
        <Hero />
        <Problem />
        <Workflow />
        <Demo />
        <Architecture />
        <GeminiLayer />
        <Features />
        <TechStack />
        <WhyMinari />
        <Market />
        <Revenue />
        <Roadmap />
        <CTA />
      </main>
    </>
  );
}
