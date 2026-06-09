import { LandingNav } from "@/components/landing/LandingNav";
import { Hero } from "@/components/landing/Hero";
import { Problem } from "@/components/landing/Problem";
import { Workflow } from "@/components/landing/Workflow";
import { GeminiLayer } from "@/components/landing/GeminiLayer";
import { Architecture } from "@/components/landing/Architecture";
import { Features } from "@/components/landing/Features";
import { TechStack } from "@/components/landing/TechStack";
import { Market } from "@/components/landing/Market";
import { Revenue } from "@/components/landing/Revenue";
import { WhyMinari } from "@/components/landing/WhyMinari";
import { Roadmap } from "@/components/landing/Roadmap";
import { Demo } from "@/components/landing/Demo";
import { CTA } from "@/components/landing/CTA";

// Marketing landing — composed from focused section components (each isolated and
// independently editable). The page stays a server component; interactive leaves
// (nav scroll-spy, starfield, animated pipeline, scroll-reveal) opt into "use client".
export default function Home() {
  return (
    <>
      <LandingNav />
      <main>
        <Hero />
        <Problem />
        <Workflow />
        <GeminiLayer />
        <Architecture />
        <Features />
        <TechStack />
        <Market />
        <Revenue />
        <WhyMinari />
        <Roadmap />
        <Demo />
        <CTA />
      </main>
    </>
  );
}
