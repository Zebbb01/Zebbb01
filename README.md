<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Zebbb01/Zebbb01/main/assets/header.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Zebbb01/Zebbb01/main/assets/header-light.svg" />
  <img src="https://raw.githubusercontent.com/Zebbb01/Zebbb01/main/assets/header.svg" alt="Gerald Villaceran — Software Engineer, full-stack web and mobile" width="100%" />
</picture>

<br/>

**[Portfolio](https://portfolio-five-ruddy-49.vercel.app)** &nbsp;·&nbsp; [LinkedIn](https://www.linkedin.com/in/gerald-villaceran-798983325) &nbsp;·&nbsp; [Email](mailto:geraldvillaceran01@gmail.com)

</div>

<br/>

I build production platforms that carry real money and real operations. Right now that means a multi-tenant accounting SaaS I own end to end, shipped every week for six months straight, and the web platforms and admin portals behind an on-demand delivery operation — plus the customer, merchant and rider apps that talk to them.

Money paths run on `Decimal.js`, never floats. Tenant isolation is a PostgreSQL RLS policy, not an `if` statement. 92 Vitest and Playwright suites run in CI before anything ships.

<br/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Zebbb01/Zebbb01/main/assets/now.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Zebbb01/Zebbb01/main/assets/now-light.svg" />
  <img src="https://raw.githubusercontent.com/Zebbb01/Zebbb01/main/assets/now.svg" alt="Currently building — ProfitView Accounting: 24 modules live, 158K lines of TypeScript, 92 test suites in CI, release v0.66" width="100%" />
</picture>

<br/>

## Selected work

**ProfitView Accounting** — a double-entry ledger with the Philippine compliance layer built in rather than bolted on: VAT across taxable, zero-rated and exempt, expanded withholding tax, SLSP, BIR Books of Accounts.<br/>
<sub>[live](https://profit-view-swart.vercel.app/) · [case study](https://portfolio-five-ruddy-49.vercel.app/projects/profitview) · `Next.js 15` `Supabase` `PostgreSQL RLS` `Anthropic SDK` `Decimal.js` `Playwright`</sub>

**Body Tracker** — photograph the meal, skip the form. A vision model estimates the macros, the user corrects them, and every write lands in IndexedDB first so the app works with no signal.<br/>
<sub>[live](https://body-tracker-iota.vercel.app/) · [code](https://github.com/Zebbb01/Workout-Tracker) · [case study](https://portfolio-five-ruddy-49.vercel.app/projects/body-tracker) · `Next.js 16` `Supabase` `PWA` `IndexedDB`</sub>

**OSCA Civic Platform** — senior citizen affairs management for a local government office that was running records, benefits and reporting on paper.<br/>
<sub>[code](https://github.com/Zebbb01/OSCA) · `Next.js` `Prisma` `PostgreSQL` `NextAuth`</sub>

**Business automation** — multi-step pipelines across CRMs, email, payment gateways and internal tools. Event-driven where latency matters, scheduled where it does not, loud when a run fails.<br/>
<sub>[case study](https://portfolio-five-ruddy-49.vercel.app/projects/n8n-automation) · `n8n` `Make` `Webhooks` `GoHighLevel` `OCR`</sub>

<br/>

## How I build

<div align="center">

<img height="34" src="https://cdn.simpleicons.org/claude/D4AF37" alt="Claude" />&nbsp;&nbsp;&nbsp;
<img height="34" src="https://cdn.simpleicons.org/googlegemini/D4AF37" alt="Gemini" />&nbsp;&nbsp;&nbsp;
<img height="34" src="https://cdn.simpleicons.org/nextdotjs/D4AF37" alt="Next.js" />&nbsp;&nbsp;&nbsp;
<img height="34" src="https://cdn.simpleicons.org/typescript/D4AF37" alt="TypeScript" />&nbsp;&nbsp;&nbsp;
<img height="34" src="https://cdn.simpleicons.org/react/D4AF37" alt="React" />&nbsp;&nbsp;&nbsp;
<img height="34" src="https://cdn.simpleicons.org/expo/D4AF37" alt="Expo" />&nbsp;&nbsp;&nbsp;
<img height="34" src="https://cdn.simpleicons.org/supabase/D4AF37" alt="Supabase" />&nbsp;&nbsp;&nbsp;
<img height="34" src="https://cdn.simpleicons.org/postgresql/D4AF37" alt="PostgreSQL" />&nbsp;&nbsp;&nbsp;
<img height="34" src="https://cdn.simpleicons.org/tailwindcss/D4AF37" alt="Tailwind CSS" />&nbsp;&nbsp;&nbsp;
<img height="34" src="https://cdn.simpleicons.org/vercel/D4AF37" alt="Vercel" />&nbsp;&nbsp;&nbsp;
<img height="34" src="https://cdn.simpleicons.org/githubactions/D4AF37" alt="GitHub Actions" />&nbsp;&nbsp;&nbsp;
<img height="34" src="https://cdn.simpleicons.org/n8n/D4AF37" alt="n8n" />&nbsp;&nbsp;&nbsp;
<img height="34" src="https://cdn.simpleicons.org/figma/D4AF37" alt="Figma" />

</div>

<br/>

Started on Gemini's free tier — scaffolding, research, throwaway prototypes. The build itself now runs on **Claude Code**: an agent working inside the repository, writing against the test suite rather than around it. That is what a weekly release cadence costs in practice — **v0.66 after 26 straight weeks**, 460+ commits across four repositories, 24 modules live, and 92 suites that have to pass before any of it ships.

The rest of the toolchain is deliberately cheap: Supabase, Vercel and GitHub Actions all start free, which is the point. A solo engineer should be able to run a production platform on a free tier until real usage justifies paying for it.

<br/>

<details>
<summary><b>Full stack</b></summary>

<br/>

**Frontend** — `Next.js` `React` `React Native` `TypeScript` `Tailwind CSS` `Framer Motion` `Radix UI`<br/>
**Backend & infra** — `Supabase` `PostgreSQL` `Row Level Security` `REST APIs` `Webhooks` `Prisma` `Node.js` `Edge Functions` `Vercel`<br/>
**Mobile** — `React Native` `Expo` `Expo Router` `PWA` `Offline-first`<br/>
**Payments** — `PayMongo` `GCash` `Maya` `GrabPay` `Stripe` `Subscriptions`<br/>
**AI & automation** — `Claude Code` `Anthropic SDK` `OpenAI` `Gemini` `n8n` `Make` `OCR`<br/>
**Testing & reliability** — `Vitest` `Playwright` `Decimal.js` `Audit logging` `GitHub Actions`

</details>

<details>
<summary><b>Experience</b></summary>

<br/>

**Full-Stack Developer** · Poseidon Distribution OPC · *May 2026 — present*<br/>
Web platforms and region-scoped admin portals for an on-demand delivery and marketplace operation, plus the customer, merchant and rider apps. Real-time GPS tracking on Supabase Realtime, 70+ tables with triggers, RLS and audit logging, automated refunds and merchant settlements.

**Founder & Sole Engineer** · ProfitView · *Mar 2026 — present*<br/>
My own product, end to end: 24 modules, the Philippine compliance layer, the AI agent layer, 92 Vitest and Playwright suites in CI, 460+ commits across four repositories in six months.

**Freelance Software Engineer** · Independent · *2024 — 2026*<br/>
Civic tech for senior citizen affairs, an AI fitness PWA, a multi-provider AI chatbot, and automation systems for client operations.

</details>

<br/>

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Zebbb01/Zebbb01/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Zebbb01/Zebbb01/output/github-snake.svg" />
  <img src="https://raw.githubusercontent.com/Zebbb01/Zebbb01/output/github-snake-dark.svg" alt="Contribution graph" width="100%" />
</picture>

<br/><br/>

<sub>Philippines · GMT+8 &nbsp;·&nbsp; Open to work that ships &nbsp;·&nbsp; replies within 24 hours — <a href="mailto:geraldvillaceran01@gmail.com">geraldvillaceran01@gmail.com</a></sub>

</div>
