import type { NextConfig } from "next";

const isDev = process.env.NODE_ENV !== "production";

// CSP must be environment-aware: React + Turbopack need 'unsafe-eval' and a
// websocket connection for Fast Refresh in DEVELOPMENT only. Production React
// never uses eval(), so prod stays strict (no 'unsafe-eval').
const scriptSrc = isDev
  ? "script-src 'self' 'unsafe-inline' 'unsafe-eval'"
  : "script-src 'self' 'unsafe-inline'"; // tighten with nonces post-hackathon

const connectSrc = isDev
  ? "connect-src 'self' ws: http://localhost:* https://*.run.app" // HMR websocket + API
  : "connect-src 'self' https://*.run.app"; // Cloud Run API

const securityHeaders = [
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "Permissions-Policy", value: "geolocation=(), microphone=(), camera=()" },
  {
    key: "Content-Security-Policy",
    value: [
      "default-src 'self'",
      scriptSrc,
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data:",
      "font-src 'self'", // Poppins is self-hosted -> no google domain needed
      connectSrc,
      "frame-ancestors 'none'",
    ].join("; "),
  },
];

const nextConfig: NextConfig = {
  poweredByHeader: false, // don't advertise the framework
  async headers() {
    return [{ source: "/:path*", headers: securityHeaders }];
  },
};

export default nextConfig;
